import { __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import ApiForm from 'app/components/forms/apiForm';
import NumberField from 'app/components/forms/numberField';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
var impacts = [
    tct('[strong:Reprocessing creates new events.] This may temporarily affect event counts in both Discover and the Issue Stream.', { strong: <strong /> }),
    tct('[strong:Store Native crash reports to reprocess Minidump crash reports.] Note that this requires attachment storage.', { strong: <strong /> }),
    tct('[strong:Reprocessed events count towards your organization’s quota.] Rate limits and spike protection don’t apply to reprocessed events.', { strong: <strong /> }),
    t('Please wait one hour before attempting to reprocess missing debug files.'),
    t('Reprocessed events will not trigger issue alerts, and reprocessed events are not subject to data forwarding.'),
];
function ReprocessingDialogForm(_a) {
    var orgSlug = _a.orgSlug, group = _a.group, project = _a.project, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal;
    var endpoint = "/organizations/" + orgSlug + "/issues/" + group.id + "/reprocessing/";
    var title = t('Reprocess Events');
    function handleSuccess() {
        var _a;
        var hasReprocessingV2Feature = !!((_a = project.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2'));
        if (hasReprocessingV2Feature) {
            closeModal();
            window.location.reload();
            return;
        }
        browserHistory.push("/organizations/" + orgSlug + "/issues/?query=reprocessing.original_issue_id:" + group.id + "/");
    }
    return (<React.Fragment>
      <Header closeButton>{title}</Header>
      <Body>
        <Introduction>
          {t('Reprocessing applies any new debug files or grouping configuration to an Issue. Before you give it a try, you should probably consider these impacts:')}
        </Introduction>
        <StyledList symbol="bullet">
          {impacts.map(function (impact, index) { return (<ListItem key={index}>{impact}</ListItem>); })}
        </StyledList>
        <ApiForm apiEndpoint={endpoint} apiMethod="POST" footerClass="modal-footer" onSubmitSuccess={handleSuccess} submitLabel={title} submitLoadingMessage={t('Reprocessing\u2026')} submitErrorMessage={t('Failed to reprocess. Please check your input.')} onCancel={closeModal}>
          <NumberField name="maxEvents" label={t('Enter the number of events to be reprocessed')} help={t('You can limit the number of events reprocessed in this Issue. If you set a limit, we will reprocess your most recent events.')} placeholder={t('Reprocess all events')} min={1}/>
        </ApiForm>
      </Body>
    </React.Fragment>);
}
export default ReprocessingDialogForm;
var Introduction = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(1), space(4), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessingDialogForm.jsx.map