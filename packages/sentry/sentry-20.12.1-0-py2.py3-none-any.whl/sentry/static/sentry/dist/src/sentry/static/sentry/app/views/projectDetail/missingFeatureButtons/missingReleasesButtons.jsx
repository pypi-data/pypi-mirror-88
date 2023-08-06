import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import FeatureTourModal from 'app/components/modals/featureTourModal';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { RELEASES_TOUR_STEPS } from 'app/views/releases/list/releaseLanding';
var DOCS_URL = 'https://docs.sentry.io/product/releases/';
var DOCS_HEALTH_URL = 'https://docs.sentry.io/product/releases/health/';
function MissingReleasesButtons(_a) {
    var organization = _a.organization, health = _a.health, projectId = _a.projectId;
    function handleTourAdvance(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'project_detail.releases_tour.advance',
            eventName: 'Project Detail: Releases Tour Advance',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step: step,
            duration: duration,
        });
    }
    function handleClose(step, duration) {
        trackAnalyticsEvent({
            eventKey: 'project_detail.releases_tour.close',
            eventName: 'Project Detail: Releases Tour Close',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId && parseInt(projectId, 10),
            step: step,
            duration: duration,
        });
    }
    return (<StyledButtonBar gap={1}>
      <Button size="small" priority="primary" external href={health ? DOCS_HEALTH_URL : DOCS_URL}>
        {t('Start Setup')}
      </Button>
      <FeatureTourModal steps={RELEASES_TOUR_STEPS} onAdvance={handleTourAdvance} onCloseModal={handleClose} doneText={t('Start Setup')} doneUrl={health ? DOCS_HEALTH_URL : DOCS_URL}>
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
export default MissingReleasesButtons;
var templateObject_1;
//# sourceMappingURL=missingReleasesButtons.jsx.map