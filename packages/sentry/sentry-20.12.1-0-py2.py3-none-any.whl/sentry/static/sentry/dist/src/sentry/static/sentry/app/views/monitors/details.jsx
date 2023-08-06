import { __assign, __extends } from "tslib";
import React from 'react';
import { Panel, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import MonitorCheckIns from './monitorCheckIns';
import MonitorHeader from './monitorHeader';
import MonitorIssues from './monitorIssues';
import MonitorStats from './monitorStats';
var MonitorDetails = /** @class */ (function (_super) {
    __extends(MonitorDetails, _super);
    function MonitorDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onUpdate = function (data) {
            return _this.setState(function (state) { return ({ monitor: __assign(__assign({}, state.monitor), data) }); });
        };
        return _this;
    }
    MonitorDetails.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [['monitor', "/monitors/" + params.monitorId + "/", { query: location.query }]];
    };
    MonitorDetails.prototype.getTitle = function () {
        if (this.state.monitor) {
            return this.state.monitor.name + " - Monitors - " + this.props.params.orgId;
        }
        return "Monitors - " + this.props.params.orgId;
    };
    MonitorDetails.prototype.renderBody = function () {
        var monitor = this.state.monitor;
        if (monitor === null) {
            return null;
        }
        return (<React.Fragment>
        <MonitorHeader monitor={monitor} orgId={this.props.params.orgId} onUpdate={this.onUpdate}/>

        <MonitorStats monitor={monitor}/>

        <Panel style={{ paddingBottom: 0 }}>
          <PanelHeader>{t('Related Issues')}</PanelHeader>

          <MonitorIssues monitor={monitor} orgId={this.props.params.orgId}/>
        </Panel>

        <Panel>
          <PanelHeader>{t('Recent Check-ins')}</PanelHeader>

          <MonitorCheckIns monitor={monitor}/>
        </Panel>
      </React.Fragment>);
    };
    return MonitorDetails;
}(AsyncView));
export default MonitorDetails;
//# sourceMappingURL=details.jsx.map