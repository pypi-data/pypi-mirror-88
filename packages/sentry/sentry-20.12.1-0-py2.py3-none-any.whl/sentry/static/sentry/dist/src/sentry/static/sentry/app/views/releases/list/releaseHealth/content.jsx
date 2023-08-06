import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Count from 'app/components/count';
import Link from 'app/components/links/link';
import { PanelItem } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import ProgressBar from 'app/components/progressBar';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { getReleaseNewIssuesUrl } from '../../utils';
import AdoptionTooltip from '../adoptionTooltip';
import ClippedHealthRows from '../clippedHealthRows';
import CrashFree from '../crashFree';
import HealthStatsChart from '../healthStatsChart';
import HealthStatsPeriod from '../healthStatsPeriod';
import NotAvailable from '../notAvailable';
import { DisplayOption } from '../utils';
import Header from './header';
import ProjectName from './projectName';
var Content = function (_a) {
    var projects = _a.projects, releaseVersion = _a.releaseVersion, location = _a.location, orgSlug = _a.orgSlug, activeDisplay = _a.activeDisplay, showPlaceholders = _a.showPlaceholders;
    var activeStatsPeriod = (location.query.healthStatsPeriod || '24h');
    var healthStatsPeriod = (<HealthStatsPeriod location={location} activePeriod={activeStatsPeriod}/>);
    return (<React.Fragment>
      <Header>
        <Layout>
          <ProjectColumn>{t('Project name')}</ProjectColumn>
          <AdoptionColumn>{t('User Adoption')}</AdoptionColumn>
          {activeDisplay === DisplayOption.CRASH_FREE_USERS ? (<React.Fragment>
              <UsersColumn>{t('Crash Free Users')}</UsersColumn>
              <DailyColumn>
                <span>{t('Users')}</span>
                {healthStatsPeriod}
              </DailyColumn>
            </React.Fragment>) : (<React.Fragment>
              <SessionsColumn>{t('Crash Free Sessions')}</SessionsColumn>
              <DailyColumn>
                <span>{t('Sessions')}</span>
                {healthStatsPeriod}
              </DailyColumn>
            </React.Fragment>)}
          <CrashesColumn>{t('Crashes')}</CrashesColumn>
          <IssuesColumn>{t('New Issues')}</IssuesColumn>
        </Layout>
      </Header>

      <ClippedHealthRows>
        {projects.map(function (project) {
        var slug = project.slug, healthData = project.healthData, newGroups = project.newGroups;
        var _a = healthData || {}, hasHealthData = _a.hasHealthData, adoption = _a.adoption, stats = _a.stats, crashFreeUsers = _a.crashFreeUsers, crashFreeSessions = _a.crashFreeSessions, sessionsCrashed = _a.sessionsCrashed, totalUsers = _a.totalUsers, totalUsers24h = _a.totalUsers24h, totalSessions = _a.totalSessions, totalSessions24h = _a.totalSessions24h;
        return (<ProjectRow key={releaseVersion + "-" + slug + "-health"}>
              <Layout>
                <ProjectColumn>
                  <ProjectName orgSlug={orgSlug} project={project} releaseVersion={releaseVersion}/>
                </ProjectColumn>

                <AdoptionColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="150px"/>) : defined(adoption) ? (<AdoptionWrapper>
                      <ProgressBarWrapper>
                        <Tooltip containerDisplayMode="block" title={<AdoptionTooltip totalUsers={totalUsers} totalSessions={totalSessions} totalUsers24h={totalUsers24h} totalSessions24h={totalSessions24h}/>}>
                          <ProgressBar value={Math.ceil(adoption)}/>
                        </Tooltip>
                      </ProgressBarWrapper>
                      <Count value={totalUsers24h !== null && totalUsers24h !== void 0 ? totalUsers24h : 0}/>
                    </AdoptionWrapper>) : (<NotAvailable />)}
                </AdoptionColumn>

                {activeDisplay === DisplayOption.CRASH_FREE_USERS ? (<UsersColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeUsers) ? (<CrashFree percent={crashFreeUsers}/>) : (<NotAvailable />)}
                  </UsersColumn>) : (<SessionsColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeSessions) ? (<CrashFree percent={crashFreeSessions}/>) : (<NotAvailable />)}
                  </SessionsColumn>)}

                <DailyColumn>
                  {showPlaceholders ? (<StyledPlaceholder />) : hasHealthData && defined(stats) ? (<ChartWrapper>
                      <HealthStatsChart data={stats} height={20} period={activeStatsPeriod} activeDisplay={activeDisplay}/>
                    </ChartWrapper>) : (<NotAvailable />)}
                </DailyColumn>

                <CrashesColumn>
                  {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : hasHealthData && defined(sessionsCrashed) ? (<Count value={sessionsCrashed}/>) : (<NotAvailable />)}
                </CrashesColumn>

                <IssuesColumn>
                  <Tooltip title={t('Open in Issues')}>
                    <Link to={getReleaseNewIssuesUrl(orgSlug, project.id, releaseVersion)}>
                      <Count value={newGroups || 0}/>
                    </Link>
                  </Tooltip>
                </IssuesColumn>
              </Layout>
            </ProjectRow>);
    })}
      </ClippedHealthRows>
    </React.Fragment>);
};
export default Content;
var ProjectRow = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 10px ", ";\n  max-height: 41px;\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  padding: 10px ", ";\n  max-height: 41px;\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.fontSizeMedium; });
var Layout = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 0.5fr 0.5fr;\n  grid-column-gap: ", ";\n  align-content: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 0.5fr 0.5fr;\n  grid-column-gap: ", ";\n  align-content: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 1fr 0.5fr 0.5fr;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var Column = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  height: 20px;\n  line-height: 20px;\n"], ["\n  ", ";\n  height: 20px;\n  line-height: 20px;\n"])), overflowEllipsis);
var ProjectColumn = styled(Column)(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var AdoptionColumn = styled(Column)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AdoptionWrapper = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var UsersColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject([""], [""])));
var SessionsColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject([""], [""])));
var DailyColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n\n  @media (min-width: ", ") {\n    display: none;\n    overflow: hidden;\n  }\n\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n\n  @media (min-width: ", ") {\n    display: none;\n    overflow: hidden;\n  }\n\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var CrashesColumn = styled(Column)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var IssuesColumn = styled(Column)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var ChartWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"], ["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var StyledPlaceholder = styled(Placeholder)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"], ["\n  height: 20px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"])), space(0.25));
var ProgressBarWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  min-width: 70px;\n  max-width: 90px;\n"], ["\n  min-width: 70px;\n  max-width: 90px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=content.jsx.map