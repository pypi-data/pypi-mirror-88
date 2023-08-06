import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import IdBadge from 'app/components/idBadge';
import LoadingIndicator from 'app/components/loadingIndicator';
import space from 'app/styles/space';
import recreateRoute from 'app/utils/recreateRoute';
import replaceRouterParams from 'app/utils/replaceRouterParams';
import withLatestContext from 'app/utils/withLatestContext';
import withProjects from 'app/utils/withProjects';
import BreadcrumbDropdown from 'app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown';
import findFirstRouteWithoutRouteParam from 'app/views/settings/components/settingsBreadcrumb/findFirstRouteWithoutRouteParam';
import MenuItem from 'app/views/settings/components/settingsBreadcrumb/menuItem';
import { CrumbLink } from '.';
var ProjectCrumb = function (_a) {
    var latestOrganization = _a.organization, latestProject = _a.project, projects = _a.projects, params = _a.params, routes = _a.routes, route = _a.route, props = __rest(_a, ["organization", "project", "projects", "params", "routes", "route"]);
    var handleSelect = function (item) {
        // We have to make exceptions for routes like "Project Alerts Rule Edit" or "Client Key Details"
        // Since these models are project specific, we need to traverse up a route when switching projects
        //
        // we manipulate `routes` so that it doesn't include the current project's route
        // which, unlike the org version, does not start with a route param
        var returnTo = findFirstRouteWithoutRouteParam(routes.slice(routes.indexOf(route) + 1), route);
        if (returnTo === undefined) {
            return;
        }
        browserHistory.push(recreateRoute(returnTo, { routes: routes, params: __assign(__assign({}, params), { projectId: item.value }) }));
    };
    if (!latestOrganization) {
        return null;
    }
    if (!projects) {
        return null;
    }
    var hasMenu = projects && projects.length > 1;
    return (<BreadcrumbDropdown hasMenu={hasMenu} route={route} name={<ProjectName>
          {!latestProject ? (<LoadingIndicator mini/>) : (<CrumbLink to={replaceRouterParams('/settings/:orgId/projects/:projectId/', {
        orgId: latestOrganization.slug,
        projectId: latestProject.slug,
    })}>
              <IdBadge project={latestProject} avatarSize={18}/>
            </CrumbLink>)}
        </ProjectName>} onSelect={handleSelect} items={projects.map(function (project, index) { return ({
        index: index,
        value: project.slug,
        label: (<MenuItem>
            <IdBadge project={project} avatarProps={{ consistentWidth: true }} avatarSize={18}/>
          </MenuItem>),
    }); })} {...props}/>);
};
export { ProjectCrumb };
export default withProjects(withLatestContext(ProjectCrumb));
// Set height of crumb because of spinner
var SPINNER_SIZE = '24px';
var ProjectName = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n\n  .loading {\n    width: ", ";\n    height: ", ";\n    margin: 0 ", " 0 0;\n  }\n"], ["\n  display: flex;\n\n  .loading {\n    width: ", ";\n    height: ", ";\n    margin: 0 ", " 0 0;\n  }\n"])), SPINNER_SIZE, SPINNER_SIZE, space(0.25));
var templateObject_1;
//# sourceMappingURL=projectCrumb.jsx.map