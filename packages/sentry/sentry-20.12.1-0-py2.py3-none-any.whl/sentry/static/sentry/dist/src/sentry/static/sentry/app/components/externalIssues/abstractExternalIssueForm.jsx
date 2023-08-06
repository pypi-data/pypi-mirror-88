import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import { Modal } from 'react-bootstrap';
import debounce from 'lodash/debounce';
import * as queryString from 'query-string';
import AsyncComponent from 'app/components/asyncComponent';
import { tct } from 'app/locale';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
var DEBOUNCE_MS = 200;
/**
 * @abstract
 */
var AbstractExternalIssueForm = /** @class */ (function (_super) {
    __extends(AbstractExternalIssueForm, _super);
    function AbstractExternalIssueForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldRenderBadRequests = true;
        _this.refetchConfig = function () {
            var _a = _this.state, action = _a.action, dynamicFieldValues = _a.dynamicFieldValues;
            var query = __assign({ action: action }, dynamicFieldValues);
            var endpoint = _this.getEndPointString();
            _this.api.request(endpoint, {
                method: 'GET',
                query: query,
                success: function (data, _, jqXHR) {
                    _this.handleRequestSuccess({ stateKey: 'integrationDetails', data: data, jqXHR: jqXHR }, true);
                },
                error: function (error) {
                    _this.handleError(error, ['integrationDetails', endpoint, null, null]);
                },
            });
        };
        _this.getConfigName = function () {
            // Explicitly returning a non-interpolated string for clarity.
            var action = _this.state.action;
            switch (action) {
                case 'create':
                    return 'createIssueConfig';
                case 'link':
                    return 'linkIssueConfig';
                default:
                    throw new Error('illegal action');
            }
        };
        _this.getDynamicFields = function (integrationDetailsParam) {
            var integrationDetailsFromState = _this.state.integrationDetails;
            var integrationDetails = integrationDetailsParam || integrationDetailsFromState;
            var config = (integrationDetails || {})[_this.getConfigName()];
            return Object.fromEntries((config || [])
                .filter(function (field) { return field.updatesForm; })
                .map(function (field) { return [field.name, field.default || null]; }));
        };
        _this.onRequestSuccess = function (_a) {
            var stateKey = _a.stateKey, data = _a.data;
            if (stateKey === 'integrationDetails') {
                _this.setState({
                    dynamicFieldValues: _this.getDynamicFields(data),
                });
            }
        };
        _this.onFieldChange = function (label, value) {
            var dynamicFieldValues = _this.state.dynamicFieldValues;
            var dynamicFields = _this.getDynamicFields();
            if (dynamicFields.hasOwnProperty(label) && dynamicFieldValues) {
                dynamicFieldValues[label] = value;
                _this.setState({
                    dynamicFieldValues: dynamicFieldValues,
                    reloading: true,
                    error: false,
                    remainingRequests: 1,
                }, _this.refetchConfig);
            }
        };
        _this.updateDynamicFieldChoices = function (_field, _result) {
            // Do nothing.
        };
        _this.getOptions = function (field, input) {
            return new Promise(function (resolve, reject) {
                if (!input) {
                    var choices = field.choices || [];
                    var options = choices.map(function (_a) {
                        var _b = __read(_a, 2), value = _b[0], label = _b[1];
                        return ({ value: value, label: label });
                    });
                    return resolve({ options: options });
                }
                return _this.debouncedOptionLoad(field, input, function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        _this.updateDynamicFieldChoices(field, result);
                        resolve(result);
                    }
                });
            });
        };
        _this.debouncedOptionLoad = debounce(function (field, input, cb) { return __awaiter(_this, void 0, void 0, function () {
            var dynamicFieldValues, query, url, separator, response, _a, _b, _c, err_1;
            var _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        dynamicFieldValues = this.state.dynamicFieldValues;
                        query = queryString.stringify(__assign(__assign({}, dynamicFieldValues), { field: field.name, query: input }));
                        url = field.url || '';
                        separator = url.includes('?') ? '&' : '?';
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 6, , 7]);
                        return [4 /*yield*/, fetch(url + separator + query)];
                    case 2:
                        response = _e.sent();
                        _a = cb;
                        _b = [null];
                        _d = {};
                        if (!response.ok) return [3 /*break*/, 4];
                        return [4 /*yield*/, response.json()];
                    case 3:
                        _c = _e.sent();
                        return [3 /*break*/, 5];
                    case 4:
                        _c = [];
                        _e.label = 5;
                    case 5:
                        _a.apply(void 0, _b.concat([(_d.options = _c, _d)]));
                        return [3 /*break*/, 7];
                    case 6:
                        err_1 = _e.sent();
                        cb(err_1);
                        return [3 /*break*/, 7];
                    case 7: return [2 /*return*/];
                }
            });
        }); }, DEBOUNCE_MS, { trailing: true });
        _this.getFieldProps = function (field) {
            return field.url
                ? {
                    loadOptions: function (input) { return _this.getOptions(field, input); },
                    async: true,
                    cache: false,
                    onSelectResetsInput: false,
                    onCloseResetsInput: false,
                    onBlurResetsInput: false,
                    autoload: true,
                }
                : {};
        };
        // Abstract methods.
        _this.getEndPointString = function () { return ''; };
        _this.renderNavTabs = function () { return null; };
        _this.renderBodyText = function () { return null; };
        _this.getTitle = function () { return tct('Issue Link Settings', {}); };
        _this.getFormProps = function () {
            throw new Error("Method 'getFormProps()' must be implemented.");
        };
        _this.getDefaultFormProps = function () {
            return {
                footerClass: 'modal-footer',
                onFieldChange: _this.onFieldChange,
                submitDisabled: _this.state.reloading,
            };
        };
        _this.renderForm = function (formFields) {
            var initialData = (formFields || []).reduce(function (accumulator, field) {
                // passing an empty array breaks multi select
                // TODO(jess): figure out why this is breaking and fix
                if (!accumulator.hasOwnProperty(field.name)) {
                    accumulator[field.name] = field.multiple ? '' : field.default;
                }
                return accumulator;
            }, {});
            return (<React.Fragment>
        <Modal.Header closeButton>
          <Modal.Title>{_this.getTitle()}</Modal.Title>
        </Modal.Header>
        {_this.renderNavTabs()}
        <Modal.Body>
          {_this.shouldRenderLoading() ? (_this.renderLoading()) : (<React.Fragment>
              {_this.renderBodyText()}
              <Form initialData={initialData} {..._this.getFormProps()}>
                {(formFields || [])
                .filter(function (field) { return field.hasOwnProperty('name'); })
                .map(function (field) { return (<FieldFromConfig key={field.name + "-" + field.default + "-" + field.required} field={field} inline={false} stacked flexibleControlStateSize disabled={_this.state.reloading} {..._this.getFieldProps(field)}/>); })}
              </Form>
            </React.Fragment>)}
        </Modal.Body>
      </React.Fragment>);
        };
        return _this;
    }
    AbstractExternalIssueForm.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { action: 'create', 
            // This is derived from integrationDetails when it loads.
            dynamicFieldValues: null, 
            // This is fetched by AsyncComponent.getEndpoints.
            integrationDetails: null });
    };
    AbstractExternalIssueForm.prototype.renderComponent = function () {
        return this.state.error
            ? this.renderError(new Error('Unable to load all required endpoints'))
            : this.renderBody();
    };
    return AbstractExternalIssueForm;
}(AsyncComponent));
export default AbstractExternalIssueForm;
//# sourceMappingURL=abstractExternalIssueForm.jsx.map