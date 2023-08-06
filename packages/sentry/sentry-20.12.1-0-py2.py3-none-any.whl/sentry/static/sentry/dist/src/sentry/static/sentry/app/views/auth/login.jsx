import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import NavTabs from 'app/components/navTabs';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import LoginForm from './loginForm';
import RegisterForm from './registerForm';
import SsoForm from './ssoForm';
var FORM_COMPONENTS = {
    login: LoginForm,
    register: RegisterForm,
    sso: SsoForm,
};
var Login = /** @class */ (function (_super) {
    __extends(Login, _super);
    function Login() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: null,
            activeTab: 'login',
            authConfig: null,
        };
        _this.handleSetTab = function (activeTab, event) {
            _this.setState({ activeTab: activeTab });
            event.preventDefault();
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var api, response, vsts_login_link, github_login_link, google_login_link, config, authConfig, e_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/config/')];
                    case 2:
                        response = _a.sent();
                        vsts_login_link = response.vsts_login_link, github_login_link = response.github_login_link, google_login_link = response.google_login_link, config = __rest(response, ["vsts_login_link", "github_login_link", "google_login_link"]);
                        authConfig = __assign(__assign({}, config), { vstsLoginLink: vsts_login_link, githubLoginLink: github_login_link, googleLoginLink: google_login_link });
                        this.setState({ authConfig: authConfig });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        this.setState({ error: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Login.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Object.defineProperty(Login.prototype, "hasAuthProviders", {
        get: function () {
            if (this.state.authConfig === null) {
                return false;
            }
            var _a = this.state.authConfig, githubLoginLink = _a.githubLoginLink, googleLoginLink = _a.googleLoginLink, vstsLoginLink = _a.vstsLoginLink;
            return !!(githubLoginLink || vstsLoginLink || googleLoginLink);
        },
        enumerable: false,
        configurable: true
    });
    Login.prototype.render = function () {
        var _this = this;
        var api = this.props.api;
        var _a = this.state, loading = _a.loading, error = _a.error, activeTab = _a.activeTab, authConfig = _a.authConfig;
        var FormComponent = FORM_COMPONENTS[activeTab];
        var tabs = [
            ['login', t('Login')],
            ['sso', t('Single Sign-On')],
            ['register', t('Register'), !(authConfig === null || authConfig === void 0 ? void 0 : authConfig.canRegister)],
        ];
        var renderTab = function (_a) {
            var _b = __read(_a, 3), key = _b[0], label = _b[1], disabled = _b[2];
            return !disabled && (<li key={key} className={activeTab === key ? 'active' : ''}>
          <a href="#" onClick={function (e) { return _this.handleSetTab(key, e); }}>
            {label}
          </a>
        </li>);
        };
        return (<React.Fragment>
        <Header>
          <Heading>{t('Sign in to continue')}</Heading>
          <AuthNavTabs>{tabs.map(renderTab)}</AuthNavTabs>
        </Header>
        {loading && <LoadingIndicator />}
        {error && (<StyledLoadingError message={t('Unable to load authentication configuration')} onRetry={this.fetchData}/>)}
        {!loading && authConfig !== null && !error && (<FormWrapper hasAuthProviders={this.hasAuthProviders}>
            <FormComponent {...{ api: api, authConfig: authConfig }}/>
          </FormWrapper>)}
      </React.Fragment>);
    };
    return Login;
}(React.Component));
var StyledLoadingError = styled(LoadingError)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(2));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: 20px 40px 0;\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: 20px 40px 0;\n"])), function (p) { return p.theme.border; });
var Heading = styled('h3')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 24px;\n  margin: 0 0 20px 0;\n"], ["\n  font-size: 24px;\n  margin: 0 0 20px 0;\n"])));
var AuthNavTabs = styled(NavTabs)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var FormWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: 35px;\n  width: ", ";\n"], ["\n  padding: 35px;\n  width: ", ";\n"])), function (p) { return (p.hasAuthProviders ? '600px' : '490px'); });
var formFooterClass = "\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: " + space(1) + ";\n  align-items: center;\n  justify-items: end;\n  border-top: none;\n  margin-bottom: 0;\n  padding: 0;\n";
export { formFooterClass };
export default withApi(Login);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=login.jsx.map