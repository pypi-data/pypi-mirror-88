import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AlertLink from 'app/components/alertLink';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Tag from 'app/components/tag';
import accountEmailsFields from 'app/data/forms/accountEmails';
import { IconDelete, IconStack } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var ENDPOINT = '/users/me/emails/';
var AccountEmails = /** @class */ (function (_super) {
    __extends(AccountEmails, _super);
    function AccountEmails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (_change, model, id) {
            if (id === undefined) {
                return;
            }
            model.setValue(id, '');
            _this.remountComponent();
        };
        _this.handleSetPrimary = function (email) {
            return _this.doApiCall(ENDPOINT, {
                method: 'PUT',
                data: { email: email },
            });
        };
        _this.handleRemove = function (email) {
            return _this.doApiCall(ENDPOINT, {
                method: 'DELETE',
                data: { email: email },
            });
        };
        _this.handleVerify = function (email) {
            return _this.doApiCall(ENDPOINT + "confirm/", {
                method: 'POST',
                data: { email: email },
            });
        };
        return _this;
    }
    AccountEmails.prototype.getEndpoints = function () {
        return [['emails', ENDPOINT]];
    };
    AccountEmails.prototype.getTitle = function () {
        return t('Emails');
    };
    AccountEmails.prototype.doApiCall = function (endpoint, requestParams) {
        var _this = this;
        this.setState({ loading: true, emails: [] }, function () {
            return _this.api
                .requestPromise(endpoint, requestParams)
                .then(function () { return _this.remountComponent(); })
                .catch(function (err) {
                var _a;
                _this.remountComponent();
                if ((_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.email) {
                    addErrorMessage(err.responseJSON.email);
                }
            });
        });
    };
    AccountEmails.prototype.renderBody = function () {
        var _this = this;
        var emails = this.state.emails;
        var primary = emails === null || emails === void 0 ? void 0 : emails.find(function (_a) {
            var isPrimary = _a.isPrimary;
            return isPrimary;
        });
        var secondary = emails === null || emails === void 0 ? void 0 : emails.filter(function (_a) {
            var isPrimary = _a.isPrimary;
            return !isPrimary;
        });
        return (<div>
        <SettingsPageHeader title={t('Emails')}/>

        <Panel>
          <PanelHeader>{t('Emails')}</PanelHeader>
          <PanelBody>
            {primary && (<EmailRow onRemove={this.handleRemove} onVerify={this.handleVerify} {...primary}/>)}

            {secondary === null || secondary === void 0 ? void 0 : secondary.map(function (emailObj) { return (<EmailRow key={emailObj.email} onSetPrimary={_this.handleSetPrimary} onRemove={_this.handleRemove} onVerify={_this.handleVerify} {...emailObj}/>); })}
          </PanelBody>
        </Panel>

        <Form apiMethod="POST" apiEndpoint={ENDPOINT} saveOnBlur allowUndo={false} onSubmitSuccess={this.handleSubmitSuccess}>
          <JsonForm location={this.props.location} forms={accountEmailsFields}/>
        </Form>

        <AlertLink to="/settings/account/notifications" icon={<IconStack />}>
          {t('Want to change how many emails you get? Use the notifications panel.')}
        </AlertLink>
      </div>);
    };
    return AccountEmails;
}(AsyncView));
export default AccountEmails;
var EmailRow = function (_a) {
    var email = _a.email, onRemove = _a.onRemove, onVerify = _a.onVerify, onSetPrimary = _a.onSetPrimary, isVerified = _a.isVerified, isPrimary = _a.isPrimary, hideRemove = _a.hideRemove;
    return (<EmailItem>
    <EmailTags>
      {email}
      {!isVerified && <Tag type="warning">{t('Unverified')}</Tag>}
      {isPrimary && <Tag type="success">{t('Primary')}</Tag>}
    </EmailTags>
    <ButtonBar gap={1}>
      {!isPrimary && isVerified && (<Button size="small" onClick={function (e) { return onSetPrimary === null || onSetPrimary === void 0 ? void 0 : onSetPrimary(email, e); }}>
          {t('Set as primary')}
        </Button>)}
      {!isVerified && (<Button size="small" onClick={function (e) { return onVerify(email, e); }}>
          {t('Resend verification')}
        </Button>)}
      {!hideRemove && !isPrimary && (<Button label={t('Remove email')} data-test-id="remove" priority="danger" size="small" icon={<IconDelete />} onClick={function (e) { return onRemove(email, e); }}/>)}
    </ButtonBar>
  </EmailItem>);
};
var EmailTags = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var EmailItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  justify-content: space-between;\n"], ["\n  justify-content: space-between;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=accountEmails.jsx.map