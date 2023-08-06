import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel, PanelBody } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function ScoreCard(_a) {
    var title = _a.title, score = _a.score, help = _a.help, trend = _a.trend, trendStyle = _a.trendStyle, className = _a.className;
    return (<StyledPanel className={className}>
      <PanelBody withPadding>
        <TitleWrapper>
          <Title>{title}</Title>

          {help && <StyledQuestionTooltip title={help} size="sm" position="top"/>}
        </TitleWrapper>

        <ScoreWrapper>
          <Score>{score !== null && score !== void 0 ? score : '\u2014'}</Score>

          {trend && <Trend trendStyle={trendStyle}>{trend}</Trend>}
        </ScoreWrapper>
      </PanelBody>
    </StyledPanel>);
}
function getTrendColor(p) {
    switch (p.trendStyle) {
        case 'good':
            return p.theme.green300;
        case 'bad':
            return p.theme.red300;
        default:
            return p.theme.blue300;
    }
}
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var TitleWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: ", ";\n"])), space(2));
var Title = styled('h3')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  margin-bottom: 0 !important;\n  ", ";\n  width: auto;\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  margin-bottom: 0 !important;\n  ", ";\n  width: auto;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, overflowEllipsis);
var StyledQuestionTooltip = styled(QuestionTooltip)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var ScoreWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n"], ["\n  display: flex;\n  align-items: baseline;\n"])));
var Score = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: 36px;\n"], ["\n  font-size: 36px;\n"])));
var Trend = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  margin-left: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  margin-left: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, getTrendColor, space(1), overflowEllipsis);
export default ScoreCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=scoreCard.jsx.map