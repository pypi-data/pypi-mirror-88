import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import { openModal } from 'app/actionCreators/modal';
import ActionLink from 'app/components/actions/actionLink';
import Button from 'app/components/button';
import CustomResolutionModal from 'app/components/customResolutionModal';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { ResolutionStatus, } from 'app/types';
import { formatVersion } from 'app/utils/formatters';
var defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: t('Resolve'),
    hasInbox: false,
};
var ResolveActions = /** @class */ (function (_super) {
    __extends(ResolveActions, _super);
    function ResolveActions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResolveActions.prototype.onCustomResolution = function (statusDetails) {
        this.props.onUpdate({
            status: ResolutionStatus.RESOLVED,
            statusDetails: statusDetails,
        });
    };
    ResolveActions.prototype.getButtonClass = function (otherClasses) {
        return classNames('btn btn-default btn-sm', otherClasses);
    };
    ResolveActions.prototype.renderResolved = function () {
        var _a = this.props, isAutoResolved = _a.isAutoResolved, onUpdate = _a.onUpdate;
        if (isAutoResolved) {
            return (<ResolvedActionWrapper>
          <Tooltip title={t('This event is resolved due to the Auto Resolve configuration for this project')}>
            <StyledResolveButton data-test-id="button-unresolve" icon={<IconCheckmark size="xs"/>}/>
          </Tooltip>
        </ResolvedActionWrapper>);
        }
        else {
            return (<ResolvedActionWrapper>
          <Tooltip title={t('Unresolve')}>
            <StyledResolveButton data-test-id="button-unresolve" icon={<IconCheckmark size="xs"/>} onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }}/>
          </Tooltip>
        </ResolvedActionWrapper>);
        }
    };
    ResolveActions.prototype.renderDropdownMenu = function () {
        var _this = this;
        var _a = this.props, projectId = _a.projectId, isResolved = _a.isResolved, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, disableDropdown = _a.disableDropdown, hasInbox = _a.hasInbox;
        var buttonClass = this.getButtonClass();
        if (isResolved) {
            return this.renderResolved();
        }
        var actionTitle = !hasRelease
            ? t('Set up release tracking in order to use this feature.')
            : '';
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<ResolveWrapper hasInbox={hasInbox}>
        <StyledDropdownLink key="resolve-dropdown" caret={!hasInbox} className={hasInbox ? undefined : buttonClass} title={hasInbox ? t('Resolve In\u2026') : ''} alwaysRenderMenu disabled={!projectId ? disabled : disableDropdown} anchorRight={hasInbox} isNestedDropdown={hasInbox}>
          <StyledMenuItem header>{t('Resolved In')}</StyledMenuItem>
          <StyledTooltip title={actionTitle} containerDisplayMode="block">
            <StyledActionLink {...actionLinkProps} title={t('The next release')} onAction={function () {
            return hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inNextRelease: true,
                    },
                });
        }}>
              {t('The next release')}
            </StyledActionLink>
          </StyledTooltip>
          <StyledTooltip title={actionTitle} containerDisplayMode="block">
            <StyledActionLink {...actionLinkProps} title={t('The current release')} onAction={function () {
            return hasRelease &&
                onUpdate({
                    status: ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inRelease: latestRelease ? latestRelease.version : 'latest',
                    },
                });
        }}>
              {latestRelease
            ? t('The current release (%s)', formatVersion(latestRelease.version))
            : t('The current release')}
            </StyledActionLink>
          </StyledTooltip>
          <StyledTooltip title={actionTitle} containerDisplayMode="block">
            <StyledActionLink {...actionLinkProps} title={t('Another version')} onAction={function () { return hasRelease && _this.openCustomReleaseModal(); }} shouldConfirm={false}>
              {t('Another version\u2026')}
            </StyledActionLink>
          </StyledTooltip>
        </StyledDropdownLink>
      </ResolveWrapper>);
    };
    ResolveActions.prototype.openCustomReleaseModal = function () {
        var _this = this;
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId;
        openModal(function (deps) { return (<CustomResolutionModal {...deps} onSelected={function (statusDetails) {
            return _this.onCustomResolution(statusDetails);
        }} orgId={orgId} projectId={projectId}/>); });
    };
    ResolveActions.prototype.render = function () {
        var _a = this.props, isResolved = _a.isResolved, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, projectFetchError = _a.projectFetchError, hasInbox = _a.hasInbox;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<ResolveWrapper hasInbox={hasInbox}>
        <Tooltip disabled={!projectFetchError} title={t('Error fetching project')}>
          {hasInbox ? (<div style={{ width: '100%' }}>
              <div className="dropdown-submenu flex expand-left">
                {this.renderDropdownMenu()}
              </div>
            </div>) : (<ResolvedActionWrapper>
              <StyledResolveActionLink {...actionLinkProps} title={t('Resolve')} disabled={disabled} onAction={function () { return onUpdate({ status: ResolutionStatus.RESOLVED }); }}>
                <StyledIconCheckmark size="xs"/>
                {t('Resolve')}
              </StyledResolveActionLink>
              {this.renderDropdownMenu()}
            </ResolvedActionWrapper>)}
        </Tooltip>
      </ResolveWrapper>);
    };
    ResolveActions.propTypes = {
        hasRelease: PropTypes.bool.isRequired,
        latestRelease: PropTypes.object,
        onUpdate: PropTypes.func.isRequired,
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string,
        shouldConfirm: PropTypes.bool,
        confirmMessage: PropTypes.node,
        disabled: PropTypes.bool,
        disableDropdown: PropTypes.bool,
        isResolved: PropTypes.bool,
        isAutoResolved: PropTypes.bool,
        confirmLabel: PropTypes.string,
        projectFetchError: PropTypes.bool,
    };
    ResolveActions.defaultProps = defaultProps;
    return ResolveActions;
}(React.Component));
// currently needed when the button is disabled on the issue stream (no issues are selected)
// colors can probably be updated to use theme colors based on design
var disabledCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: #ced3d6;\n  border-color: #e3e5e6;\n  box-shadow: none;\n  cursor: default;\n  opacity: 0.65;\n  pointer-events: none;\n  background: none !important;\n"], ["\n  color: #ced3d6;\n  border-color: #e3e5e6;\n  box-shadow: none;\n  cursor: default;\n  opacity: 0.65;\n  pointer-events: none;\n  background: none !important;\n"])));
var dropdownTipCss = function (p) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 44px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"], ["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 44px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"])), p.theme.borderRadius, p.theme.bodyBackground); };
var actionLinkCss = function (p) { return css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", ";\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", ";\n    color: ", ";\n  }\n"])), p.theme.subText, p.theme.borderRadius, p.theme.bodyBackground, p.theme.textColor); };
var ResolvedActionWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: 5px;\n  display: inline-flex;\n"], ["\n  margin-right: 5px;\n  display: inline-flex;\n"])));
var ResolveWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: inline-flex;\n  align-self: baseline;\n  ", ";\n  & span {\n    position: relative;\n  }\n  width: ", ";\n"], ["\n  display: inline-flex;\n  align-self: baseline;\n  ", ";\n  & span {\n    position: relative;\n  }\n  width: ", ";\n"])), dropdownTipCss, function (p) { return (p.hasInbox ? '100%' : 'auto'); });
var StyledIconCheckmark = styled(IconCheckmark)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: ", ";\n  align-self: center;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  margin-right: ", ";\n  align-self: center;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; });
var StyledResolveButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-flex;\n  vertical-align: middle;\n  color: ", ";\n  background: ", ";\n  border: 1px solid #4538a1;\n  box-shadow: none;\n  & span {\n    padding: 6px 4.5px;\n  }\n  &:hover {\n    background: ", ";\n    color: ", ";\n    border: 1px solid #4538a1;\n  }\n  ", ";\n"], ["\n  display: inline-flex;\n  vertical-align: middle;\n  color: ", ";\n  background: ", ";\n  border: 1px solid #4538a1;\n  box-shadow: none;\n  & span {\n    padding: 6px 4.5px;\n  }\n  &:hover {\n    background: ", ";\n    color: ", ";\n    border: 1px solid #4538a1;\n  }\n  ", ";\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.white; }, function (p) { return (!p.onClick ? 'pointer-events: none' : null); });
var StyledResolveActionLink = styled(ActionLink)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  float: left;\n  color: #493e54;\n  background-image: linear-gradient(to bottom, ", " 0%, #fcfbfc 100%);\n  background-repeat: repeat-x;\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  font-size: ", ";\n  padding: ", " 9px;\n  border: 1px solid ", ";\n  border-radius: 3px 0 0 3px !important;\n  border-right: 0;\n  font-weight: 600;\n  line-height: 1.5;\n  user-select: none;\n  transition: none;\n  ", ";\n  &:hover {\n    background-color: #e6e6e6;\n    border-radius: 3px;\n    color: ", ";\n    border-color: #afa3bb;\n    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.06);\n  }\n"], ["\n  display: flex;\n  float: left;\n  color: #493e54;\n  background-image: linear-gradient(to bottom, ", " 0%, #fcfbfc 100%);\n  background-repeat: repeat-x;\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  font-size: ", ";\n  padding: ", " 9px;\n  border: 1px solid ", ";\n  border-radius: 3px 0 0 3px !important;\n  border-right: 0;\n  font-weight: 600;\n  line-height: 1.5;\n  user-select: none;\n  transition: none;\n  ", ";\n  &:hover {\n    background-color: #e6e6e6;\n    border-radius: 3px;\n    color: ", ";\n    border-color: #afa3bb;\n    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.06);\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeSmall; }, space(0.5), function (p) { return p.theme.border; }, function (p) { return (p.disabled ? disabledCss : null); }, function (p) { return p.theme.button.default.color; });
var StyledMenuItem = styled(MenuItem)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-radius: ", ";\n"], ["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-radius: ", ";\n"])), space(1), space(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.borderRadius; });
var StyledTooltip = styled(Tooltip)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  :not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n  > span {\n    border-radius: ", ";\n    display: block;\n  }\n  &:hover > span {\n    background: ", ";\n    border-radius: ", ";\n  }\n"], ["\n  :not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n  > span {\n    border-radius: ", ";\n    display: block;\n  }\n  &:hover > span {\n    background: ", ";\n    border-radius: ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.borderRadius; });
var StyledActionLink = styled(ActionLink)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n  color: ", " !important;\n  padding: ", " 10px ", " 10px;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  overflow: hidden;\n  ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n  color: ", " !important;\n  padding: ", " 10px ", " 10px;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  overflow: hidden;\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space(1), space(1), actionLinkCss);
var StyledDropdownLink = styled(DropdownLink)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n  ", ";\n"], ["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n  ", ";\n"])), function (p) { return (p.disabled ? disabledCss : null); });
export default ResolveActions;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=resolve.jsx.map