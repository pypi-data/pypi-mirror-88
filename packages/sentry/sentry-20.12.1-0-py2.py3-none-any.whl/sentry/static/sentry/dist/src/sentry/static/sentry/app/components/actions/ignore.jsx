import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import classNames from 'classnames';
import { openModal } from 'app/actionCreators/modal';
import ActionLink from 'app/components/actions/actionLink';
import Button from 'app/components/button';
import CustomIgnoreCountModal from 'app/components/customIgnoreCountModal';
import CustomIgnoreDurationModal from 'app/components/customIgnoreDurationModal';
import DropdownLink from 'app/components/dropdownLink';
import Duration from 'app/components/duration';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconChevron, IconMute, IconNot } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { ResolutionStatus, } from 'app/types';
var IGNORE_DURATIONS = [30, 120, 360, 60 * 24, 60 * 24 * 7];
var IGNORE_COUNTS = [1, 10, 100, 1000, 10000, 100000];
var IGNORE_WINDOWS = [
    [60, t('per hour')],
    [24 * 60, t('per day')],
    [24 * 7 * 60, t('per week')],
];
var IgnoreActions = function (_a) {
    var onUpdate = _a.onUpdate, disabled = _a.disabled, shouldConfirm = _a.shouldConfirm, confirmMessage = _a.confirmMessage, _b = _a.confirmLabel, confirmLabel = _b === void 0 ? t('Ignore') : _b, _c = _a.isIgnored, isIgnored = _c === void 0 ? false : _c, _d = _a.hasInbox, hasInbox = _d === void 0 ? false : _d;
    var onIgnore = function (statusDetails) {
        return onUpdate({
            status: ResolutionStatus.IGNORED,
            statusDetails: statusDetails || {},
        });
    };
    var onCustomIgnore = function (statusDetails) {
        onIgnore(statusDetails);
    };
    var linkClassName = classNames('btn btn-default btn-sm', {
        active: isIgnored,
    });
    var actionLinkProps = {
        shouldConfirm: shouldConfirm,
        title: t('Ignore'),
        message: confirmMessage,
        confirmLabel: confirmLabel,
        disabled: disabled,
    };
    if (isIgnored) {
        return (<IgnoredButtonActionWrapper>
        <Tooltip title={t('Change status to unresolved')}>
          <StyledIgnoreButton data-test-id="button-unresolve" onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }} icon={<IconNot size="xs"/>}/>
        </Tooltip>
      </IgnoredButtonActionWrapper>);
    }
    var openCustomIgnoreDuration = function () {
        return openModal(function (deps) { return (<CustomIgnoreDurationModal {...deps} onSelected={function (details) { return onCustomIgnore(details); }}/>); });
    };
    var openCustomIngoreCount = function () {
        return openModal(function (deps) { return (<CustomIgnoreCountModal {...deps} onSelected={function (details) { return onCustomIgnore(details); }} label={t('Ignore this issue until it occurs again\u2026')} countLabel={t('Number of times')} countName="ignoreCount" windowName="ignoreWindow" windowChoices={IGNORE_WINDOWS}/>); });
    };
    var openCustomIgnoreUserCount = function () {
        return openModal(function (deps) { return (<CustomIgnoreCountModal {...deps} onSelected={function (details) { return onCustomIgnore(details); }} label={t('Ignore this issue until it affects an additional\u2026')} countLabel={t('Number of users')} countName="ignoreUserCount" windowName="ignoreUserWindow" windowChoices={IGNORE_WINDOWS}/>); });
    };
    return (<IgnoreWrapper>
      <IgnoredButtonActionWrapper>
        {!hasInbox && (<StyledIgnoreActionLink {...actionLinkProps} title={t('Ignore')} className={linkClassName} onAction={function () { return onUpdate({ status: ResolutionStatus.IGNORED }); }}>
            <StyledIconNot size="xs"/>
            {t('Ignore')}
          </StyledIgnoreActionLink>)}

        <StyledDropdownLink caret={!hasInbox} className={linkClassName} customTitle={hasInbox ? <IconMute size="xs" color="gray300"/> : undefined} title="" alwaysRenderMenu disabled={disabled} anchorRight={hasInbox} hasInbox>
          <StyledMenuItem header>Ignore</StyledMenuItem>
          <DropdownMenuItem hasInbox={hasInbox}>
            <DropdownLink title={<ActionSubMenu>
                  {t('For\u2026')}
                  <SubMenuChevron>
                    <IconChevron direction="right" size="xs"/>
                  </SubMenuChevron>
                </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
              {IGNORE_DURATIONS.map(function (duration) { return (<DropdownMenuItem hasInbox={hasInbox} key={duration}>
                  <StyledForActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreDuration: duration }); }}>
                    <ActionSubMenu>
                      <Duration seconds={duration * 60}/>
                    </ActionSubMenu>
                  </StyledForActionLink>
                </DropdownMenuItem>); })}
              <DropdownMenuItem hasInbox={hasInbox}>
                <ActionSubMenu>
                  <a onClick={openCustomIgnoreDuration}>{t('Custom')}</a>
                </ActionSubMenu>
              </DropdownMenuItem>
            </DropdownLink>
          </DropdownMenuItem>
          <DropdownMenuItem hasInbox={hasInbox}>
            <DropdownLink title={<ActionSubMenu>
                  {t('Until this occurs again\u2026')}
                  <SubMenuChevron>
                    <IconChevron direction="right" size="xs"/>
                  </SubMenuChevron>
                </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
              {IGNORE_COUNTS.map(function (count) { return (<DropdownMenuItem hasInbox={hasInbox} key={count}>
                  <DropdownLink title={<ActionSubMenu>
                        {count === 1
        ? t('one time\u2026') // This is intentional as unbalanced string formatters are problematic
        : tn('%s time\u2026', '%s times\u2026', count)}
                        <SubMenuChevron>
                          <IconChevron direction="right" size="xs"/>
                        </SubMenuChevron>
                      </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                    <DropdownMenuItem hasInbox={hasInbox}>
                      <StyledActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreCount: count }); }}>
                        {t('from now')}
                      </StyledActionLink>
                    </DropdownMenuItem>
                    {IGNORE_WINDOWS.map(function (_a) {
        var _b = __read(_a, 2), hours = _b[0], label = _b[1];
        return (<DropdownMenuItem hasInbox={hasInbox} key={hours}>
                        <StyledActionLink {...actionLinkProps} onAction={function () {
            return onIgnore({
                ignoreCount: count,
                ignoreWindow: hours,
            });
        }}>
                          {label}
                        </StyledActionLink>
                      </DropdownMenuItem>);
    })}
                  </DropdownLink>
                </DropdownMenuItem>); })}
              <DropdownMenuItem hasInbox={hasInbox}>
                <ActionSubMenu>
                  <a onClick={openCustomIngoreCount}>{t('Custom')}</a>
                </ActionSubMenu>
              </DropdownMenuItem>
            </DropdownLink>
          </DropdownMenuItem>
          <DropdownMenuItem hasInbox={hasInbox}>
            <DropdownLink title={<ActionSubMenu>
                  {t('Until this affects an additional\u2026')}
                  <SubMenuChevron>
                    <IconChevron direction="right" size="xs"/>
                  </SubMenuChevron>
                </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
              {IGNORE_COUNTS.map(function (count) { return (<DropdownMenuItem hasInbox={hasInbox} key={count}>
                  <DropdownLink title={<ActionSubMenu>
                        {tn('one user\u2026', '%s users\u2026', count)}
                        <SubMenuChevron>
                          <IconChevron direction="right" size="xs"/>
                        </SubMenuChevron>
                      </ActionSubMenu>} caret={false} isNestedDropdown alwaysRenderMenu>
                    <DropdownMenuItem hasInbox={hasInbox}>
                      <StyledActionLink {...actionLinkProps} onAction={function () { return onIgnore({ ignoreUserCount: count }); }}>
                        {t('from now')}
                      </StyledActionLink>
                    </DropdownMenuItem>
                    {IGNORE_WINDOWS.map(function (_a) {
        var _b = __read(_a, 2), hours = _b[0], label = _b[1];
        return (<DropdownMenuItem hasInbox={hasInbox} key={hours}>
                        <StyledActionLink {...actionLinkProps} onAction={function () {
            return onIgnore({
                ignoreUserCount: count,
                ignoreUserWindow: hours,
            });
        }}>
                          {label}
                        </StyledActionLink>
                      </DropdownMenuItem>);
    })}
                  </DropdownLink>
                </DropdownMenuItem>); })}
              <DropdownMenuItem hasInbox={hasInbox}>
                <ActionSubMenu>
                  <a onClick={openCustomIgnoreUserCount}>{t('Custom')}</a>
                </ActionSubMenu>
              </DropdownMenuItem>
            </DropdownLink>
          </DropdownMenuItem>
        </StyledDropdownLink>
      </IgnoredButtonActionWrapper>
    </IgnoreWrapper>);
};
export default IgnoreActions;
// currently needed when the button is disabled on the issue stream (no issues are selected)
// colors can probably be updated to use theme colors based on design
var disabledCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: #ced3d6;\n  border-color: #e3e5e6;\n  box-shadow: none;\n  cursor: default;\n  opacity: 0.65;\n  pointer-events: none;\n"], ["\n  color: #ced3d6;\n  border-color: #e3e5e6;\n  box-shadow: none;\n  cursor: default;\n  opacity: 0.65;\n  pointer-events: none;\n"])));
var actionLinkCss = function (p) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", " !important;\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    border-radius: ", ";\n    background: ", " !important;\n  }\n"])), p.theme.subText, p.theme.borderRadius, p.theme.bodyBackground); };
var dropdownTipCss = function (p) { return css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 44px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"], ["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 44px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"])), p.theme.borderRadius, p.theme.bodyBackground); };
var IgnoreWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: inline-flex;\n  ", ";\n  & span {\n    position: relative;\n  }\n"], ["\n  display: inline-flex;\n  ", ";\n  & span {\n    position: relative;\n  }\n"])), dropdownTipCss);
var IgnoredButtonActionWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-right: 5px;\n  display: inline-flex;\n  align-self: baseline;\n"], ["\n  margin-right: 5px;\n  display: inline-flex;\n  align-self: baseline;\n"])));
var StyledIgnoreButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  vertical-align: middle;\n  color: ", ";\n  background: ", ";\n  border: 1px solid #4538a1;\n  box-shadow: none;\n  & span {\n    padding: 6px 4.5px;\n  }\n  &:hover {\n    background: ", ";\n    color: ", ";\n    border: 1px solid #4538a1;\n  }\n"], ["\n  vertical-align: middle;\n  color: ", ";\n  background: ", ";\n  border: 1px solid #4538a1;\n  box-shadow: none;\n  & span {\n    padding: 6px 4.5px;\n  }\n  &:hover {\n    background: ", ";\n    color: ", ";\n    border: 1px solid #4538a1;\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.white; });
var StyledIgnoreActionLink = styled(ActionLink)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: baseline;\n  float: left;\n  color: #493e54;\n  background-image: linear-gradient(to bottom, ", " 0%, #fcfbfc 100%);\n  background-repeat: repeat-x;\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  font-size: ", ";\n  padding: ", " 9px;\n  border: 1px solid ", ";\n  border-radius: 3px 0 0 3px !important;\n  border-right: 0;\n  font-weight: 600;\n  line-height: 1.5;\n  user-select: none;\n  transition: none;\n  ", ";\n  &:hover {\n    background-color: #e6e6e6;\n    border-radius: 3px;\n    color: ", ";\n    border-color: #afa3bb;\n    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.06);\n  }\n"], ["\n  display: inline-flex;\n  align-items: baseline;\n  float: left;\n  color: #493e54;\n  background-image: linear-gradient(to bottom, ", " 0%, #fcfbfc 100%);\n  background-repeat: repeat-x;\n  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.03);\n  font-size: ", ";\n  padding: ", " 9px;\n  border: 1px solid ", ";\n  border-radius: 3px 0 0 3px !important;\n  border-right: 0;\n  font-weight: 600;\n  line-height: 1.5;\n  user-select: none;\n  transition: none;\n  ", ";\n  &:hover {\n    background-color: #e6e6e6;\n    border-radius: 3px;\n    color: ", ";\n    border-color: #afa3bb;\n    box-shadow: 0 2px 0 rgba(0, 0, 0, 0.06);\n  }\n"])), function (p) { return p.theme.white; }, function (p) { return p.theme.fontSizeSmall; }, space(0.5), function (p) { return p.theme.border; }, function (p) { return (p.disabled ? disabledCss : null); }, function (p) { return p.theme.button.default.color; });
var StyledIconNot = styled(IconNot)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-right: ", ";\n  align-self: center;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  margin-right: ", ";\n  align-self: center;\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(0.5), function (p) { return p.theme.breakpoints[0]; });
var StyledActionLink = styled(ActionLink)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding: 7px 10px !important;\n  ", ";\n"], ["\n  padding: 7px 10px !important;\n  ", ";\n"])), actionLinkCss);
var StyledForActionLink = styled(ActionLink)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  padding: ", " 0;\n  ", ";\n"], ["\n  padding: ", " 0;\n  ", ";\n"])), space(0.5), actionLinkCss);
// The icon with no text label needs the height reduced for row actions
var StyledDropdownLink = styled(DropdownLink)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  ", ";\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"], ["\n  ", ";\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"])), function (p) { return (p.hasInbox ? 'line-height: 0' : ''); });
var DropdownMenuItem = styled('li')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  :not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n  > span {\n    border-radius: ", ";\n    display: block;\n    > ul {\n      border-radius: ", ";\n      top: 5px;\n      left: 100%;\n      margin-top: -5px;\n      margin-left: -1px;\n      &:after,\n      &:before {\n        display: none !important;\n      }\n    }\n  }\n  &:hover > span {\n    background: ", ";\n    border-radius: ", ";\n  }\n  ", ";\n"], ["\n  :not(:first-child) {\n    border-top: 1px solid ", ";\n  }\n  > span {\n    border-radius: ", ";\n    display: block;\n    > ul {\n      border-radius: ", ";\n      top: 5px;\n      left: 100%;\n      margin-top: -5px;\n      margin-left: -1px;\n      &:after,\n      &:before {\n        display: none !important;\n      }\n    }\n  }\n  &:hover > span {\n    background: ", ";\n    border-radius: ", ";\n  }\n  ",
    ";\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.borderRadius; }, function (p) {
    return p.hasInbox &&
        "\n      flex: 1;\n      justify-content: flex-start;\n    ";
});
var StyledMenuItem = styled(MenuItem)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-radius: ", ";\n"], ["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-radius: ", ";\n"])), space(1), space(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.borderRadius; });
var ActionSubMenu = styled('span')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  grid-column-start: 1;\n  grid-column-end: 4;\n  gap: ", ";\n  padding: ", " 0;\n  color: ", ";\n  a {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 200px 1fr;\n  grid-column-start: 1;\n  grid-column-end: 4;\n  gap: ", ";\n  padding: ", " 0;\n  color: ", ";\n  a {\n    color: ", ";\n  }\n"])), space(1), space(0.5), function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var SubMenuChevron = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: grid;\n  align-self: center;\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  align-self: center;\n  color: ", ";\n  transition: 0.1s color linear;\n\n  &:hover,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=ignore.jsx.map