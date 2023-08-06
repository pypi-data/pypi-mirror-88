import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import ProjectOwnershipModal from 'app/views/settings/project/projectOwnership/modal';
var CreateOwnershipRuleModal = function (_a) {
    var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal, props = __rest(_a, ["Body", "Header", "closeModal"]);
    var handleSuccess = function () {
        var _a;
        (_a = props.onClose) === null || _a === void 0 ? void 0 : _a.call(props);
        window.setTimeout(closeModal, 2000);
    };
    return (<React.Fragment>
      <Header closeButton onHide={closeModal}>
        {t('Create Ownership Rule')}
      </Header>
      <Body>
        <ProjectOwnershipModal {...props} onSave={handleSuccess}/>
      </Body>
    </React.Fragment>);
};
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 80%;\n      margin-left: -40%;\n    }\n  }\n  .modal-content {\n    overflow: initial;\n  }\n"], ["\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 80%;\n      margin-left: -40%;\n    }\n  }\n  .modal-content {\n    overflow: initial;\n  }\n"])), theme.breakpoints[0]);
export default CreateOwnershipRuleModal;
var templateObject_1;
//# sourceMappingURL=createOwnershipRuleModal.jsx.map