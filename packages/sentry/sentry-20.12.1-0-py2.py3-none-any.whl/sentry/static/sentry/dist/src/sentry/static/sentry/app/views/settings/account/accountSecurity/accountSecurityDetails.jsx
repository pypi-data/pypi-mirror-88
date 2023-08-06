import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
/**
 * AccountSecurityDetails is only displayed when user is enrolled in the 2fa method.
 * It displays created + last used time of the 2fa method.
 *
 * Also displays 2fa method specific details.
 */
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import CircleIndicator from 'app/components/circleIndicator';
import DateTime from 'app/components/dateTime';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import AsyncView from 'app/views/asyncView';
import RecoveryCodes from 'app/views/settings/account/accountSecurity/components/recoveryCodes';
import RemoveConfirm from 'app/views/settings/account/accountSecurity/components/removeConfirm';
import U2fEnrolledDetails from 'app/views/settings/account/accountSecurity/components/u2fEnrolledDetails';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var ENDPOINT = '/users/me/authenticators/';
function AuthenticatorDate(_a) {
    var label = _a.label, date = _a.date;
    return (<React.Fragment>
      <DateLabel>{label}</DateLabel>
      <div>{date ? <DateTime date={date}/> : t('never')}</div>
    </React.Fragment>);
}
var AccountSecurityDetails = /** @class */ (function (_super) {
    __extends(AccountSecurityDetails, _super);
    function AccountSecurityDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function (device) { return __awaiter(_this, void 0, void 0, function () {
            var authenticator, deviceId, deviceName, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        authenticator = this.state.authenticator;
                        if (!authenticator || !authenticator.authId) {
                            return [2 /*return*/];
                        }
                        deviceId = device ? device.key_handle + "/" : '';
                        deviceName = device ? device.name : t('Authenticator');
                        this.setState({ loading: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + ENDPOINT + authenticator.authId + "/" + deviceId, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        this.props.router.push('/settings/account/security');
                        addSuccessMessage(t('%s has been removed', deviceName));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        // Error deleting authenticator
                        this.setState({ loading: false });
                        addErrorMessage(t('Error removing %s', deviceName));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountSecurityDetails.prototype.getTitle = function () {
        return t('Security');
    };
    AccountSecurityDetails.prototype.getEndpoints = function () {
        var params = this.props.params;
        var authId = params.authId;
        return [['authenticator', "" + ENDPOINT + authId + "/"]];
    };
    AccountSecurityDetails.prototype.renderBody = function () {
        var authenticator = this.state.authenticator;
        if (!authenticator) {
            return null;
        }
        var _a = this.props, deleteDisabled = _a.deleteDisabled, onRegenerateBackupCodes = _a.onRegenerateBackupCodes;
        return (<React.Fragment>
        <SettingsPageHeader title={<React.Fragment>
              <span>{authenticator.name}</span>
              <AuthenticatorStatus enabled={authenticator.isEnrolled}/>
            </React.Fragment>} action={authenticator.isEnrolled &&
            authenticator.removeButton && (<Tooltip title={t("Two-factor authentication is required for at least one organization you're a member of.")} disabled={!deleteDisabled}>
                <RemoveConfirm onConfirm={this.handleRemove} disabled={deleteDisabled}>
                  <Button priority="danger">{authenticator.removeButton}</Button>
                </RemoveConfirm>
              </Tooltip>)}/>

        <TextBlock>{authenticator.description}</TextBlock>

        <AuthenticatorDates>
          <AuthenticatorDate label={t('Created at')} date={authenticator.createdAt}/>
          <AuthenticatorDate label={t('Last used')} date={authenticator.lastUsedAt}/>
        </AuthenticatorDates>

        <U2fEnrolledDetails isEnrolled={authenticator.isEnrolled} id={authenticator.id} devices={authenticator.devices} onRemoveU2fDevice={this.handleRemove}/>

        {authenticator.isEnrolled && authenticator.phone && (<PhoneWrapper>
            {t('Confirmation codes are sent to the following phone number')}:
            <Phone>{authenticator.phone}</Phone>
          </PhoneWrapper>)}

        <RecoveryCodes onRegenerateBackupCodes={onRegenerateBackupCodes} isEnrolled={authenticator.isEnrolled} codes={authenticator.codes}/>
      </React.Fragment>);
    };
    return AccountSecurityDetails;
}(AsyncView));
export default AccountSecurityDetails;
var AuthenticatorStatus = styled(CircleIndicator)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var AuthenticatorDates = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content auto;\n"])), space(2));
var DateLabel = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var PhoneWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(4));
var Phone = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-weight: bold;\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=accountSecurityDetails.jsx.map