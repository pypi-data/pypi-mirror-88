import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import PropTypes from 'prop-types';
import Reflux from 'reflux';
import SettingsBreadcrumbActions from 'app/actions/settingsBreadcrumbActions';
import Link from 'app/components/links/link';
import SentryTypes from 'app/sentryTypes';
import SettingsBreadcrumbStore from 'app/stores/settingsBreadcrumbStore';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import recreateRoute from 'app/utils/recreateRoute';
import Crumb from 'app/views/settings/components/settingsBreadcrumb/crumb';
import Divider from 'app/views/settings/components/settingsBreadcrumb/divider';
import OrganizationCrumb from 'app/views/settings/components/settingsBreadcrumb/organizationCrumb';
import ProjectCrumb from 'app/views/settings/components/settingsBreadcrumb/projectCrumb';
import TeamCrumb from 'app/views/settings/components/settingsBreadcrumb/teamCrumb';
var MENUS = {
    Organization: OrganizationCrumb,
    Project: ProjectCrumb,
    Team: TeamCrumb,
};
var SettingsBreadcrumb = /** @class */ (function (_super) {
    __extends(SettingsBreadcrumb, _super);
    function SettingsBreadcrumb() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsBreadcrumb.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.routes === prevProps.routes) {
            return;
        }
        SettingsBreadcrumbActions.trimMappings(this.props.routes);
    };
    SettingsBreadcrumb.prototype.render = function () {
        var _a = this.props, className = _a.className, routes = _a.routes, params = _a.params, pathMap = _a.pathMap;
        var lastRouteIndex = routes.map(function (r) { return !!r.name; }).lastIndexOf(true);
        return (<Breadcrumbs className={className}>
        {routes.map(function (route, i) {
            if (!route.name) {
                return null;
            }
            var pathTitle = pathMap[getRouteStringFromRoutes(routes.slice(0, i + 1))];
            var isLast = i === lastRouteIndex;
            var createMenu = MENUS[route.name];
            var Menu = typeof createMenu === 'function' && createMenu;
            var hasMenu = !!Menu;
            var CrumbPicker = hasMenu
                ? Menu
                : function () { return (<Crumb>
                  <CrumbLink to={recreateRoute(route, { routes: routes, params: params })}>
                    {pathTitle || route.name}{' '}
                  </CrumbLink>
                  <Divider isLast={isLast}/>
                </Crumb>); };
            return (<CrumbPicker key={route.name + ":" + route.path} routes={routes} params={params} route={route} isLast={isLast}/>);
        })}
      </Breadcrumbs>);
    };
    SettingsBreadcrumb.propTypes = {
        routes: PropTypes.array,
        // pathMap maps stringifed routes to a breadcrumb title. This property is
        // provided by the SettingsBreadcrumbStore.
        pathMap: PropTypes.object,
    };
    SettingsBreadcrumb.contextTypes = {
        organization: SentryTypes.Organization,
    };
    SettingsBreadcrumb.defaultProps = {
        pathMap: {},
    };
    return SettingsBreadcrumb;
}(React.Component));
export default createReactClass({
    displayName: 'ConnectedSettingsBreadcrumb',
    mixins: [Reflux.connect(SettingsBreadcrumbStore, 'pathMap')],
    render: function () {
        return <SettingsBreadcrumb {...this.props} {...this.state}/>;
    },
});
var CrumbLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  display: block;\n\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.blue300; }, function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
export { CrumbLink };
var Breadcrumbs = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map