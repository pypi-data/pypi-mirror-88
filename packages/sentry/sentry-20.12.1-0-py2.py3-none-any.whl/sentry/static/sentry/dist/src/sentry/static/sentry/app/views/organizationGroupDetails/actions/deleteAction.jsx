import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Button from 'app/components/button';
import DropdownLink from 'app/components/dropdownLink';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import MenuItem from 'app/components/menuItem';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
function DeleteAction(_a) {
    var disabled = _a.disabled, project = _a.project, organization = _a.organization, onDiscard = _a.onDiscard, onDelete = _a.onDelete;
    function renderDiscardDisabled(_a) {
        var children = _a.children, props = __rest(_a, ["children"]);
        return children(__assign(__assign({}, props), { renderDisabled: function (_a) {
                var features = _a.features;
                return (<FeatureDisabled alert featureName="Discard and Delete" features={features}/>);
            } }));
    }
    function renderDiscardModal(_a) {
        var Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal;
        return (<Feature features={['projects:discard-groups']} hookName="feature-disabled:discard-groups" organization={organization} project={project} renderDisabled={renderDiscardDisabled}>
        {function (_a) {
            var hasFeature = _a.hasFeature, renderDisabled = _a.renderDisabled, props = __rest(_a, ["hasFeature", "renderDisabled"]);
            return (<React.Fragment>
            <Body>
              {!hasFeature &&
                typeof renderDisabled === 'function' &&
                renderDisabled(__assign(__assign({}, props), { hasFeature: hasFeature, children: null }))}
              {t("Discarding this event will result in the deletion of most data associated with this issue and future events being discarded before reaching your stream. Are you sure you wish to continue?")}
            </Body>
            <Footer>
              <Button onClick={closeModal}>{t('Cancel')}</Button>
              <Button style={{ marginLeft: space(1) }} priority="primary" onClick={onDiscard} disabled={!hasFeature}>
                {t('Discard Future Events')}
              </Button>
            </Footer>
          </React.Fragment>);
        }}
      </Feature>);
    }
    function openDiscardModal() {
        openModal(renderDiscardModal);
        analytics('feature.discard_group.modal_opened', {
            org_id: parseInt(organization.id, 10),
        });
    }
    return (<DeleteDiscardWrapper>
      <StyledLinkWithConfirmation className="group-remove btn btn-default btn-sm" title={t('Delete')} message={t('Deleting this issue is permanent. Are you sure you wish to continue?')} onConfirm={onDelete} disabled={disabled}>
        <IconWrapper>
          <IconDelete size="xs"/>
        </IconWrapper>
      </StyledLinkWithConfirmation>
      <StyledDropdownLink title="" caret className="group-delete btn btn-default btn-sm" disabled={disabled}>
        <StyledMenuItemHeader header>{t('Delete & Discard')}</StyledMenuItemHeader>
        <StyledMenuItem onClick={openDiscardModal}>
          <span>{t('Delete and discard future events')}</span>
        </StyledMenuItem>
      </StyledDropdownLink>
    </DeleteDiscardWrapper>);
}
export default DeleteAction;
var dropdownTipCss = function (p) { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 40px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"], ["\n  & ul {\n    padding: 0;\n    border-radius: ", ";\n    top: 40px;\n    &:after {\n      border-bottom: 8px solid ", ";\n    }\n  }\n"])), p.theme.borderRadius, p.theme.bodyBackground); };
var IconWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var StyledMenuItemHeader = styled(MenuItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-top-left-radius: ", ";\n  border-top-right-radius: ", ";\n"], ["\n  text-transform: uppercase;\n  padding: ", " 0 ", " 10px;\n  font-weight: 600;\n  color: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-top-left-radius: ", ";\n  border-top-right-radius: ", ";\n"])), space(1), space(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var StyledMenuItem = styled(MenuItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  & span {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n    padding: 5px;\n  }\n  & span:hover {\n    background: ", ";\n  }\n"], ["\n  & span {\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n    text-overflow: ellipsis;\n    white-space: nowrap;\n    overflow: hidden;\n    padding: 5px;\n  }\n  & span:hover {\n    background: ", ";\n  }\n"])), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.bodyBackground; });
var StyledDropdownLink = styled(DropdownLink)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"], ["\n  transition: none;\n  border-top-left-radius: 0 !important;\n  border-bottom-left-radius: 0 !important;\n"])));
var StyledLinkWithConfirmation = styled(LinkWithConfirmation)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  border-top-right-radius: 0 !important;\n  border-bottom-right-radius: 0 !important;\n  border-right: 0;\n"], ["\n  border-top-right-radius: 0 !important;\n  border-bottom-right-radius: 0 !important;\n  border-right: 0;\n"])));
var DeleteDiscardWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: inline-block;\n  margin-right: 5px;\n  ", "\n  & span {\n    position: relative;\n  }\n"], ["\n  display: inline-block;\n  margin-right: 5px;\n  ", "\n  & span {\n    position: relative;\n  }\n"])), dropdownTipCss);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=deleteAction.jsx.map