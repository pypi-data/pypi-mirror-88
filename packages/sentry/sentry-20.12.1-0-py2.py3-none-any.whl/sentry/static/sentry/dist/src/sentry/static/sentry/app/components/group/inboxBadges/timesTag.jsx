import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import TimeSince from 'app/components/timeSince';
import { IconClock } from 'app/icons';
import { t } from 'app/locale';
var TimesTag = function (_a) {
    var lastSeen = _a.lastSeen, firstSeen = _a.firstSeen;
    return (<Wrapper>
      <StyledIconClock size="xs" color="gray300"/>
      {lastSeen && (<TimeSince tooltipTitle={t('Last Seen')} date={lastSeen} suffix={t('ago')} shorten/>)}
      {firstSeen && lastSeen && (<Seperator className="hidden-xs hidden-sm">&nbsp;|&nbsp;</Seperator>)}
      {firstSeen && (<TimeSince tooltipTitle={t('First Seen')} date={firstSeen} suffix={t('old')} className="hidden-xs hidden-sm" shorten/>)}
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  font-size: ", ";\n"], ["\n  display: flex;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var Seperator = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledIconClock = styled(IconClock)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: 2px;\n"], ["\n  margin-right: 2px;\n"])));
export default TimesTag;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=timesTag.jsx.map