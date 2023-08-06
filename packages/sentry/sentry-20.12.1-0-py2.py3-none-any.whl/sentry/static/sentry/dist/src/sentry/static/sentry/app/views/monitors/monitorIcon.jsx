import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
export default styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  height: ", "px;\n  width: ", "px;\n\n  ", ";\n"], ["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  height: ", "px;\n  width: ", "px;\n\n  ",
    ";\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) {
    return p.color
        ? "background: " + p.color + ";"
        : "background: " + (p.status === 'error'
            ? p.theme.error
            : p.status === 'ok'
                ? p.theme.success
                : p.theme.disabled) + ";";
});
var templateObject_1;
//# sourceMappingURL=monitorIcon.jsx.map