import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import Confirm from 'app/components/confirm';
import Switch from 'app/components/switch';
import InputField from 'app/views/settings/components/forms/inputField';
var BooleanField = /** @class */ (function (_super) {
    __extends(BooleanField, _super);
    function BooleanField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (value, onChange, onBlur, e) {
            // We need to toggle current value because Switch is not an input
            var newValue = _this.coerceValue(!value);
            onChange(newValue, e);
            onBlur(newValue, e);
        };
        return _this;
    }
    BooleanField.prototype.coerceValue = function (value) {
        return !!value;
    };
    BooleanField.prototype.render = function () {
        var _this = this;
        var _a = this.props, confirm = _a.confirm, fieldProps = __rest(_a, ["confirm"]);
        return (<InputField {...fieldProps} resetOnError field={function (_a) {
            var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, disabled = _a.disabled, props = __rest(_a, ["onChange", "onBlur", "value", "disabled"]);
            // Create a function with required args bound
            var handleChange = _this.handleChange.bind(_this, value, onChange, onBlur);
            var switchProps = __assign(__assign({}, props), { size: 'lg', isActive: !!value, isDisabled: disabled, toggle: handleChange });
            if (confirm) {
                return (<Confirm renderMessage={function () { return confirm[(!value).toString()]; }} onConfirm={function () { return handleChange({}); }}>
                {function (_a) {
                    var open = _a.open;
                    return (<Switch {...switchProps} toggle={function (e) {
                        // If we have a `confirm` prop and enabling switch
                        // Then show confirm dialog, otherwise propagate change as normal
                        if (confirm[(!value).toString()]) {
                            // Open confirm modal
                            open();
                            return;
                        }
                        handleChange(e);
                    }}/>);
                }}
              </Confirm>);
            }
            return <Switch {...switchProps}/>;
        }}/>);
    };
    return BooleanField;
}(React.Component));
export default BooleanField;
//# sourceMappingURL=booleanField.jsx.map