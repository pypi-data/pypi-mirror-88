import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import IdBadge from 'app/components/idBadge';
import recreateRoute from 'app/utils/recreateRoute';
import withLatestContext from 'app/utils/withLatestContext';
import BreadcrumbDropdown from 'app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown';
import findFirstRouteWithoutRouteParam from 'app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam';
import MenuItem from 'app/views/settings/components/settingsBreadcrumb/menuItem';
import { CrumbLink } from '.';
var OrganizationCrumb = function (_a) {
    var organization = _a.organization, organizations = _a.organizations, params = _a.params, routes = _a.routes, route = _a.route, props = __rest(_a, ["organization", "organizations", "params", "routes", "route"]);
    var handleSelect = function (item) {
        // If we are currently in a project context, and we're attempting to switch organizations,
        // then we need to default to index route (e.g. `route`)
        //
        // Otherwise, find the last route without a router param
        // e.g. if you are on API details, we want the API listing
        // This fails if our route tree is not nested
        var hasProjectParam = !!params.projectId;
        var destination = hasProjectParam
            ? route
            : findFirstRouteWithoutRouteParam(routes.slice(routes.indexOf(route)));
        // It's possible there is no route without route params (e.g. organization settings index),
        // in which case, we can use the org settings index route (e.g. `route`)
        if (!hasProjectParam && typeof destination === 'undefined') {
            destination = route;
        }
        if (destination === undefined) {
            return;
        }
        browserHistory.push(recreateRoute(destination, {
            routes: routes,
            params: __assign(__assign({}, params), { orgId: item.value }),
        }));
    };
    if (!organization) {
        return null;
    }
    var hasMenu = organizations.length > 1;
    return (<BreadcrumbDropdown name={<CrumbLink to={recreateRoute(route, {
        routes: routes,
        params: __assign(__assign({}, params), { orgId: organization.slug }),
    })}>
          <BadgeWrapper>
            <IdBadge avatarSize={18} organization={organization}/>
          </BadgeWrapper>
        </CrumbLink>} onSelect={handleSelect} hasMenu={hasMenu} route={route} items={organizations.map(function (org, index) { return ({
        index: index,
        value: org.slug,
        label: (<MenuItem>
            <IdBadge organization={org}/>
          </MenuItem>),
    }); })} {...props}/>);
};
var BadgeWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
export { OrganizationCrumb };
export default withLatestContext(OrganizationCrumb);
var templateObject_1;
//# sourceMappingURL=organizationCrumb.jsx.map