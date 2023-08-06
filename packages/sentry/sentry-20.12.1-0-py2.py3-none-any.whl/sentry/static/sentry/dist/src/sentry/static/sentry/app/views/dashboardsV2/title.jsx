import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import InlineInput from 'app/components/inputInline';
import { t } from 'app/locale';
import space from 'app/styles/space';
var DashboardTitle = /** @class */ (function (_super) {
    __extends(DashboardTitle, _super);
    function DashboardTitle() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.refInput = React.createRef();
        _this.onBlur = function (event) {
            var nextDashboardTitle = (event.target.value || '').trim().slice(0, 255).trim();
            if (!nextDashboardTitle) {
                addErrorMessage(t('Please set the title for this dashboard'));
                // Help our users re-focus so they cannot run away from this problem
                if (_this.refInput.current) {
                    _this.refInput.current.focus();
                }
                return;
            }
            var _a = _this.props, dashboard = _a.dashboard, onUpdate = _a.onUpdate;
            if (!dashboard) {
                return;
            }
            event.target.innerText = nextDashboardTitle;
            onUpdate(__assign(__assign({}, dashboard), { title: nextDashboardTitle }));
        };
        return _this;
    }
    DashboardTitle.prototype.render = function () {
        var _a = this.props, dashboard = _a.dashboard, isEditing = _a.isEditing;
        if (!dashboard) {
            return <Container>{t('Dashboards')}</Container>;
        }
        if (!isEditing) {
            return <Container>{dashboard.title}</Container>;
        }
        return (<Container>
        <StyledInlineInput name="dashboard-title" ref={this.refInput} value={dashboard.title} onBlur={this.onBlur}/>
      </Container>);
    };
    return DashboardTitle;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledInlineInput = styled(React.forwardRef(function (props, ref) { return (<InlineInput {...props} ref={ref}/>); }))(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  overflow-wrap: anywhere;\n  white-space: normal;\n"], ["\n  overflow-wrap: anywhere;\n  white-space: normal;\n"])));
export default DashboardTitle;
var templateObject_1, templateObject_2;
//# sourceMappingURL=title.jsx.map