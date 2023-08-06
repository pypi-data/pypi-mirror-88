import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { Panel, PanelAlert, PanelBody, PanelHeader, PanelItem, } from 'app/components/panels';
import { IconFlag } from 'app/icons';
import { t, tct } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var BYE_URL = '/';
var leaveRedirect = function () { return (window.location.href = BYE_URL); };
var Important = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.2em;\n"], ["\n  font-weight: bold;\n  font-size: 1.2em;\n"])));
var GoodbyeModalContent = function (_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
    return (<div>
    <Header>{t('Closing Account')}</Header>
    <Body>
      <TextBlock>
        {t('Your account has been deactivated and scheduled for removal.')}
      </TextBlock>
      <TextBlock>
        {t('Thanks for using Sentry! We hope to see you again soon!')}
      </TextBlock>
    </Body>
    <Footer>
      <Button href={BYE_URL}>{t('Goodbye')}</Button>
    </Footer>
  </div>);
};
var AccountClose = /** @class */ (function (_super) {
    __extends(AccountClose, _super);
    function AccountClose() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (_a, isSingle, event) {
            var slug = _a.slug;
            var checked = event.target.checked;
            // Can't unselect an org where you are the single owner
            if (isSingle) {
                return;
            }
            _this.setState(function (state) {
                var set = state.orgsToRemove || new Set(_this.singleOwnerOrgs);
                if (checked) {
                    set.add(slug);
                }
                else {
                    set.delete(slug);
                }
                return { orgsToRemove: set };
            });
        };
        _this.handleRemoveAccount = function () { return __awaiter(_this, void 0, void 0, function () {
            var orgsToRemove, orgs, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        orgsToRemove = this.state.orgsToRemove;
                        orgs = orgsToRemove === null ? this.singleOwnerOrgs : Array.from(orgsToRemove);
                        addLoadingMessage('Closing account\u2026');
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise('/users/me/', {
                                method: 'DELETE',
                                data: { organizations: orgs },
                            })];
                    case 2:
                        _b.sent();
                        openModal(GoodbyeModalContent, {
                            onClose: leaveRedirect,
                        });
                        // Redirect after 10 seconds
                        setTimeout(leaveRedirect, 10000);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage('Error closing account');
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountClose.prototype.getEndpoints = function () {
        return [['organizations', '/organizations/?owner=1']];
    };
    AccountClose.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { orgsToRemove: null });
    };
    Object.defineProperty(AccountClose.prototype, "singleOwnerOrgs", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.state.organizations) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                var singleOwner = _a.singleOwner;
                return singleOwner;
            })) === null || _b === void 0 ? void 0 : _b.map(function (_a) {
                var organization = _a.organization;
                return organization.slug;
            });
        },
        enumerable: false,
        configurable: true
    });
    AccountClose.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, organizations = _a.organizations, orgsToRemove = _a.orgsToRemove;
        return (<div>
        <SettingsPageHeader title="Close Account"/>

        <TextBlock>
          {t('This will permanently remove all associated data for your user')}.
        </TextBlock>

        <Alert type="error" icon={<IconFlag size="md"/>}>
          <Important>
            {t('Closing your account is permanent and cannot be undone')}!
          </Important>
        </Alert>

        <Panel>
          <PanelHeader>{t('Remove the following organizations')}</PanelHeader>
          <PanelBody>
            <PanelAlert type="info">
              {t('Ownership will remain with other organization owners if an organization is not deleted.')}
              <br />
              {tct("Boxes which can't be unchecked mean that you are the only organization owner and the organization [strong:will be deleted].", { strong: <strong /> })}
            </PanelAlert>

            {organizations === null || organizations === void 0 ? void 0 : organizations.map(function (_a) {
            var organization = _a.organization, singleOwner = _a.singleOwner;
            return (<PanelItem key={organization.slug}>
                <label>
                  <input style={{ marginRight: 6 }} type="checkbox" value={organization.slug} onChange={_this.handleChange.bind(_this, organization, singleOwner)} name="organizations" checked={orgsToRemove === null
                ? singleOwner
                : orgsToRemove.has(organization.slug)} disabled={singleOwner}/>
                  {organization.slug}
                </label>
              </PanelItem>);
        })}
          </PanelBody>
        </Panel>

        <Confirm priority="danger" message={t('This is permanent and cannot be undone, are you really sure you want to do this?')} onConfirm={this.handleRemoveAccount}>
          <Button priority="danger">{t('Close Account')}</Button>
        </Confirm>
      </div>);
    };
    return AccountClose;
}(AsyncView));
export default AccountClose;
var templateObject_1;
//# sourceMappingURL=accountClose.jsx.map