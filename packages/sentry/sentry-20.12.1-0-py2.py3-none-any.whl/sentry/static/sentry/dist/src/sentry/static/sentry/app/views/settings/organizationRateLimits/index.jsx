import React from 'react';
import withOrganization from 'app/utils/withOrganization';
import OrganizationRateLimits from './organizationRateLimits';
var OrganizationRateLimitsContainer = function (props) { return (!props.organization ? null : <OrganizationRateLimits {...props}/>); };
export default withOrganization(OrganizationRateLimitsContainer);
//# sourceMappingURL=index.jsx.map