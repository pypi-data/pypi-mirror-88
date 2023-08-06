import { __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import KeySettings from 'app/views/settings/project/projectKeys/details/keySettings';
import KeyStats from 'app/views/settings/project/projectKeys/details/keyStats';
var ProjectKeyDetails = /** @class */ (function (_super) {
    __extends(ProjectKeyDetails, _super);
    function ProjectKeyDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            browserHistory.push("/" + orgId + "/" + projectId + "/settings/keys/");
        };
        return _this;
    }
    ProjectKeyDetails.prototype.getTitle = function () {
        return t('Key Details');
    };
    ProjectKeyDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, keyId = _a.keyId, orgId = _a.orgId, projectId = _a.projectId;
        return [['data', "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/"]];
    };
    ProjectKeyDetails.prototype.renderBody = function () {
        var data = this.state.data;
        var params = this.props.params;
        return (<div data-test-id="key-details">
        <SettingsPageHeader title={t('Key Details')}/>
        <PermissionAlert />

        <KeyStats api={this.api} params={params}/>

        <KeySettings api={this.api} params={params} data={data} onRemove={this.handleRemove}/>
      </div>);
    };
    return ProjectKeyDetails;
}(AsyncView));
export default ProjectKeyDetails;
//# sourceMappingURL=index.jsx.map