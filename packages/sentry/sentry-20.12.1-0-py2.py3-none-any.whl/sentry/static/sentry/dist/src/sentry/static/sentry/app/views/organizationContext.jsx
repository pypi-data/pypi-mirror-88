import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import PropTypes from 'prop-types';
import { openSudo } from 'app/actionCreators/modal';
import { fetchOrganizationDetails } from 'app/actionCreators/organization';
import ProjectActions from 'app/actions/projectActions';
import Alert from 'app/components/alert';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Sidebar from 'app/components/sidebar';
import { ORGANIZATION_FETCH_ERROR_TYPES } from 'app/constants';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import ConfigStore from 'app/stores/configStore';
import HookStore from 'app/stores/hookStore';
import OrganizationStore from 'app/stores/organizationStore';
import space from 'app/styles/space';
import { metric } from 'app/utils/analytics';
import { callIfFunction } from 'app/utils/callIfFunction';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import withApi from 'app/utils/withApi';
import withOrganizations from 'app/utils/withOrganizations';
var defaultProps = {
    detailed: true,
};
var OrganizationContext = /** @class */ (function (_super) {
    __extends(OrganizationContext, _super);
    function OrganizationContext() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.unlisteners = [
            ProjectActions.createSuccess.listen(function () { return _this.onProjectCreation(); }, undefined),
            OrganizationStore.listen(function (data) { return _this.loadOrganization(data); }, undefined),
        ];
        _this.remountComponent = function () {
            _this.setState(_this.getDefaultState(), _this.fetchData);
        };
        return _this;
    }
    OrganizationContext.prototype.getChildContext = function () {
        return {
            organization: this.state.organization,
        };
    };
    OrganizationContext.prototype.componentDidMount = function () {
        this.fetchData();
    };
    OrganizationContext.prototype.componentDidUpdate = function (prevProps) {
        var hasOrgIdAndChanged = prevProps.params.orgId &&
            this.props.params.orgId &&
            prevProps.params.orgId !== this.props.params.orgId;
        var hasOrgId = this.props.params.orgId ||
            (this.props.useLastOrganization && ConfigStore.get('lastOrganization'));
        // protect against the case where we finish fetching org details
        // and then `OrganizationsStore` finishes loading:
        // only fetch in the case where we don't have an orgId
        //
        // Compare `getOrganizationSlug`  because we may have a last used org from server
        // if there is no orgId in the URL
        var organizationLoadingChanged = prevProps.organizationsLoading !== this.props.organizationsLoading &&
            this.props.organizationsLoading === false;
        if (hasOrgIdAndChanged ||
            (!hasOrgId && organizationLoadingChanged) ||
            (this.props.location.state === 'refresh' && prevProps.location.state !== 'refresh')) {
            this.remountComponent();
        }
    };
    OrganizationContext.prototype.componentWillUnmount = function () {
        this.unlisteners.forEach(callIfFunction);
    };
    OrganizationContext.prototype.getDefaultState = function () {
        if (this.isOrgStorePopulatedCorrectly()) {
            // retrieve initial state from store
            return OrganizationStore.get();
        }
        return {
            loading: true,
            error: null,
            errorType: null,
            organization: null,
        };
    };
    OrganizationContext.prototype.onProjectCreation = function () {
        // If a new project was created, we need to re-fetch the
        // org details endpoint, which will propagate re-rendering
        // for the entire component tree
        fetchOrganizationDetails(this.props.api, this.getOrganizationSlug(), true, true);
    };
    OrganizationContext.prototype.getOrganizationSlug = function () {
        var _a, _b;
        return (this.props.params.orgId ||
            (this.props.useLastOrganization &&
                (ConfigStore.get('lastOrganization') || ((_b = (_a = this.props.organizations) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.slug))));
    };
    OrganizationContext.prototype.isOrgChanging = function () {
        var organization = OrganizationStore.get().organization;
        return organization && organization.slug !== this.getOrganizationSlug();
    };
    OrganizationContext.prototype.isOrgStorePopulatedCorrectly = function () {
        var detailed = this.props.detailed;
        var _a = OrganizationStore.get(), organization = _a.organization, dirty = _a.dirty;
        return (!dirty &&
            organization &&
            !this.isOrgChanging() &&
            (!detailed || (detailed && organization.projects && organization.teams)));
    };
    OrganizationContext.prototype.isLoading = function () {
        // In the absence of an organization slug, the loading state should be
        // derived from this.props.organizationsLoading from OrganizationsStore
        if (!this.getOrganizationSlug()) {
            return this.props.organizationsLoading;
        }
        // The following loading logic exists because we could either be waiting for
        // the whole organization object to come in or just the teams and projects.
        var _a = this.state, loading = _a.loading, error = _a.error, organization = _a.organization;
        var detailed = this.props.detailed;
        return (loading ||
            (!error &&
                detailed &&
                (!organization || !organization.projects || !organization.teams)));
    };
    OrganizationContext.prototype.fetchData = function () {
        if (!this.getOrganizationSlug()) {
            return;
        }
        // fetch from the store, then fetch from the API if necessary
        if (this.isOrgStorePopulatedCorrectly()) {
            return;
        }
        metric.mark({ name: 'organization-details-fetch-start' });
        fetchOrganizationDetails(this.props.api, this.getOrganizationSlug(), this.props.detailed, !this.isOrgChanging() // if true, will preserve a lightweight org that was fetched
        );
    };
    OrganizationContext.prototype.loadOrganization = function (orgData) {
        var _this = this;
        var organization = orgData.organization, error = orgData.error;
        var hooks = [];
        if (organization && !error) {
            HookStore.get('organization:header').forEach(function (cb) {
                hooks.push(cb(organization));
            });
            // Configure scope to have organization tag
            Sentry.configureScope(function (scope) {
                // XXX(dcramer): this is duplicated in sdk.py on the backend
                scope.setTag('organization', organization.id);
                scope.setTag('organization.slug', organization.slug);
                scope.setContext('organization', { id: organization.id, slug: organization.slug });
            });
        }
        else if (error) {
            // If user is superuser, open sudo window
            var user = ConfigStore.get('user');
            if (!user || !user.isSuperuser || error.status !== 403) {
                // This `catch` can swallow up errors in development (and tests)
                // So let's log them. This may create some noise, especially the test case where
                // we specifically test this branch
                console.error(error); // eslint-disable-line no-console
            }
            else {
                openSudo({
                    retryRequest: function () { return Promise.resolve(_this.fetchData()); },
                });
            }
        }
        this.setState(__assign(__assign({}, orgData), { hooks: hooks }), function () {
            // Take a measurement for when organization details are done loading and the new state is applied
            if (organization) {
                metric.measure({
                    name: 'app.component.perf',
                    start: 'organization-details-fetch-start',
                    data: {
                        name: 'org-details',
                        route: getRouteStringFromRoutes(_this.props.routes),
                        organization_id: parseInt(organization.id, 10),
                    },
                });
            }
        });
    };
    OrganizationContext.prototype.getOrganizationDetailsEndpoint = function () {
        return "/organizations/" + this.getOrganizationSlug() + "/";
    };
    OrganizationContext.prototype.getTitle = function () {
        if (this.state.organization) {
            return this.state.organization.name;
        }
        return 'Sentry';
    };
    OrganizationContext.prototype.renderSidebar = function () {
        if (!this.props.includeSidebar) {
            return null;
        }
        var _a = this.props, _ = _a.children, props = __rest(_a, ["children"]);
        return <Sidebar {...props} organization={this.state.organization}/>;
    };
    OrganizationContext.prototype.renderError = function () {
        var errorComponent;
        switch (this.state.errorType) {
            case ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND:
                errorComponent = (<Alert type="error">
            {t('The organization you were looking for was not found.')}
          </Alert>);
                break;
            default:
                errorComponent = <LoadingError onRetry={this.remountComponent}/>;
        }
        return <ErrorWrapper>{errorComponent}</ErrorWrapper>;
    };
    OrganizationContext.prototype.render = function () {
        if (this.isLoading()) {
            return (<LoadingIndicator triangle>
          {t('Loading data for your organization.')}
        </LoadingIndicator>);
        }
        if (this.state.error) {
            return (<React.Fragment>
          {this.renderSidebar()}
          {this.renderError()}
        </React.Fragment>);
        }
        return (<DocumentTitle title={this.getTitle()}>
        <div className="app">
          {this.state.hooks}
          {this.renderSidebar()}
          {this.props.children}
        </div>
      </DocumentTitle>);
    };
    OrganizationContext.propTypes = {
        api: PropTypes.object,
        routes: PropTypes.arrayOf(PropTypes.object),
        includeSidebar: PropTypes.bool,
        useLastOrganization: PropTypes.bool,
        organizationsLoading: PropTypes.bool,
        organizations: PropTypes.arrayOf(SentryTypes.Organization),
        detailed: PropTypes.bool,
    };
    OrganizationContext.childContextTypes = {
        organization: SentryTypes.Organization,
    };
    OrganizationContext.defaultProps = defaultProps;
    return OrganizationContext;
}(React.Component));
export default withApi(withOrganizations(Sentry.withProfiler(OrganizationContext)));
export { OrganizationContext };
var ErrorWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(3));
var templateObject_1;
//# sourceMappingURL=organizationContext.jsx.map