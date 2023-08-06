import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { imageStyle } from 'app/components/avatar/styles';
import theme from 'app/utils/theme';
/**
 * Creates an avatar placeholder that is used when showing multiple
 * suggested assignees
 */
var BackgroundAvatar = styled(function (_a) {
    var _round = _a.round, forwardedRef = _a.forwardedRef, props = __rest(_a, ["round", "forwardedRef"]);
    return (<svg ref={forwardedRef} viewBox="0 0 120 120" {...props}>
      <rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={theme.purple100}/>
    </svg>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), imageStyle);
BackgroundAvatar.defaultProps = {
    round: false,
    suggested: true,
};
export default React.forwardRef(function (props, ref) { return (<BackgroundAvatar forwardedRef={ref} {...props}/>); });
var templateObject_1;
//# sourceMappingURL=backgroundAvatar.jsx.map