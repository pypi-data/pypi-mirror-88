import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import AsyncComponent from 'app/components/asyncComponent';
import NotFound from 'app/components/errors/notFound';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
var OrgDashboards = /** @class */ (function (_super) {
    __extends(OrgDashboards, _super);
    function OrgDashboards() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            dashboards: [],
            selectedDashboard: null,
        };
        return _this;
    }
    OrgDashboards.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var url = "/organizations/" + organization.slug + "/dashboards/";
        var endpoints = [['dashboards', url]];
        if (params.dashboardId) {
            endpoints.push(['selectedDashboard', "" + url + params.dashboardId + "/"]);
        }
        return endpoints;
    };
    OrgDashboards.prototype.getDashboards = function () {
        var dashboards = this.state.dashboards;
        return Array.isArray(dashboards) ? dashboards : [];
    };
    OrgDashboards.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        var _b = this.props, params = _b.params, organization = _b.organization;
        if (params.dashboardId || stateKey === 'selectedDashboard') {
            return;
        }
        // If we don't have a selected dashboard, and one isn't going to arrive
        // we can redirect to the first dashboard in the list.
        var dashboardId = data.length ? data[0].id : 'default-overview';
        var url = "/organizations/" + organization.slug + "/dashboards/" + dashboardId + "/";
        browserHistory.replace({ pathname: url });
    };
    OrgDashboards.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        var _b = this.state, selectedDashboard = _b.selectedDashboard, error = _b.error;
        return (<PageContent>
        <LightWeightNoProjectMessage organization={organization}>
          {children({
            error: error,
            dashboard: selectedDashboard,
            dashboards: this.getDashboards(),
            reloadData: this.reloadData.bind(this),
        })}
        </LightWeightNoProjectMessage>
      </PageContent>);
    };
    OrgDashboards.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        if (notFound) {
            return <NotFound />;
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    OrgDashboards.prototype.renderComponent = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        if (!organization.features.includes('dashboards-v2')) {
            // Redirect to Dashboards v1
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/dashboards/",
                query: __assign({}, location.query),
            });
            return null;
        }
        return (<SentryDocumentTitle title={t('Dashboards')} objSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </SentryDocumentTitle>);
    };
    return OrgDashboards;
}(AsyncComponent));
export default OrgDashboards;
//# sourceMappingURL=orgDashboards.jsx.map