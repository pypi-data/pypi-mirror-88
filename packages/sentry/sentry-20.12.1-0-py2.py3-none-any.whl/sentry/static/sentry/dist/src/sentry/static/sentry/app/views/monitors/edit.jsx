import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import AsyncView from 'app/views/asyncView';
import MonitorForm from './monitorForm';
var EditMonitor = /** @class */ (function (_super) {
    __extends(EditMonitor, _super);
    function EditMonitor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onUpdate = function (data) {
            return _this.setState(function (state) { return ({ monitor: __assign(__assign({}, state.monitor), data) }); });
        };
        _this.onSubmitSuccess = function (data) {
            return browserHistory.push("/organizations/" + _this.props.params.orgId + "/monitors/" + data.id + "/");
        };
        return _this;
    }
    EditMonitor.prototype.getEndpoints = function () {
        var params = this.props.params;
        return [['monitor', "/monitors/" + params.monitorId + "/"]];
    };
    EditMonitor.prototype.getTitle = function () {
        if (this.state.monitor) {
            return this.state.monitor.name + " - Monitors - " + this.props.params.orgId;
        }
        return "Monitors - " + this.props.params.orgId;
    };
    EditMonitor.prototype.renderBody = function () {
        var monitor = this.state.monitor;
        if (monitor === null) {
            return null;
        }
        return (<React.Fragment>
        <h1>Edit Monitor</h1>

        <MonitorForm monitor={monitor} apiMethod="PUT" apiEndpoint={"/monitors/" + monitor.id + "/"} onSubmitSuccess={this.onSubmitSuccess}/>
      </React.Fragment>);
    };
    return EditMonitor;
}(AsyncView));
export default EditMonitor;
//# sourceMappingURL=edit.jsx.map