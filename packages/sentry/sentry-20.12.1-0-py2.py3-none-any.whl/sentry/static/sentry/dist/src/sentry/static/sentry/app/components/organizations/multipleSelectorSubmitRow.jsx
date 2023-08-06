import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import Button from 'app/components/button';
import { t } from 'app/locale';
import { growIn } from 'app/styles/animations';
import space from 'app/styles/space';
var MultipleSelectorSubmitRow = function (_a) {
    var onSubmit = _a.onSubmit, _b = _a.disabled, disabled = _b === void 0 ? false : _b;
    return (<SubmitButtonContainer>
    <SubmitButton disabled={disabled} onClick={onSubmit} size="xsmall" priority="primary">
      {t('Apply')}
    </SubmitButton>
  </SubmitButtonContainer>);
};
MultipleSelectorSubmitRow.propTypes = {
    onSubmit: PropTypes.func.isRequired,
};
var SubmitButtonContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var SubmitButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  animation: 0.1s ", " ease-in;\n  margin: ", " 0;\n"], ["\n  animation: 0.1s ", " ease-in;\n  margin: ", " 0;\n"])), growIn, space(0.5));
export default MultipleSelectorSubmitRow;
var templateObject_1, templateObject_2;
//# sourceMappingURL=multipleSelectorSubmitRow.jsx.map