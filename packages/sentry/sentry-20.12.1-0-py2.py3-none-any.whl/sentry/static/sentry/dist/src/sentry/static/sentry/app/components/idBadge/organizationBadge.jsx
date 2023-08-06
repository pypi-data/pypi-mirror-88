import { __rest } from "tslib";
import React from 'react';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
import BaseBadge from 'app/components/idBadge/baseBadge';
var OrganizationBadge = function (_a) {
    var _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, organization = _a.organization, props = __rest(_a, ["hideOverflow", "organization"]);
    return (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>{organization.slug}</BadgeDisplayName>} organization={organization} {...props}/>);
};
export default OrganizationBadge;
//# sourceMappingURL=organizationBadge.jsx.map