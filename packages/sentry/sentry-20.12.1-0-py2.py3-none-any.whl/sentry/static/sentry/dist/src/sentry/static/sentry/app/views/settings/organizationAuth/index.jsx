import { __extends } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import OrganizationAuthList from './organizationAuthList';
var OrganizationAuth = /** @class */ (function (_super) {
    __extends(OrganizationAuth, _super);
    function OrganizationAuth() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleSendReminders = function (_provider) {
            _this.setState({ sendRemindersBusy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/send-reminders/", {
                method: 'POST',
                data: {},
                success: function () { return addSuccessMessage(t('Sent reminders to members')); },
                error: function () { return addErrorMessage(t('Failed to send reminders')); },
                complete: function () { return _this.setState({ sendRemindersBusy: false }); },
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleConfigure = function (provider) {
            _this.setState({ busy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/", {
                method: 'POST',
                data: { provider: provider, init: true },
                success: function (data) {
                    // Redirect to auth provider URL
                    if (data && data.auth_url) {
                        window.location.href = data.auth_url;
                    }
                },
                error: function () {
                    _this.setState({ busy: false });
                },
            });
        };
        /**
         * TODO(epurkhiser): This does not work right now as we still fallback to the
         * old SSO auth configuration page
         */
        _this.handleDisableProvider = function (provider) {
            _this.setState({ busy: true });
            _this.api.request("/organizations/" + _this.props.params.orgId + "/auth-provider/", {
                method: 'DELETE',
                data: { provider: provider },
                success: function () {
                    _this.setState({ provider: null, busy: false });
                },
                error: function () {
                    _this.setState({ busy: false });
                },
            });
        };
        return _this;
    }
    OrganizationAuth.prototype.UNSAFE_componentWillUpdate = function (_nextProps, nextState) {
        var access = this.props.organization.access;
        if (nextState.provider && access.includes('org:write')) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            window.location.assign("/organizations/" + this.props.params.orgId + "/auth/configure/");
        }
    };
    OrganizationAuth.prototype.getEndpoints = function () {
        return [
            ['providerList', "/organizations/" + this.props.params.orgId + "/auth-providers/"],
            ['provider', "/organizations/" + this.props.params.orgId + "/auth-provider/"],
        ];
    };
    OrganizationAuth.prototype.getTitle = function () {
        return routeTitleGen(t('Auth Settings'), this.props.organization.slug, false);
    };
    OrganizationAuth.prototype.renderBody = function () {
        var _a = this.state, providerList = _a.providerList, provider = _a.provider;
        if (providerList === null) {
            return null;
        }
        if (this.props.organization.access.includes('org:write') && provider) {
            // If SSO provider is configured, keep showing loading while we redirect
            // to django configuration view
            return this.renderLoading();
        }
        var activeProvider = providerList === null || providerList === void 0 ? void 0 : providerList.find(function (p) { return p.key === (provider === null || provider === void 0 ? void 0 : provider.key); });
        return (<OrganizationAuthList activeProvider={activeProvider} providerList={providerList}/>);
    };
    return OrganizationAuth;
}(AsyncView));
export default withOrganization(OrganizationAuth);
//# sourceMappingURL=index.jsx.map