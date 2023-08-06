import { __extends } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
import DashboardsV1 from 'app/views/dashboards';
var DashboardsV2Container = /** @class */ (function (_super) {
    __extends(DashboardsV2Container, _super);
    function DashboardsV2Container() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderNoAccess = function () {
            var children = _this.props.children;
            return <DashboardsV1>{children}</DashboardsV1>;
        };
        return _this;
    }
    DashboardsV2Container.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature features={['dashboards-v2']} requireAll={false} organization={organization} renderDisabled={this.renderNoAccess}>
        {children}
      </Feature>);
    };
    return DashboardsV2Container;
}(React.Component));
export default withOrganization(DashboardsV2Container);
//# sourceMappingURL=index.jsx.map