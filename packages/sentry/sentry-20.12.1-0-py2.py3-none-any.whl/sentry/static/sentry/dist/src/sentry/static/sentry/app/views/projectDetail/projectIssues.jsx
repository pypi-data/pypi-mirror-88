import { __assign, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import GroupList from 'app/components/issues/groupList';
import { Panel, PanelBody } from 'app/components/panels';
import { DEFAULT_RELATIVE_PERIODS, DEFAULT_STATS_PERIOD } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
function ProjectIssues(_a) {
    var organization = _a.organization, location = _a.location;
    function handleOpenClick() {
        trackAnalyticsEvent({
            eventKey: 'project_detail.open_issues',
            eventName: 'Project Detail: Open issues from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function renderEmptyMessage() {
        var _a;
        var selectedTimePeriod = location.query.start
            ? null
            : DEFAULT_RELATIVE_PERIODS[(_a = decodeScalar(location.query.statsPeriod)) !== null && _a !== void 0 ? _a : DEFAULT_STATS_PERIOD];
        var displayedPeriod = selectedTimePeriod
            ? selectedTimePeriod.toLowerCase()
            : t('given timeframe');
        return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {tct('No issues for the [timePeriod].', {
            timePeriod: displayedPeriod,
        })}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
    }
    var endpointPath = "/organizations/" + organization.slug + "/issues/";
    var queryParams = __assign(__assign({ limit: 5 }, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor']))), { query: 'is:unresolved' });
    var issueSearch = {
        pathname: endpointPath,
        query: queryParams,
    };
    return (<React.Fragment>
      <ControlsWrapper>
        <SectionHeading>{t('Project Issues')}</SectionHeading>
        <Button data-test-id="issues-open" size="small" to={issueSearch} onClick={handleOpenClick}>
          {t('Open in Issues')}
        </Button>
      </ControlsWrapper>

      <TableWrapper>
        <GroupList orgId={organization.slug} endpointPath={endpointPath} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={renderEmptyMessage} withChart={false} withPagination/>
      </TableWrapper>
    </React.Fragment>);
}
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(1));
var TableWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default ProjectIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectIssues.jsx.map