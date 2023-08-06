import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import Form from 'app/components/forms/form';
import TextField from 'app/components/forms/textField';
import { t, tct } from 'app/locale';
var SsoForm = /** @class */ (function (_super) {
    __extends(SsoForm, _super);
    function SsoForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
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
                        return [4 /*yield*/, api.requestPromise('/auth/sso-locate/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        response = _a.sent();
                        onSuccess(data);
                        browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        if (!e_1.responseJSON) {
                            onError(e_1);
                            return [2 /*return*/];
                        }
                        message = e_1.responseJSON.detail;
                        this.setState({ errorMessage: message });
                        onError(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    SsoForm.prototype.render = function () {
        var serverHostname = this.props.authConfig.serverHostname;
        var errorMessage = this.state.errorMessage;
        return (<Form className="form-stacked" submitLabel={t('Continue')} onSubmit={this.handleSubmit} footerClass="auth-footer" errorMessage={errorMessage}>
        <TextField name="organization" placeholder="acme" label={t('Organization ID')} required help={tct('Your ID is the slug after the hostname. e.g. [example] is [slug].', {
            slug: <strong>acme</strong>,
            example: <SlugExample slug="acme" hostname={serverHostname}/>,
        })}/>
      </Form>);
    };
    return SsoForm;
}(React.Component));
var SlugExample = function (_a) {
    var hostname = _a.hostname, slug = _a.slug;
    return (<code>
    {hostname}/<strong>{slug}</strong>
  </code>);
};
export default SsoForm;
//# sourceMappingURL=ssoForm.jsx.map