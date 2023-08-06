import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import theme from 'app/utils/theme';
export var imageStyle = function (props) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0px;\n  left: 0px;\n  border-radius: ", ";\n  border: ", ";\n  ", "\n"], ["\n  position: absolute;\n  top: 0px;\n  left: 0px;\n  border-radius: ", ";\n  border: ", ";\n  ",
    "\n"])), props.round ? '50%' : '3px', props.suggested ? "1px dashed " + theme.gray400 : 'none', props.grayscale && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    padding: 1px;\n    filter: grayscale(100%);\n  "], ["\n    padding: 1px;\n    filter: grayscale(100%);\n  "])))); };
var templateObject_1, templateObject_2;
//# sourceMappingURL=styles.jsx.map