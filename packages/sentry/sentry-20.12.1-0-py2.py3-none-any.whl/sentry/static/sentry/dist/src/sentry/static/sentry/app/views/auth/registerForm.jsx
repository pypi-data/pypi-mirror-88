import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { ClassNames } from '@emotion/core';
import styled from '@emotion/styled';
import Form from 'app/components/forms/form';
import PasswordField from 'app/components/forms/passwordField';
import RadioBooleanField from 'app/components/forms/radioBooleanField';
import TextField from 'app/components/forms/textField';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import { formFooterClass } from 'app/views/auth/login';
var SubscribeField = function () { return (<RadioBooleanField name="subscribe" yesLabel={t('Yes, I would like to receive updates via email')} noLabel={t("No, I'd prefer not to receive these updates")} help={tct("We'd love to keep you updated via email with product and feature\n           announcements, promotions, educational materials, and events. Our\n           updates focus on relevant information, and we'll never sell your data\n           to third parties. See our [link] for more details.", {
    link: <a href="https://sentry.io/privacy/">Privacy Policy</a>,
})}/>); };
var RegisterForm = /** @class */ (function (_super) {
    __extends(RegisterForm, _super);
    function RegisterForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
            errors: {},
        };
        _this.handleSubmit = function (data, onSuccess, onError) { return __awaiter(_this, void 0, void 0, function () {
            var api, response, e_1, message;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/register/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        response = _a.sent();
                        onSuccess(data);
                        // TODO(epurkhiser): There is more we need to do to setup the user. but
                        // definitely primarily we need to init our user.
                        ConfigStore.set('user', response.user);
                        browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        if (!e_1.responseJSON || !e_1.responseJSON.errors) {
                            onError(e_1);
                            return [2 /*return*/];
                        }
                        message = e_1.responseJSON.detail;
                        if (e_1.responseJSON.errors.__all__) {
                            message = e_1.responseJSON.errors.__all__;
                        }
                        this.setState({
                            errorMessage: message,
                            errors: e_1.responseJSON.errors || {},
                        });
                        onError(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    RegisterForm.prototype.render = function () {
        var _this = this;
        var hasNewsletter = this.props.authConfig.hasNewsletter;
        var _a = this.state, errorMessage = _a.errorMessage, errors = _a.errors;
        return (<ClassNames>
        {function (_a) {
            var css = _a.css;
            return (<Form initialData={{ subscribe: true }} submitLabel={t('Continue')} onSubmit={_this.handleSubmit} footerClass={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n              ", "\n            "], ["\n              ", "\n            "])), formFooterClass)} errorMessage={errorMessage} extraButton={<PrivacyPolicyLink href="https://sentry.io/privacy/">
                {t('Privacy Policy')}
              </PrivacyPolicyLink>}>
            <TextField name="name" placeholder={t('Jane Bloggs')} maxlength={30} label={t('Name')} error={errors.name} required/>
            <TextField name="username" placeholder={t('you@example.com')} maxlength={128} label={t('Email')} error={errors.username} required/>
            <PasswordField name="password" placeholder={t('something super secret')} label={t('Password')} error={errors.password} required/>
            {hasNewsletter && <SubscribeField />}
          </Form>);
        }}
      </ClassNames>);
    };
    return RegisterForm;
}(React.Component));
var PrivacyPolicyLink = styled(ExternalLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
export default RegisterForm;
var templateObject_1, templateObject_2;
//# sourceMappingURL=registerForm.jsx.map