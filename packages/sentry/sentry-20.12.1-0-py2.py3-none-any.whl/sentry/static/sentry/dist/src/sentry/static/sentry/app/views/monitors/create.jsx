import { __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import AsyncView from 'app/views/asyncView';
import MonitorForm from './monitorForm';
var CreateMonitor = /** @class */ (function (_super) {
    __extends(CreateMonitor, _super);
    function CreateMonitor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onSubmitSuccess = function (data) {
            browserHistory.push("/organizations/" + _this.props.params.orgId + "/monitors/" + data.id + "/");
        };
        return _this;
    }
    CreateMonitor.prototype.getTitle = function () {
        return "Monitors - " + this.props.params.orgId;
    };
    CreateMonitor.prototype.renderBody = function () {
        return (<React.Fragment>
        <h1>New Monitor</h1>
        <MonitorForm apiMethod="POST" apiEndpoint={"/organizations/" + this.props.params.orgId + "/monitors/"} onSubmitSuccess={this.onSubmitSuccess}/>
      </React.Fragment>);
    };
    return CreateMonitor;
}(AsyncView));
export default CreateMonitor;
//# sourceMappingURL=create.jsx.map