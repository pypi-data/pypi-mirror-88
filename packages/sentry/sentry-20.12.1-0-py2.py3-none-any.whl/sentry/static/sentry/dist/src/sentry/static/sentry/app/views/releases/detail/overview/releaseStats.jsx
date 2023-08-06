import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { SectionHeading } from 'app/components/charts/styles';
import Count from 'app/components/count';
import DeployBadge from 'app/components/deployBadge';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import QuestionTooltip from 'app/components/questionTooltip';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getTermHelp } from 'app/views/performance/data';
import { getSessionTermDescription, SessionTerm, sessionTerm, } from 'app/views/releases/utils/sessionTerm';
import { getReleaseEventView } from '../utils';
function ReleaseStats(_a) {
    var _b;
    var organization = _a.organization, release = _a.release, project = _a.project, location = _a.location, selection = _a.selection;
    var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, newGroups = release.newGroups, version = release.version;
    var hasHealthData = project.hasHealthData;
    var sessionsCrashed = project.healthData.sessionsCrashed;
    return (<Container>
      <DateStatWrapper>
        <SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Date Deployed') : t('Date Created')}
        </SectionHeading>
        <div>
          <TimeSince date={(_b = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _b !== void 0 ? _b : dateCreated}/>
        </div>
      </DateStatWrapper>

      <div>
        <SectionHeading>{t('Last Deploy')}</SectionHeading>
        <div>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<DeployBadge deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : ('\u2014')}
        </div>
      </div>

      <div>
        <SectionHeading>{t('New Issues')}</SectionHeading>
        <div>
          <Count value={newGroups}/>
        </div>
      </div>

      <div>
        <SectionHeading>
          {t('Apdex')}
          <QuestionTooltip position="top" title={getTermHelp(organization, 'apdex')} size="sm"/>
        </SectionHeading>
        <div>
          <Feature features={['performance-view']}>
            {function (hasFeature) {
        return hasFeature ? (<DiscoverQuery eventView={getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                  {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            if (isLoading || error || !tableData || tableData.data.length === 0) {
                return '\u2014';
            }
            return (<GlobalSelectionLink to={{
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: {
                    query: "release:" + (release === null || release === void 0 ? void 0 : release.version),
                },
            }}>
                        <Count value={tableData.data[0][getAggregateAlias("apdex(" + organization.apdexThreshold + ")")]}/>
                      </GlobalSelectionLink>);
        }}
                </DiscoverQuery>) : (<Tooltip title={t('This view is only available with Performance Monitoring.')}>
                  {'\u2014'}
                </Tooltip>);
    }}
          </Feature>
        </div>
      </div>

      <div>
        <SectionHeading>
          {sessionTerm.crashes}
          <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASHES, project.platform)} size="sm"/>
        </SectionHeading>
        <div>
          {hasHealthData ? (<Count value={sessionsCrashed}/>) : (<Tooltip title={t('This view is only available with release health data.')}>
              {'\u2014'}
            </Tooltip>)}
        </div>
      </div>
    </Container>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"])), space(2), space(3));
var DateStatWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
export default ReleaseStats;
var templateObject_1, templateObject_2;
//# sourceMappingURL=releaseStats.jsx.map