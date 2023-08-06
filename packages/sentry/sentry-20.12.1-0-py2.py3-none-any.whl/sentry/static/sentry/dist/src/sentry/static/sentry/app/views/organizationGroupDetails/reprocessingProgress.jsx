import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ProgressBar from 'app/components/progressBar';
import { IconRefresh } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
function ReprocessingProgress(_a) {
    var totalEvents = _a.totalEvents, pendingEvents = _a.pendingEvents;
    var remainingEventsToReprocess = totalEvents - pendingEvents;
    var remainingEventsToReprocessPercent = (remainingEventsToReprocess / totalEvents) * 100;
    // this is a temp solution
    function handleRefresh() {
        window.location.reload();
    }
    return (<Wrapper>
      <Inner>
        <Header>
          <Title>{t('Reprocessing\u2026')}</Title>
          {t('Once the events in this issue have been reprocessed, you’ll be able to make changes and view any new issues that may have been created.')}
        </Header>
        <Content>
          <ProgressBar value={remainingEventsToReprocessPercent} variant="large"/>
          {tct('[remainingEventsToReprocess]/[totalEvents] [event] reprocessed', {
        remainingEventsToReprocess: remainingEventsToReprocess,
        totalEvents: totalEvents,
        event: tn('event', 'events', totalEvents),
    })}
          <Button icon={<IconRefresh />} onClick={handleRefresh}>
            {t('Refresh')}
          </Button>
        </Content>
      </Inner>
    </Wrapper>);
}
export default ReprocessingProgress;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 40px;\n  flex: 1;\n  text-align: center;\n\n  @media (min-width: ", ") {\n    margin: 40px;\n  }\n"], ["\n  margin: ", " 40px;\n  flex: 1;\n  text-align: center;\n\n  @media (min-width: ", ") {\n    margin: 40px;\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[0]; });
var Content = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  max-width: 402px;\n  width: 100%;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n  max-width: 402px;\n  width: 100%;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1.5));
var Inner = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"])), space(3));
var Header = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  color: ", ";\n  max-width: 557px;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  color: ", ";\n  max-width: 557px;\n"])), space(1), function (p) { return p.theme.gray500; });
var Title = styled('h3')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: 0;\n"], ["\n  font-size: ", ";\n  font-weight: 600;\n  margin-bottom: 0;\n"])), function (p) { return p.theme.headerFontSize; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=reprocessingProgress.jsx.map