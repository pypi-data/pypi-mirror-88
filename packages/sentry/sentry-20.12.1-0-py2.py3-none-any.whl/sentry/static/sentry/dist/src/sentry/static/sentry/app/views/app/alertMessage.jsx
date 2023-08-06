import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AlertActions from 'app/actions/alertActions';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { IconCheckmark, IconClose, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var AlertMessage = function (_a) {
    var alert = _a.alert, system = _a.system;
    var handleCloseAlert = function () {
        AlertActions.closeAlert(alert);
    };
    var url = alert.url, message = alert.message, type = alert.type;
    var icon = type === 'success' ? (<IconCheckmark size="md" isCircled/>) : (<IconWarning size="md"/>);
    return (<StyledAlert type={type} icon={icon} system={system}>
      <StyledMessage>
        {url ? <ExternalLink href={url}>{message}</ExternalLink> : message}
      </StyledMessage>
      <StyledCloseButton icon={<IconClose size="md" isCircled/>} aria-label={t('Close')} onClick={handleCloseAlert} size="zero" borderless/>
    </StyledAlert>);
};
export default AlertMessage;
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  margin: 0;\n"], ["\n  padding: ", " ", ";\n  margin: 0;\n"])), space(1), space(2));
var StyledMessage = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin: auto ", " auto 0;\n"], ["\n  display: block;\n  margin: auto ", " auto 0;\n"])), space(4));
var StyledCloseButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: transparent;\n  opacity: 0.4;\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 50%;\n  right: 0;\n  transform: translateY(-50%);\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"], ["\n  background-color: transparent;\n  opacity: 0.4;\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 50%;\n  right: 0;\n  transform: translateY(-50%);\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=alertMessage.jsx.map