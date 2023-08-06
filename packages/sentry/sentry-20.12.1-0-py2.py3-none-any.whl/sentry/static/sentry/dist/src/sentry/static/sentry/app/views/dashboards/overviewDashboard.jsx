import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import DashboardDetail from 'app/views/dashboardsV2/detail';
import overviewDashboard from './data/dashboards/overviewDashboard';
import Dashboard from './dashboard';
var OverviewDashboard = /** @class */ (function (_super) {
    __extends(OverviewDashboard, _super);
    function OverviewDashboard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OverviewDashboard.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return [['releases', "/organizations/" + orgId + "/releases/"]];
    };
    OverviewDashboard.prototype.getTitle = function () {
        var params = this.props.params;
        var orgId = params.orgId;
        return t('Dashboard') + " - " + orgId;
    };
    OverviewDashboard.prototype.renderLoading = function () {
        // We don't want a loading state
        return this.renderBody();
    };
    OverviewDashboard.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases;
        if (!releases) {
            return null;
        }
        // Passing the rest of `this.props` to `<Dashboard>` for tests
        var _b = this.props, router = _b.router, props = __rest(_b, ["router"]);
        return (<Dashboard releases={releases} releasesLoading={loading} router={router} {...overviewDashboard} {...props}/>);
    };
    return OverviewDashboard;
}(AsyncView));
function DashboardLanding(props) {
    var organization = props.organization, params = props.params, restProps = __rest(props, ["organization", "params"]);
    var showDashboardV2 = organization.features.includes('dashboards-v2');
    if (showDashboardV2) {
        var updatedParams = __assign(__assign({}, params), { dashboardId: '' });
        return <DashboardDetail {...restProps} params={updatedParams}/>;
    }
    return <OverviewDashboard {...restProps} params={params}/>;
}
export default withOrganization(DashboardLanding);
//# sourceMappingURL=overviewDashboard.jsx.map