import { __extends } from "tslib";
import React from 'react';
import { fetchOrganizationDetails } from 'app/actionCreators/organizations';
import SentryTypes from 'app/sentryTypes';
import withLatestContext from 'app/utils/withLatestContext';
import AccountSettingsNavigation from 'app/views/settings/account/accountSettingsNavigation';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
var AccountSettingsLayout = /** @class */ (function (_super) {
    __extends(AccountSettingsLayout, _super);
    function AccountSettingsLayout() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountSettingsLayout.prototype.getChildContext = function () {
        return {
            organization: this.props.organization,
        };
    };
    AccountSettingsLayout.prototype.componentDidUpdate = function (prevProps) {
        var organization = this.props.organization;
        if (prevProps.organization === organization) {
            return;
        }
        // if there is no org in context, SidebarDropdown uses an org from `withLatestContext`
        // (which queries the org index endpoint instead of org details)
        // and does not have `access` info
        if (organization && typeof organization.access === 'undefined') {
            fetchOrganizationDetails(organization.slug, {
                setActive: true,
                loadProjects: true,
            });
        }
    };
    AccountSettingsLayout.prototype.render = function () {
        return (<SettingsLayout {...this.props} renderNavigation={function () { return <AccountSettingsNavigation />; }}>
        {this.props.children}
      </SettingsLayout>);
    };
    AccountSettingsLayout.childContextTypes = {
        organization: SentryTypes.Organization,
    };
    return AccountSettingsLayout;
}(React.Component));
export default withLatestContext(AccountSettingsLayout);
//# sourceMappingURL=accountSettingsLayout.jsx.map