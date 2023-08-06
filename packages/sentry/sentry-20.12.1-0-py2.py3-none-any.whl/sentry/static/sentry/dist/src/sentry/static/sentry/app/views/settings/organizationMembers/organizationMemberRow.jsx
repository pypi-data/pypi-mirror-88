import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import UserAvatar from 'app/components/avatar/userAvatar';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import { PanelItem } from 'app/components/panels';
import { IconCheckmark, IconClose, IconFlag, IconMail, IconSubtract } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import recreateRoute from 'app/utils/recreateRoute';
var OrganizationMemberRow = /** @class */ (function (_super) {
    __extends(OrganizationMemberRow, _super);
    function OrganizationMemberRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            busy: false,
        };
        _this.handleRemove = function () {
            var onRemove = _this.props.onRemove;
            if (typeof onRemove !== 'function') {
                return;
            }
            _this.setState({ busy: true });
            onRemove(_this.props.member);
        };
        _this.handleLeave = function () {
            var onLeave = _this.props.onLeave;
            if (typeof onLeave !== 'function') {
                return;
            }
            _this.setState({ busy: true });
            onLeave(_this.props.member);
        };
        _this.handleSendInvite = function () {
            var _a = _this.props, onSendInvite = _a.onSendInvite, member = _a.member;
            if (typeof onSendInvite !== 'function') {
                return;
            }
            onSendInvite(member);
        };
        return _this;
    }
    OrganizationMemberRow.prototype.render = function () {
        var _a = this.props, params = _a.params, routes = _a.routes, member = _a.member, orgName = _a.orgName, status = _a.status, requireLink = _a.requireLink, memberCanLeave = _a.memberCanLeave, currentUser = _a.currentUser, canRemoveMembers = _a.canRemoveMembers, canAddMembers = _a.canAddMembers;
        var id = member.id, flags = member.flags, email = member.email, name = member.name, roleName = member.roleName, pending = member.pending, expired = member.expired, user = member.user;
        // if member is not the only owner, they can leave
        var needsSso = !flags['sso:linked'] && requireLink;
        var isCurrentUser = currentUser.email === email;
        var showRemoveButton = !isCurrentUser;
        var showLeaveButton = isCurrentUser;
        var canRemoveMember = canRemoveMembers && !isCurrentUser;
        // member has a `user` property if they are registered with sentry
        // i.e. has accepted an invite to join org
        var has2fa = user && user.has2fa;
        var detailsUrl = recreateRoute(id, { routes: routes, params: params });
        var isInviteSuccessful = status === 'success';
        var isInviting = status === 'loading';
        var showResendButton = pending || needsSso;
        return (<StyledPanelItem data-test-id={email}>
        <MemberHeading>
          <UserAvatar size={32} user={user !== null && user !== void 0 ? user : { id: email, email: email }}/>
          <MemberDescription to={detailsUrl}>
            <h5 style={{ margin: '0 0 3px' }}>
              <UserName>{name}</UserName>
            </h5>
            <Email>{email}</Email>
          </MemberDescription>
        </MemberHeading>

        <div data-test-id="member-role">
          {pending ? (<InvitedRole>
              <IconMail size="md"/>
              {expired ? t('Expired Invite') : tct('Invited [roleName]', { roleName: roleName })}
            </InvitedRole>) : (roleName)}
        </div>

        <div data-test-id="member-status">
          {showResendButton ? (<React.Fragment>
              {isInviting && (<LoadingContainer>
                  <LoadingIndicator mini/>
                </LoadingContainer>)}
              {isInviteSuccessful && <span>Sent!</span>}
              {!isInviting && !isInviteSuccessful && (<Button disabled={!canAddMembers} priority="primary" size="small" onClick={this.handleSendInvite}>
                  {pending ? t('Resend invite') : t('Resend SSO link')}
                </Button>)}
            </React.Fragment>) : (<AuthStatus>
              {has2fa ? (<IconCheckmark isCircled color="success"/>) : (<IconFlag color="error"/>)}
              {has2fa ? t('2FA Enabled') : t('2FA Not Enabled')}
            </AuthStatus>)}
        </div>

        {showRemoveButton || showLeaveButton ? (<div>
            {showRemoveButton && canRemoveMember && (<Confirm message={tct('Are you sure you want to remove [name] from [orgName]?', {
            name: name,
            orgName: orgName,
        })} onConfirm={this.handleRemove}>
                <Button data-test-id="remove" icon={<IconSubtract isCircled size="xs"/>} size="small" busy={this.state.busy}>
                  {t('Remove')}
                </Button>
              </Confirm>)}

            {showRemoveButton && !canRemoveMember && (<Button disabled size="small" title={t('You do not have access to remove members')} icon={<IconSubtract isCircled size="xs"/>}>
                {t('Remove')}
              </Button>)}

            {showLeaveButton && memberCanLeave && (<Confirm message={tct('Are you sure you want to leave [orgName]?', {
            orgName: orgName,
        })} onConfirm={this.handleLeave}>
                <Button priority="danger" size="small" icon={<IconClose size="xs"/>}>
                  {t('Leave')}
                </Button>
              </Confirm>)}

            {showLeaveButton && !memberCanLeave && (<Button size="small" icon={<IconClose size="xs"/>} disabled title={t('You cannot leave this organization as you are the only organization owner.')}>
                {t('Leave')}
              </Button>)}
          </div>) : null}
      </StyledPanelItem>);
    };
    return OrganizationMemberRow;
}(React.PureComponent));
export default OrganizationMemberRow;
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(150px, 2fr) minmax(90px, 1fr) minmax(120px, 1fr) 90px;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: minmax(150px, 2fr) minmax(90px, 1fr) minmax(120px, 1fr) 90px;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(2));
var Section = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var MemberHeading = styled(Section)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var MemberDescription = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var UserName = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: block;\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  display: block;\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.fontSizeLarge; });
var Email = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeMedium; });
var InvitedRole = styled(Section)(templateObject_7 || (templateObject_7 = __makeTemplateObject([""], [""])));
var LoadingContainer = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-top: 0;\n  margin-bottom: ", ";\n"], ["\n  margin-top: 0;\n  margin-bottom: ", ";\n"])), space(1.5));
var AuthStatus = styled(Section)(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=organizationMemberRow.jsx.map