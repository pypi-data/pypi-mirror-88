import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GroupReleaseChart from 'app/components/group/releaseChart';
import SeenInfo from 'app/components/group/seenInfo';
import Placeholder from 'app/components/placeholder';
import Tooltip from 'app/components/tooltip';
import { IconQuestion } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import SidebarSection from './sidebarSection';
var GroupReleaseStats = function (_a) {
    var group = _a.group, organization = _a.organization, project = _a.project, environments = _a.environments, allEnvironments = _a.allEnvironments;
    var environmentLabel = environments.length > 0
        ? environments.map(function (env) { return env.displayName; }).join(', ')
        : t('All Environments');
    var shortEnvironmentLabel = environments.length > 1
        ? t('selected environments')
        : environments.length === 1
            ? environments[0].displayName
            : undefined;
    var projectId = project.id;
    var projectSlug = project.slug;
    var orgSlug = organization.slug;
    var hasRelease = new Set(project.features).has('releases');
    var releaseTrackingUrl = "/settings/" + organization.slug + "/projects/" + project.slug + "/release-tracking/";
    return (<SidebarSection title={<span data-test-id="env-label">{environmentLabel}</span>}>
      {!group || !allEnvironments ? (<Placeholder height="288px"/>) : (<React.Fragment>
          <GroupReleaseChart group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={group.currentRelease ? group.currentRelease.release : null} releaseStats={group.currentRelease ? group.currentRelease.stats : null} statsPeriod="24h" title={t('Last 24 Hours')} firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>
          <GroupReleaseChart group={allEnvironments} environment={environmentLabel} environmentStats={group.stats} release={group.currentRelease ? group.currentRelease.release : null} releaseStats={group.currentRelease ? group.currentRelease.stats : null} statsPeriod="30d" title={t('Last 30 Days')} className="bar-chart-small" firstSeen={group.firstSeen} lastSeen={group.lastSeen}/>

          <SidebarSection secondary title={<span>
                {t('Last seen')}
                <TooltipWrapper>
                  <Tooltip title={t('When the most recent event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </Tooltip>
                </TooltipWrapper>
              </span>}>
            <SeenInfo orgSlug={orgSlug} projectId={projectId} projectSlug={projectSlug} date={getDynamicText({
        value: group.lastSeen,
        fixed: '2016-01-13T03:08:25Z',
    })} dateGlobal={allEnvironments.lastSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.lastRelease || null} title={t('Last seen')}/>
          </SidebarSection>

          <SidebarSection secondary title={<span>
                {t('First seen')}
                <TooltipWrapper>
                  <Tooltip title={t('When the first event in this issue was captured.')} disableForVisualTest>
                    <StyledIconQuest size="xs" color="gray200"/>
                  </Tooltip>
                </TooltipWrapper>
              </span>}>
            <SeenInfo orgSlug={orgSlug} projectId={projectId} projectSlug={projectSlug} date={getDynamicText({
        value: group.firstSeen,
        fixed: '2015-08-13T03:08:25Z',
    })} dateGlobal={allEnvironments.firstSeen} hasRelease={hasRelease} environment={shortEnvironmentLabel} release={group.firstRelease || null} title={t('First seen')}/>
          </SidebarSection>
          {!hasRelease ? (<SidebarSection secondary title={t('Releases not configured')}>
              <a href={releaseTrackingUrl}>{t('Setup Releases')}</a>{' '}
              {t(' to make issues easier to fix.')}
            </SidebarSection>) : null}
        </React.Fragment>)}
    </SidebarSection>);
};
export default React.memo(GroupReleaseStats);
var TooltipWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
var StyledIconQuest = styled(IconQuestion)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  top: 2px;\n"], ["\n  position: relative;\n  top: 2px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=releaseStats.jsx.map