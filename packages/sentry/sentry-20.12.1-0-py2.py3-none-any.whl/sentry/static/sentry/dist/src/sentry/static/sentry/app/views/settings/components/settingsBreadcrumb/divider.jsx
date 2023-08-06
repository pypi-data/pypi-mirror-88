import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconChevron } from 'app/icons';
var Divider = function (_a) {
    var isHover = _a.isHover, isLast = _a.isLast;
    return isLast ? null : (<StyledDivider>
      <StyledIconChevron direction={isHover ? 'down' : 'right'} size="14px"/>
    </StyledDivider>);
};
var StyledIconChevron = styled(IconChevron)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n"], ["\n  display: block;\n"])));
var StyledDivider = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  margin-left: 6px;\n  color: ", ";\n  position: relative;\n"], ["\n  display: inline-block;\n  margin-left: 6px;\n  color: ", ";\n  position: relative;\n"])), function (p) { return p.theme.gray200; });
export default Divider;
var templateObject_1, templateObject_2;
//# sourceMappingURL=divider.jsx.map