import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Badge from 'app/components/badge';
import Breadcrumbs from 'app/components/breadcrumbs';
import Clipboard from 'app/components/clipboard';
import IdBadge from 'app/components/idBadge';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import Tooltip from 'app/components/tooltip';
import Version from 'app/components/version';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconCopy, IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { formatAbbreviatedNumber, formatVersion } from 'app/utils/formatters';
import ReleaseActions from './releaseActions';
var ReleaseHeader = function (_a) {
    var location = _a.location, organization = _a.organization, release = _a.release, project = _a.project, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    var version = release.version, url = release.url;
    var commitCount = releaseMeta.commitCount, commitFilesChanged = releaseMeta.commitFilesChanged, releaseFileCount = releaseMeta.releaseFileCount;
    var releasePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(version) + "/";
    var tabs = [
        { title: t('Overview'), to: releasePath },
        {
            title: (<React.Fragment>
          {t('Commits')} <NavTabsBadge text={formatAbbreviatedNumber(commitCount)}/>
        </React.Fragment>),
            to: releasePath + "commits/",
        },
        {
            title: (<React.Fragment>
          {t('Files Changed')}
          <NavTabsBadge text={formatAbbreviatedNumber(commitFilesChanged)}/>
        </React.Fragment>),
            to: releasePath + "files-changed/",
        },
        {
            title: (<React.Fragment>
          {t('Artifacts')}
          <NavTabsBadge text={formatAbbreviatedNumber(releaseFileCount)}/>
        </React.Fragment>),
            to: releasePath + "artifacts/",
        },
    ];
    var getCurrentTabUrl = function (path) { return ({
        pathname: path,
        query: pick(location.query, Object.values(URL_PARAM)),
    }); };
    return (<Layout.Header>
      <Layout.HeaderContent>
        <Breadcrumbs crumbs={[
        {
            to: "/organizations/" + organization.slug + "/releases/",
            label: t('Releases'),
            preserveGlobalSelection: true,
        },
        { label: formatVersion(version) },
    ]}/>
        <Layout.Title>
          <IdBadge project={project} avatarSize={28} displayName={<ReleaseName>
                <Version version={version} anchor={false}/>
                <IconWrapper>
                  <Clipboard value={version}>
                    <Tooltip title={version} containerDisplayMode="flex">
                      <IconCopy size="xs"/>
                    </Tooltip>
                  </Clipboard>
                </IconWrapper>
                {!!url && (<IconWrapper>
                    <Tooltip title={url}>
                      <ExternalLink href={url}>
                        <IconOpen size="xs"/>
                      </ExternalLink>
                    </Tooltip>
                  </IconWrapper>)}
              </ReleaseName>}/>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <ReleaseActions orgSlug={organization.slug} projectSlug={project.slug} release={release} releaseMeta={releaseMeta} refetchData={refetchData}/>
      </Layout.HeaderActions>

      <React.Fragment>
        <StyledNavTabs>
          {tabs.map(function (tab) { return (<ListLink key={tab.to} to={getCurrentTabUrl(tab.to)} isActive={function () { return tab.to === location.pathname; }}>
              {tab.title}
            </ListLink>); })}
        </StyledNavTabs>
      </React.Fragment>
    </Layout.Header>);
};
var ReleaseName = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IconWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"], ["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"])), space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
var StyledNavTabs = styled(NavTabs)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
var NavTabsBadge = styled(Badge)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default ReleaseHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=releaseHeader.jsx.map