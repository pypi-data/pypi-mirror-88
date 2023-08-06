import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { ClassNames } from '@emotion/core';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Form from 'app/components/forms/form';
import PasswordField from 'app/components/forms/passwordField';
import TextField from 'app/components/forms/textField';
import Link from 'app/components/links/link';
import { IconGithub, IconGoogle, IconVsts } from 'app/icons';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import space from 'app/styles/space';
import { formFooterClass } from 'app/views/auth/login';
// TODO(epurkhiser): The abstraction here would be much nicer if we just
// exposed a configuration object telling us what auth providers there are.
var LoginProviders = function (_a) {
    var vstsLoginLink = _a.vstsLoginLink, githubLoginLink = _a.githubLoginLink, googleLoginLink = _a.googleLoginLink;
    return (<ProviderWrapper>
    <ProviderHeading>{t('External Account Login')}</ProviderHeading>
    {googleLoginLink && (<Button align="left" size="small" icon={<IconGoogle size="xs"/>} href={googleLoginLink}>
        {t('Sign in with Google')}
      </Button>)}
    {githubLoginLink && (<Button align="left" size="small" icon={<IconGithub size="xs"/>} href={githubLoginLink}>
        {t('Sign in with GitHub')}
      </Button>)}
    {vstsLoginLink && (<Button align="left" size="small" icon={<IconVsts size="xs"/>} href={vstsLoginLink}>
        {t('Sign in with Azure DevOps')}
      </Button>)}
  </ProviderWrapper>);
};
var LoginForm = /** @class */ (function (_super) {
    __extends(LoginForm, _super);
    function LoginForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
            errors: {},
        };
        _this.handleSubmit = function (data, onSuccess, onError) { return __awaiter(_this, void 0, void 0, function () {
            var response, e_1, message;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.props.api.requestPromise('/auth/login/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 1:
                        response = _a.sent();
                        onSuccess(data);
                        // TODO(epurkhiser): There is likely more that needs to happen to update
                        // the application state after user login.
                        ConfigStore.set('user', response.user);
                        // TODO(epurkhiser): Reconfigure sentry SDK identity
                        browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 3];
                    case 2:
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
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    LoginForm.prototype.render = function () {
        var _this = this;
        var _a = this.state, errorMessage = _a.errorMessage, errors = _a.errors;
        var _b = this.props.authConfig, githubLoginLink = _b.githubLoginLink, vstsLoginLink = _b.vstsLoginLink;
        var hasLoginProvider = !!(githubLoginLink || vstsLoginLink);
        return (<ClassNames>
        {function (_a) {
            var css = _a.css;
            return (<FormWrapper hasLoginProvider={hasLoginProvider}>
            <Form submitLabel={t('Continue')} onSubmit={_this.handleSubmit} footerClass={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                ", "\n              "], ["\n                ", "\n              "])), formFooterClass)} errorMessage={errorMessage} extraButton={<LostPasswordLink to="/account/recover/">
                  {t('Lost your password?')}
                </LostPasswordLink>}>
              <TextField name="username" placeholder={t('username or email')} label={t('Account')} error={errors.username} required/>
              <PasswordField name="password" placeholder={t('password')} label={t('Password')} error={errors.password} required/>
            </Form>
            {hasLoginProvider && <LoginProviders {...{ vstsLoginLink: vstsLoginLink, githubLoginLink: githubLoginLink }}/>}
          </FormWrapper>);
        }}
      </ClassNames>);
    };
    return LoginForm;
}(React.Component));
var FormWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: 60px;\n  grid-template-columns: ", ";\n"], ["\n  display: grid;\n  grid-gap: 60px;\n  grid-template-columns: ", ";\n"])), function (p) { return (p.hasLoginProvider ? '1fr 0.8fr' : '1fr'); });
var ProviderHeading = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0;\n  font-size: 15px;\n  font-weight: bold;\n  line-height: 24px;\n"], ["\n  margin: 0;\n  font-size: 15px;\n  font-weight: bold;\n  line-height: 24px;\n"])));
var ProviderWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-gap: ", ";\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    top: 0;\n    bottom: 0;\n    left: -30px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  position: relative;\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-gap: ", ";\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    top: 0;\n    bottom: 0;\n    left: -30px;\n    border-left: 1px solid ", ";\n  }\n"])), space(1.5), function (p) { return p.theme.border; });
var LostPasswordLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
export default LoginForm;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=loginForm.jsx.map