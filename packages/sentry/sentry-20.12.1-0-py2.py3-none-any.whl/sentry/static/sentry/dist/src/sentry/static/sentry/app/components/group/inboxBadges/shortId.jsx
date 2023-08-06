import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
var ShortId = function (_a) {
    var shortId = _a.shortId, avatar = _a.avatar;
    return (<Wrapper>
    <AvatarWrapper>{avatar}</AvatarWrapper>
    <IdWrapper>{shortId}</IdWrapper>
  </Wrapper>);
};
export default ShortId;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  font-size: ", ";\n"], ["\n  display: flex;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraSmall; });
var AvatarWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: 3px;\n  flex-shrink: 0;\n"], ["\n  margin-right: 3px;\n  flex-shrink: 0;\n"])));
var IdWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  margin-top: 1px;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  margin-top: 1px;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=shortId.jsx.map