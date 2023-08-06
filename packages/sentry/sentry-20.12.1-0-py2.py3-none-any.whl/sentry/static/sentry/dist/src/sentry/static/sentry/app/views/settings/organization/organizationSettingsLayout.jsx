import React from 'react';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
import OrganizationSettingsNavigation from 'app/views/settings/organization/organizationSettingsNavigation';
function OrganizationSettingsLayout(props) {
    return (<SettingsLayout {...props} renderNavigation={function () { return <OrganizationSettingsNavigation />; }}/>);
}
export default OrganizationSettingsLayout;
//# sourceMappingURL=organizationSettingsLayout.jsx.map