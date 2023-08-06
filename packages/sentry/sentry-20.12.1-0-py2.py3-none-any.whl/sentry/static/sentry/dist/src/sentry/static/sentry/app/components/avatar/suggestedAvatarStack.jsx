import { __assign, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import BaseAvatar from 'app/components/avatar/baseAvatar';
// Constrain the number of visible suggestions
var MAX_SUGGESTIONS = 5;
var SuggestedAvatarStack = function (_a) {
    var owners = _a.owners, props = __rest(_a, ["owners"]);
    var backgroundAvatarProps = __assign(__assign({}, props), { round: owners[0].type === 'user', suggested: true });
    var numAvatars = Math.min(owners.length, MAX_SUGGESTIONS);
    return (<AvatarStack>
      {__spread(Array(numAvatars - 1)).map(function (_, i) { return (<BackgroundAvatar {...backgroundAvatarProps} key={i} type="background" index={i}/>); })}
      <Avatar {...props} suggested actor={owners[0]} index={numAvatars - 1} hasTooltip={false}/>
    </AvatarStack>);
};
var AvatarStack = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-content: center;\n  flex-direction: row-reverse;\n"], ["\n  display: flex;\n  align-content: center;\n  flex-direction: row-reverse;\n"])));
var translateStyles = function (props) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transform: translateX(", "%);\n"], ["\n  transform: translateX(", "%);\n"])), 60 * props.index); };
var Avatar = styled(ActorAvatar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), translateStyles);
var BackgroundAvatar = styled(BaseAvatar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), translateStyles);
export default SuggestedAvatarStack;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=suggestedAvatarStack.jsx.map