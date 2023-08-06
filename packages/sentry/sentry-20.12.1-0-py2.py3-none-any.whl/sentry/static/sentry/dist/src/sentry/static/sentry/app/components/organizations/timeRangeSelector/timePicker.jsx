import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
var TimePicker = styled(/** @class */ (function (_super) {
    __extends(TimePicker, _super);
    function TimePicker() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            focused: false,
        };
        _this.handleFocus = function () {
            _this.setState({ focused: true });
        };
        _this.handleBlur = function () {
            _this.setState({ focused: false });
        };
        return _this;
    }
    TimePicker.prototype.shouldComponentUpdate = function () {
        // This is necessary because when a change event happens,
        // the change is propagated up to the dropdown. This causes
        // a re-render of this component which in turn causes the
        // input element to lose focus. To get around losing focus,
        // we prevent the component from updating when one of the
        // inputs has focus. This is okay because the inputs will
        // keep track of their own values so we do not have to keep
        // track of it.
        return !this.state.focused;
    };
    TimePicker.prototype.render = function () {
        var _a = this.props, className = _a.className, start = _a.start, end = _a.end, disabled = _a.disabled, onChangeStart = _a.onChangeStart, onChangeEnd = _a.onChangeEnd;
        return (<div className={classNames(className, 'rdrDateDisplay')}>
          <div>
            <Input type="time" key={start} defaultValue={start} className="rdrDateDisplayItem" data-test-id="startTime" disabled={disabled} onFocus={this.handleFocus} onBlur={this.handleBlur} onChange={onChangeStart}/>
          </div>

          <div>
            <Input type="time" defaultValue={end} key={end} className="rdrDateDisplayItem" data-test-id="endTime" disabled={disabled} onFocus={this.handleFocus} onBlur={this.handleBlur} onChange={onChangeEnd}/>
          </div>
        </div>);
    };
    return TimePicker;
}(React.Component)))(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  &.rdrDateDisplay {\n    display: grid;\n    background: transparent;\n    grid-template-columns: 48% 48%;\n    grid-column-gap: 4%;\n    align-items: center;\n    font-size: 0.875em;\n    color: ", ";\n    width: 70%;\n    padding: 0;\n  }\n"], ["\n  &.rdrDateDisplay {\n    display: grid;\n    background: transparent;\n    grid-template-columns: 48% 48%;\n    grid-column-gap: 4%;\n    align-items: center;\n    font-size: 0.875em;\n    color: ", ";\n    width: 70%;\n    padding: 0;\n  }\n"])), function (p) { return p.theme.subText; });
var Input = styled('input')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  &.rdrDateDisplayItem {\n    width: 100%;\n    padding-left: 5%;\n    background: ", ";\n    border: 1px solid ", ";\n    color: ", ";\n    box-shadow: none;\n  }\n"], ["\n  &.rdrDateDisplayItem {\n    width: 100%;\n    padding-left: 5%;\n    background: ", ";\n    border: 1px solid ", ";\n    color: ", ";\n    box-shadow: none;\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.gray300; });
export default TimePicker;
var templateObject_1, templateObject_2;
//# sourceMappingURL=timePicker.jsx.map