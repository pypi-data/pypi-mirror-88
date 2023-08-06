import { __assign, __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { Client } from 'app/api';
import Form from 'app/components/forms/form';
import FormField from 'app/components/forms/formField';
import FormState from 'app/components/forms/state';
import { t } from 'app/locale';
var ApiForm = /** @class */ (function (_super) {
    __extends(ApiForm, _super);
    function ApiForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new Client();
        _this.onSubmit = function (e) {
            e.preventDefault();
            if (_this.state.state === FormState.SAVING) {
                return;
            }
            // Actual HTML forms do not submit data for disabled fields, and because of
            // the way some of our APIs are implemented, we need to start doing the
            // same. But, since some other parts of the app very probably depend on
            // sending disabled fields, keep that the default for now.
            // TODO(chadwhitacre): Expand and upstream this.
            var data = _this.props.omitDisabled ? _this.getEnabledData() : _this.state.data;
            _this.props.onSubmit && _this.props.onSubmit(data);
            _this.setState({
                state: FormState.SAVING,
            }, function () {
                addLoadingMessage(_this.props.submitLoadingMessage);
                _this.api.request(_this.props.apiEndpoint, {
                    method: _this.props.apiMethod,
                    data: data,
                    success: function (result) {
                        clearIndicators();
                        _this.onSubmitSuccess(result);
                    },
                    error: function (error) {
                        addErrorMessage(_this.props.submitErrorMessage);
                        _this.onSubmitError(error);
                    },
                });
            });
        };
        return _this;
    }
    ApiForm.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ApiForm.prototype.getEnabledData = function () {
        // Return a hash of data from non-disabled fields.
        // Start with this.state.data and remove rather than starting from scratch
        // and adding, because a) this.state.data is our source of truth, and b)
        // we'd have to do more work to loop over the state.data Object and lookup
        // against the props.children Array (looping over the Array and looking up
        // in the Object is more natural). Maybe the consequent use of delete
        // carries a slight performance hit. Why is yer form so big? 🤔
        var data = __assign({}, this.state.data); // Copy to avoid mutating state.data itself.
        React.Children.forEach(this.props.children, function (child) {
            var _a;
            if (!FormField.isPrototypeOf(child.type)) {
                return; // Form children include h4's, etc.
            }
            if (child.key && ((_a = child.props) === null || _a === void 0 ? void 0 : _a.disabled)) {
                delete data[child.key]; // Assume a link between child.key and data. 🐭
            }
        });
        return data;
    };
    ApiForm.propTypes = __assign(__assign({}, Form.propTypes), { omitDisabled: PropTypes.bool, onSubmit: PropTypes.func, apiMethod: PropTypes.string.isRequired, apiEndpoint: PropTypes.string.isRequired, submitLoadingMessage: PropTypes.string, submitErrorMessage: PropTypes.string });
    ApiForm.defaultProps = __assign(__assign({}, Form.defaultProps), { omitDisabled: false, submitErrorMessage: t('There was an error saving your changes.'), submitLoadingMessage: t('Saving changes\u2026') });
    return ApiForm;
}(Form));
export default ApiForm;
//# sourceMappingURL=apiForm.jsx.map