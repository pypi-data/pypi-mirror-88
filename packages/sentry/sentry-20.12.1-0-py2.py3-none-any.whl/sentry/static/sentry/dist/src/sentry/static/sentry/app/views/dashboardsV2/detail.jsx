import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { createDashboard, deleteDashboard, updateDashboard, } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import NotFound from 'app/components/errors/notFound';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import Controls from './controls';
import Dashboard from './dashboard';
import { EMPTY_DASHBOARD } from './data';
import OrgDashboards from './orgDashboards';
import DashboardTitle from './title';
import { cloneDashboard } from './utils';
var UNSAVED_MESSAGE = t('You have unsaved changes are you sure you want to leave?');
var DashboardDetail = /** @class */ (function (_super) {
    __extends(DashboardDetail, _super);
    function DashboardDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dashboardState: 'view',
            modifiedDashboard: null,
        };
        _this.onEdit = function (dashboard) { return function () {
            if (!dashboard) {
                return;
            }
            _this.setState({
                dashboardState: 'edit',
                modifiedDashboard: cloneDashboard(dashboard),
            });
        }; };
        _this.onRouteLeave = function () {
            if (_this.state.dashboardState !== 'view') {
                return UNSAVED_MESSAGE;
            }
            // eslint-disable-next-line consistent-return
            return;
        };
        _this.onUnload = function (event) {
            if (_this.state.dashboardState === 'view') {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        _this.onCreate = function () {
            _this.setState({
                dashboardState: 'create',
                modifiedDashboard: cloneDashboard(EMPTY_DASHBOARD),
            });
        };
        _this.onCancel = function () {
            _this.setState({
                dashboardState: 'view',
                modifiedDashboard: null,
            });
        };
        _this.onDelete = function (dashboard) { return function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            deleteDashboard(api, organization.slug, dashboard.id).then(function () {
                addSuccessMessage(t('Dashboard deleted'));
                browserHistory.replace({
                    pathname: "/organizations/" + organization.slug + "/dashboards/",
                    query: {},
                });
            });
        }; };
        _this.onCommit = function (_a) {
            var dashboard = _a.dashboard, reloadData = _a.reloadData;
            return function () {
                var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
                var _b = _this.state, dashboardState = _b.dashboardState, modifiedDashboard = _b.modifiedDashboard;
                switch (dashboardState) {
                    case 'create': {
                        if (modifiedDashboard) {
                            createDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard created'));
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                // redirect to new dashboard
                                browserHistory.replace({
                                    pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                    query: __assign({}, location.query),
                                });
                            });
                        }
                        break;
                    }
                    case 'edit': {
                        if (modifiedDashboard) {
                            // only update the dashboard if there are changes
                            if (isEqual(dashboard, modifiedDashboard)) {
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                return;
                            }
                            updateDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard updated'));
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                if (dashboard && newDashboard.id !== dashboard.id) {
                                    browserHistory.replace({
                                        pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                        query: __assign({}, location.query),
                                    });
                                    return;
                                }
                                reloadData();
                            });
                            return;
                        }
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                    case 'view':
                    default: {
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                }
            };
        };
        _this.onWidgetChange = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (prevState) {
                return __assign(__assign({}, prevState), { modifiedDashboard: __assign(__assign({}, modifiedDashboard), { widgets: widgets }) });
            });
        };
        _this.setModifiedDashboard = function (dashboard) {
            _this.setState({
                modifiedDashboard: dashboard,
            });
        };
        return _this;
    }
    DashboardDetail.prototype.componentDidMount = function () {
        var _a = this.props, route = _a.route, router = _a.router;
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.componentWillUnmount = function () {
        window.removeEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, location = _a.location, params = _a.params, organization = _a.organization;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        return (<GlobalSelectionHeader skipLoadLastUsed={organization.features.includes('global-views')}>
        <OrgDashboards api={api} location={location} params={params} organization={organization}>
          {function (_a) {
            var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
            return (<React.Fragment>
                <StyledPageHeader>
                  <DashboardTitle dashboard={modifiedDashboard || dashboard} onUpdate={_this.setModifiedDashboard} isEditing={dashboardState !== 'view'}/>
                  <Controls organization={organization} dashboards={dashboards} dashboard={dashboard} onEdit={_this.onEdit(dashboard)} onCreate={_this.onCreate} onCancel={_this.onCancel} onCommit={_this.onCommit({ dashboard: dashboard, reloadData: reloadData })} onDelete={_this.onDelete(dashboard)} dashboardState={dashboardState}/>
                </StyledPageHeader>
                {error ? (<NotFound />) : dashboard ? (<Dashboard dashboard={modifiedDashboard || dashboard} organization={organization} isEditing={dashboardState === 'edit' || dashboardState === 'create'} onUpdate={_this.onWidgetChange}/>) : (<LoadingIndicator />)}
              </React.Fragment>);
        }}
        </OrgDashboards>
      </GlobalSelectionHeader>);
    };
    return DashboardDetail;
}(React.Component));
var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n  white-space: nowrap;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(1));
export default withApi(withOrganization(DashboardDetail));
var templateObject_1;
//# sourceMappingURL=detail.jsx.map