import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import ScoreCard from 'app/components/scoreCard';
import { t } from 'app/locale';
import space from 'app/styles/space';
var ProjectScoreCards = /** @class */ (function (_super) {
    __extends(ProjectScoreCards, _super);
    function ProjectScoreCards() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectScoreCards.prototype.renderBody = function () {
        return (<CardWrapper>
        <ScoreCard title={t('Stability Score')} help={t('Stability score is used to ...')} score="94.1%" trend="+13.5%" trendStyle="good"/>
        <ScoreCard title={t('Velocity Score')} help={t('Velocity score is used to ...')} score="16" trend="-2 releases / 2 wks" trendStyle="bad"/>
        <ScoreCard title={t('Apdex Score')} help={t('Apdex score is used to ...')} score="0.95" trend="+0.2" trendStyle="good"/>
      </CardWrapper>);
    };
    return ProjectScoreCards;
}(AsyncComponent));
var CardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: 1fr 1fr 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: 1fr 1fr 1fr;\n  }\n"])), space(2), space(3), function (p) { return p.theme.breakpoints[0]; });
export default ProjectScoreCards;
var templateObject_1;
//# sourceMappingURL=projectScoreCards.jsx.map