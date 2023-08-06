import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __values } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import debounce from 'lodash/debounce';
import set from 'lodash/set';
import * as queryString from 'query-string';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
var TicketRuleModal = /** @class */ (function (_super) {
    __extends(TicketRuleModal, _super);
    function TicketRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dynamicFieldChoices: {},
        };
        _this.getNames = function () {
            var formFields = _this.props.formFields;
            var names = [];
            for (var name_1 in formFields) {
                if (formFields[name_1].hasOwnProperty('name')) {
                    names.push(formFields[name_1].name);
                }
            }
            return names;
        };
        _this.cleanData = function (data) {
            var e_1, _a;
            var instance = _this.props.instance;
            var names = _this.getNames();
            var formData = {};
            if (instance === null || instance === void 0 ? void 0 : instance.hasOwnProperty('integration')) {
                formData.integration = instance === null || instance === void 0 ? void 0 : instance.integration;
            }
            try {
                for (var _b = __values(Object.entries(data)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = __read(_c.value, 2), key = _d[0], value = _d[1];
                    if (names.includes(key)) {
                        formData[key] = value;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return formData;
        };
        _this.onFormSubmit = function (data, _success, _error, e) {
            var _a = _this.props, onSubmitAction = _a.onSubmitAction, closeModal = _a.closeModal;
            e.preventDefault();
            e.stopPropagation();
            var formData = _this.cleanData(data);
            onSubmitAction(formData, _this.state.dynamicFieldChoices);
            addSuccessMessage(t('Changes applied.'));
            closeModal();
        };
        _this.debouncedOptionLoad = debounce(function (field, input, cb) { return __awaiter(_this, void 0, void 0, function () {
            var options, query, url, separator, response, _a, _b, _c, err_1;
            var _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        options = this.props.instance;
                        query = queryString.stringify({
                            project: options === null || options === void 0 ? void 0 : options.project,
                            issuetype: options === null || options === void 0 ? void 0 : options.issuetype,
                            field: field.name,
                            query: input,
                        });
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
        }); }, 200, { trailing: true });
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
                        var dynamicFieldChoices_1 = result.options.map(function (obj) { return [obj.value, obj.label]; });
                        _this.setState(function (prevState) {
                            var newState = cloneDeep(prevState);
                            set(newState, "dynamicFieldChoices[" + field.name + "]", dynamicFieldChoices_1);
                            return newState;
                        });
                        resolve(result);
                    }
                });
            });
        };
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
        _this.addFields = function (fields) {
            var title = {
                name: 'title',
                label: 'Title',
                type: 'string',
                default: 'This will be the same as the Sentry Issue.',
                disabled: true,
            };
            var description = {
                name: 'description',
                label: 'Description',
                type: 'string',
                default: 'This will be generated from the Sentry Issue details.',
                disabled: true,
            };
            fields.unshift(description);
            fields.unshift(title);
        };
        return _this;
    }
    TicketRuleModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, formFields = _a.formFields, closeModal = _a.closeModal, link = _a.link, ticketType = _a.ticketType, instance = _a.instance;
        var text = t('When this alert is triggered %s will be created with the following fields. ', ticketType);
        var submitLabel = t('Apply Changes');
        var cancelLabel = t('Close');
        var fields = Object.values(formFields);
        this.addFields(fields);
        var initialData = instance || {};
        fields.forEach(function (field) {
            // passing an empty array breaks multi select
            // TODO(jess): figure out why this is breaking and fix
            if (!initialData.hasOwnProperty(field.name)) {
                initialData[field.name] = field.multiple ? '' : field.default;
            }
        });
        return (<React.Fragment>
        <Header closeButton>{t('Issue Link Settings')}</Header>
        <Body>
          <BodyText>
            {text}
            {tct("It'll also [linkToDocs] with the new Sentry Issue.", {
            linkToDocs: <ExternalLink href={link}>{t('stay in sync')}</ExternalLink>,
        })}
          </BodyText>
          <Form onSubmit={this.onFormSubmit} initialData={initialData} submitLabel={submitLabel} cancelLabel={cancelLabel} footerClass="modal-footer" onCancel={closeModal}>
            {fields
            .filter(function (field) { return field.hasOwnProperty('name'); })
            .map(function (field) { return (<FieldFromConfig key={field.name + "-" + field.default + "-" + field.required} field={field} inline={false} stacked flexibleControlStateSize {..._this.getFieldProps(field)}/>); })}
          </Form>
        </Body>
      </React.Fragment>);
    };
    return TicketRuleModal;
}(React.Component));
var BodyText = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
export default TicketRuleModal;
var templateObject_1;
//# sourceMappingURL=ticketRuleModal.jsx.map