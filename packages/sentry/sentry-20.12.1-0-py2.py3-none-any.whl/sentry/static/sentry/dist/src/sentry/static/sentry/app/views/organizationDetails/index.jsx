import { __extends } from "tslib";
import React, { Component } from 'react';
import { browserHistory } from 'react-router';
import { switchOrganization } from 'app/actionCreators/organizations';
import AlertActions from 'app/actions/alertActions';
import { Client } from 'app/api';
import Button from 'app/components/button';
import ErrorBoundary from 'app/components/errorBoundary';
import Footer from 'app/components/footer';
import NarrowLayout from 'app/components/narrowLayout';
import { t, tct } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import OrganizationContext from 'app/views/organizationContext';
function DeletionInProgress(_a) {
    var organization = _a.organization;
    return (<NarrowLayout>
      <p>
        {tct('The [organization] organization is currently in the process of being deleted from Sentry.', {
        organization: <strong>{organization.slug}</strong>,
    })}
      </p>
    </NarrowLayout>);
}
var DeletionPending = /** @class */ (function (_super) {
    __extends(DeletionPending, _super);
    function DeletionPending() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { submitInProgress: false };
        _this.api = new Client();
        _this.onRestore = function () {
            if (_this.state.submitInProgress) {
                return;
            }
            _this.setState({ submitInProgress: true });
            _this.api.request("/organizations/" + _this.props.organization.slug + "/", {
                method: 'PUT',
                data: { cancelDeletion: true },
                success: function () {
                    window.location.reload();
                },
                error: function () {
                    AlertActions.addAlert({
                        message: 'We were unable to restore this organization. Please try again or contact support.',
                        type: 'error',
                    });
                    _this.setState({ submitInProgress: false });
                },
            });
        };
        return _this;
    }
    DeletionPending.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    DeletionPending.prototype.render = function () {
        var organization = this.props.organization;
        var access = new Set(organization.access);
        return (<NarrowLayout>
        <h3>{t('Deletion Scheduled')}</h3>
        <p>
          {tct('The [organization] organization is currently scheduled for deletion.', {
            organization: <strong>{organization.slug}</strong>,
        })}
        </p>

        {access.has('org:admin') ? (<div>
            <p>
              {t('Would you like to cancel this process and restore the organization back to the original state?')}
            </p>
            <p>
              <Button priority="primary" onClick={this.onRestore} disabled={this.state.submitInProgress}>
                {t('Restore Organization')}
              </Button>
            </p>
          </div>) : (<p>
            {t('If this is a mistake, contact an organization owner and ask them to restore this organization.')}
          </p>)}
        <p>
          <small>
            {t("Note: Restoration is available until the process begins. Once it does, there's no recovering the data that has been removed.")}
          </small>
        </p>
      </NarrowLayout>);
    };
    return DeletionPending;
}(Component));
var OrganizationDetailsBody = /** @class */ (function (_super) {
    __extends(OrganizationDetailsBody, _super);
    function OrganizationDetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationDetailsBody.prototype.render = function () {
        var organization = this.context.organization;
        if (organization && organization.status) {
            if (organization.status.id === 'pending_deletion') {
                return <DeletionPending organization={organization}/>;
            }
            else if (organization.status.id === 'deletion_in_progress') {
                return <DeletionInProgress organization={organization}/>;
            }
        }
        return (<React.Fragment>
        <ErrorBoundary>{this.props.children}</ErrorBoundary>
        <Footer />
      </React.Fragment>);
    };
    OrganizationDetailsBody.contextTypes = {
        organization: SentryTypes.Organization,
    };
    return OrganizationDetailsBody;
}(Component));
var OrganizationDetails = /** @class */ (function (_super) {
    __extends(OrganizationDetails, _super);
    function OrganizationDetails() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationDetails.prototype.componentDidMount = function () {
        var routes = this.props.routes;
        var isOldRoute = getRouteStringFromRoutes(routes) === '/:orgId/';
        if (isOldRoute) {
            browserHistory.replace("/organizations/" + this.props.params.orgId + "/");
        }
    };
    OrganizationDetails.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.params &&
            this.props.params &&
            prevProps.params.orgId !== this.props.params.orgId) {
            switchOrganization();
        }
    };
    OrganizationDetails.prototype.render = function () {
        return (<OrganizationContext includeSidebar useLastOrganization {...this.props}>
        <OrganizationDetailsBody {...this.props}>
          {this.props.children}
        </OrganizationDetailsBody>
      </OrganizationContext>);
    };
    return OrganizationDetails;
}(Component));
export default OrganizationDetails;
export function LightWeightOrganizationDetails(props) {
    return <OrganizationDetails detailed={false} {...props}/>;
}
//# sourceMappingURL=index.jsx.map