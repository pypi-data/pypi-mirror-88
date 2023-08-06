import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openAddDashboardWidgetModal } from 'app/actionCreators/modal';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import { IconAdd } from 'app/icons';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import WidgetCard from './widgetCard';
var Dashboard = /** @class */ (function (_super) {
    __extends(Dashboard, _super);
    function Dashboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleStartAdd = function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
            });
        };
        _this.handleAddComplete = function (widget) {
            _this.props.onUpdate(__spread(_this.props.dashboard.widgets, [widget]));
        };
        _this.handleUpdateComplete = function (index) { return function (nextWidget) {
            var nextList = __spread(_this.props.dashboard.widgets);
            nextList[index] = nextWidget;
            _this.props.onUpdate(nextList);
        }; };
        _this.handleDeleteWidget = function (index) { return function () {
            var nextList = __spread(_this.props.dashboard.widgets);
            nextList.splice(index, 1);
            _this.props.onUpdate(nextList);
        }; };
        _this.handleEditWidget = function (widget, index) { return function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                widget: widget,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
                onUpdateWidget: _this.handleUpdateComplete(index),
            });
        }; };
        return _this;
    }
    Dashboard.prototype.componentDidMount = function () {
        var isEditing = this.props.isEditing;
        // Load organization tags when in edit mode.
        if (isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.componentDidUpdate = function (prevProps) {
        var isEditing = this.props.isEditing;
        // Load organization tags when going into edit mode.
        // We use tags on the add widget modal.
        if (prevProps.isEditing !== isEditing && isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.fetchTags = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
    };
    Dashboard.prototype.renderWidget = function (widget, index) {
        var isEditing = this.props.isEditing;
        // TODO add drag state and drag re-sorting.
        return (<WidgetWrapper key={widget.id + ":" + index}>
        <WidgetCard widget={widget} isEditing={isEditing} onDelete={this.handleDeleteWidget(index)} onEdit={this.handleEditWidget(widget, index)}/>
      </WidgetWrapper>);
    };
    Dashboard.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEditing = _a.isEditing, dashboard = _a.dashboard;
        return (<WidgetContainer>
        {dashboard.widgets.map(function (widget, i) { return _this.renderWidget(widget, i); })}
        {isEditing && (<WidgetWrapper key="add">
            <AddWidgetWrapper key="add" onClick={this.handleStartAdd}>
              <IconAdd size="lg" isCircled color="inactive"/>
            </AddWidgetWrapper>
          </WidgetWrapper>)}
      </WidgetContainer>);
    };
    return Dashboard;
}(React.Component));
export default withApi(withGlobalSelection(Dashboard));
var WidgetContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-gap: ", ";\n"])), space(2));
var WidgetWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var AddWidgetWrapper = styled('a')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n  min-height: 200px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  width: 100%;\n  height: 100%;\n  min-height: 200px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dashboard.jsx.map