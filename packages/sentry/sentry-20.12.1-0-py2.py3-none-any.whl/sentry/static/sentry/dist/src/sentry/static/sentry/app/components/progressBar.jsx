import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
var getVariantStyle = function (_a) {
    var _b = _a.variant, variant = _b === void 0 ? 'small' : _b, theme = _a.theme;
    if (variant === 'large') {
        return "\n      height: 24px;\n      border-radius: 24px;\n      border: 1px solid " + theme.border + ";\n      box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.06);\n      :before {\n        left: 6px;\n        right: 6px;\n        height: 14px;\n        top: calc(50% - 14px/2);\n        border-radius: 20px;\n        max-width: calc(100% - 12px);\n      }\n    ";
    }
    return "\n    height: 6px;\n    border-radius: 100px;\n    background: " + theme.gray100 + ";\n    :before {\n      top: 0;\n      left: 0;\n      height: 100%;\n    }\n  ";
};
var ProgressBar = styled(function (_a) {
    var className = _a.className, value = _a.value;
    return (<div role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={100} className={className}/>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  :before {\n    content: ' ';\n    width: ", "%;\n    background-color: ", ";\n    position: absolute;\n  }\n\n  ", ";\n"], ["\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  :before {\n    content: ' ';\n    width: ", "%;\n    background-color: ", ";\n    position: absolute;\n  }\n\n  ", ";\n"])), function (p) { return p.value; }, function (p) { return p.theme.purple300; }, getVariantStyle);
export default ProgressBar;
var templateObject_1;
//# sourceMappingURL=progressBar.jsx.map