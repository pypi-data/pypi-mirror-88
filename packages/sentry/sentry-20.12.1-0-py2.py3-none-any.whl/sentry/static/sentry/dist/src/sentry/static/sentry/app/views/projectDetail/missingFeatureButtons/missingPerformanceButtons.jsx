import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import FeatureTourModal from 'app/components/modals/featureTourModal';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { PERFORMANCE_TOUR_STEPS } from 'app/views/performance/onboarding';
var DOCS_URL = 'https://docs.sentry.io/performance-monitoring/getting-started/';
function MissingPerformanceButtons(_a) {
    var organization = _a.organization;
    function handleTourAdvance(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'project_detail.performance_tour.advance',
            eventName: 'Project Detail: Performance Tour Advance',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'project_detail.performance_tour.close',
            eventName: 'Project Detail: Performance Tour Close',
            organization_id: parseInt(organization.id, 10),
            step: step,
            duration: duration,
        });
    }
    return (<StyledButtonBar gap={1}>
      <Button size="small" priority="primary" external href={DOCS_URL}>
        {t('Start Setup')}
      </Button>

      <FeatureTourModal steps={PERFORMANCE_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={t('Start Setup')} doneUrl={DOCS_URL}>
        {function (_a) {
        var showModal = _a.showModal;
        return (<Button size="small" onClick={showModal}>
            {t('Get a tour')}
          </Button>);
    }}
      </FeatureTourModal>
    </StyledButtonBar>);
}
var StyledButtonBar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"], ["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"])));
export default MissingPerformanceButtons;
var templateObject_1;
//# sourceMappingURL=missingPerformanceButtons.jsx.map