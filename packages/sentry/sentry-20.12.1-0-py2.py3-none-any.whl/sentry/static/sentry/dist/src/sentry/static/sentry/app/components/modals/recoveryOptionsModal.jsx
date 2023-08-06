import { __assign, __extends } from "tslib";
import React from 'react';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TextBlock from 'app/views/settings/components/text/textBlock';
var RecoveryOptionsModal = /** @class */ (function (_super) {
    __extends(RecoveryOptionsModal, _super);
    function RecoveryOptionsModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSkipSms = function () {
            _this.setState({ skipSms: true });
        };
        return _this;
    }
    RecoveryOptionsModal.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { skipSms: false });
    };
    RecoveryOptionsModal.prototype.getEndpoints = function () {
        return [['authenticators', '/users/me/authenticators/']];
    };
    RecoveryOptionsModal.prototype.renderBody = function () {
        var _a = this.props, authenticatorName = _a.authenticatorName, closeModal = _a.closeModal, Body = _a.Body, Header = _a.Header, Footer = _a.Footer;
        var _b = this.state, authenticators = _b.authenticators, skipSms = _b.skipSms;
        var _c = authenticators.reduce(function (obj, item) {
            obj[item.id] = item;
            return obj;
        }, {}), recovery = _c.recovery, sms = _c.sms;
        var recoveryEnrolled = recovery && recovery.isEnrolled;
        var displaySmsPrompt = sms && !sms.isEnrolled && !skipSms;
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          {t('Two-Factor Authentication Enabled')}
        </Header>

        <Body>
          <TextBlock>
            {t('Two-factor authentication via %s has been enabled.', authenticatorName)}
          </TextBlock>
          <TextBlock>
            {t('You should now set up recovery options to secure your account.')}
          </TextBlock>

          {displaySmsPrompt ? (
        // set up backup phone number
        <Alert type="warning">
              {t('We recommend adding a phone number as a backup 2FA method.')}
            </Alert>) : (
        // get recovery codes
        <Alert type="warning">
              {t("Recovery codes are the only way to access your account if you lose\n                  your device and cannot receive two-factor authentication codes.")}
            </Alert>)}
        </Body>

        {displaySmsPrompt ? (
        // set up backup phone number
        <Footer>
            <Button onClick={this.handleSkipSms} name="skipStep" autoFocus>
              {t('Skip this step')}
            </Button>
            <Button priority="primary" onClick={closeModal} to={"/settings/account/security/mfa/" + sms.id + "/enroll/"} name="addPhone" css={{ marginLeft: space(1) }} autoFocus>
              {t('Add a Phone Number')}
            </Button>
          </Footer>) : (
        // get recovery codes
        <Footer>
            <Button priority="primary" onClick={closeModal} to={recoveryEnrolled
            ? "/settings/account/security/mfa/" + recovery.authId + "/"
            : '/settings/account/security/'} name="getCodes" autoFocus>
              {t('Get Recovery Codes')}
            </Button>
          </Footer>)}
      </React.Fragment>);
    };
    return RecoveryOptionsModal;
}(AsyncComponent));
export default RecoveryOptionsModal;
//# sourceMappingURL=recoveryOptionsModal.jsx.map