import React from 'react';
import IssueList from 'app/components/issueList';
import { t } from 'app/locale';
var MonitorIssues = function (_a) {
    var orgId = _a.orgId, monitor = _a.monitor;
    return (<IssueList endpoint={"/organizations/" + orgId + "/issues/"} query={{
        query: 'monitor.id:"' + monitor.id + '"',
        project: monitor.project.id,
        limit: 5,
    }} statsPeriod="0" pagination={false} emptyText={t('No issues found')} showActions={false} noBorder noMargin params={{ orgId: orgId }}/>);
};
export default MonitorIssues;
//# sourceMappingURL=monitorIssues.jsx.map