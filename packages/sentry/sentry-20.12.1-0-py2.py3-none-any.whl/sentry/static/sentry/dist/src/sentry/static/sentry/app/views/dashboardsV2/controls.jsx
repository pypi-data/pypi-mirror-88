import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import SelectControl from 'app/components/forms/selectControl';
import { IconAdd, IconEdit } from 'app/icons';
import { t } from 'app/locale';
var Controls = /** @class */ (function (_super) {
    __extends(Controls, _super);
    function Controls() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Controls.prototype.render = function () {
        var _this = this;
        var _a = this.props, dashboardState = _a.dashboardState, dashboards = _a.dashboards, dashboard = _a.dashboard, onEdit = _a.onEdit, onCreate = _a.onCreate, onCancel = _a.onCancel, onCommit = _a.onCommit, onDelete = _a.onDelete;
        var cancelButton = (<Button data-test-id="dashboard-cancel" onClick={function (e) {
            e.preventDefault();
            onCancel();
        }}>
        {t('Cancel')}
      </Button>);
        if (dashboardState === 'edit') {
            return (<ButtonBar gap={1} key="edit-controls">
          {cancelButton}
          <Button data-test-id="dashboard-delete" onClick={function (e) {
                e.preventDefault();
                onDelete();
            }} priority="danger">
            {t('Delete')}
          </Button>
          <Button data-test-id="dashboard-commit" onClick={function (e) {
                e.preventDefault();
                onCommit();
            }} priority="primary">
            {t('Finish Editing')}
          </Button>
        </ButtonBar>);
        }
        if (dashboardState === 'create') {
            return (<ButtonBar gap={1} key="create-controls">
          {cancelButton}
          <Button data-test-id="dashboard-commit" onClick={function (e) {
                e.preventDefault();
                onCommit();
            }} priority="primary" icon={<IconAdd size="xs" isCircled/>}>
            {t('Create Dashboard')}
          </Button>
        </ButtonBar>);
        }
        var dropdownOptions = dashboards.map(function (item) {
            return {
                label: item.title,
                value: item,
            };
        });
        var currentOption = undefined;
        if (dashboard) {
            currentOption = {
                label: dashboard.title,
                value: dashboard,
            };
        }
        else if (dropdownOptions.length) {
            currentOption = dropdownOptions[0];
        }
        return (<ButtonBar gap={1} key="controls">
        <DashboardSelect>
          <SelectControl key="select" name="parameter" placeholder={t('Select Dashboard')} options={dropdownOptions} value={currentOption} onChange={function (_a) {
            var value = _a.value;
            var organization = _this.props.organization;
            browserHistory.push({
                pathname: "/organizations/" + organization.slug + "/dashboards/" + value.id + "/",
                // TODO(mark) should this retain global selection?
                query: {},
            });
        }}/>
        </DashboardSelect>
        <Button data-test-id="dashboard-edit" onClick={function (e) {
            e.preventDefault();
            onEdit();
        }} icon={<IconEdit size="xs"/>}>
          {t('Edit')}
        </Button>
        <Button data-test-id="dashboard-create" onClick={function (e) {
            e.preventDefault();
            onCreate();
        }} priority="primary" icon={<IconAdd size="xs" isCircled/>}>
          {t('Create Dashboard')}
        </Button>
      </ButtonBar>);
    };
    return Controls;
}(React.Component));
var DashboardSelect = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  min-width: 200px;\n  font-size: ", ";\n"], ["\n  min-width: 200px;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
export default Controls;
var templateObject_1;
//# sourceMappingURL=controls.jsx.map