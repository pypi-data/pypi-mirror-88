import { __assign, __rest } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import IdBadge from 'app/components/idBadge';
import recreateRoute from 'app/utils/recreateRoute';
import withTeams from 'app/utils/withTeams';
import BreadcrumbDropdown from 'app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown';
import MenuItem from 'app/views/settings/components/settingsBreadcrumb/menuItem';
import { CrumbLink } from '.';
var TeamCrumb = function (_a) {
    var teams = _a.teams, params = _a.params, routes = _a.routes, route = _a.route, props = __rest(_a, ["teams", "params", "routes", "route"]);
    var team = teams.find(function (_a) {
        var slug = _a.slug;
        return slug === params.teamId;
    });
    var hasMenu = teams.length > 1;
    if (!team) {
        return null;
    }
    return (<BreadcrumbDropdown name={<CrumbLink to={recreateRoute(route, {
        routes: routes,
        params: __assign(__assign({}, params), { teamId: team.slug }),
    })}>
          <IdBadge avatarSize={18} team={team}/>
        </CrumbLink>} onSelect={function (item) {
        browserHistory.push(recreateRoute('', {
            routes: routes,
            params: __assign(__assign({}, params), { teamId: item.value }),
        }));
    }} hasMenu={hasMenu} route={route} items={teams.map(function (teamItem, index) { return ({
        index: index,
        value: teamItem.slug,
        label: (<MenuItem>
            <IdBadge team={teamItem}/>
          </MenuItem>),
    }); })} {...props}/>);
};
export { TeamCrumb };
export default withTeams(TeamCrumb);
//# sourceMappingURL=teamCrumb.jsx.map