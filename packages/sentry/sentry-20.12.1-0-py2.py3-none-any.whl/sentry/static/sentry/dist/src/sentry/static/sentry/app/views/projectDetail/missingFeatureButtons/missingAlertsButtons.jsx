import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import { t } from 'app/locale';
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/';
function MissingAlertsButtons(_a) {
    var organization = _a.organization, projectSlug = _a.projectSlug;
    return (<StyledButtonBar gap={1}>
      <CreateAlertButton organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="project_detail" projectSlug={projectSlug} hideIcon>
        {t('Create Alert')}
      </CreateAlertButton>
      <Button size="small" external href={DOCS_URL}>
        {t('Learn More')}
      </Button>
    </StyledButtonBar>);
}
var StyledButtonBar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"], ["\n  grid-template-columns: minmax(auto, max-content) minmax(auto, max-content);\n"])));
export default MissingAlertsButtons;
var templateObject_1;
//# sourceMappingURL=missingAlertsButtons.jsx.map