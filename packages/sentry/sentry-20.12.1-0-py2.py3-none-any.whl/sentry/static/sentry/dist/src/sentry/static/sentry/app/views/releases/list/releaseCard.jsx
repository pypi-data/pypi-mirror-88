import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import ReleaseStats from 'app/components/releaseStats';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import ReleaseHealth from './releaseHealth';
var ReleaseCard = function (_a) {
    var release = _a.release, orgSlug = _a.orgSlug, activeDisplay = _a.activeDisplay, location = _a.location, reloading = _a.reloading, selection = _a.selection, showHealthPlaceholders = _a.showHealthPlaceholders;
    var version = release.version, commitCount = release.commitCount, lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, versionInfo = release.versionInfo;
    return (<StyledPanel reloading={reloading ? 1 : 0}>
      <ReleaseInfo>
        <ReleaseInfoHeader>
          <VersionWrapper>
            <StyledVersion version={version} tooltipRawVersion anchor={false}/>
          </VersionWrapper>
          {commitCount > 0 && <ReleaseStats release={release} withHeading={false}/>}
        </ReleaseInfoHeader>
        <ReleaseInfoSubheader>
          {(versionInfo === null || versionInfo === void 0 ? void 0 : versionInfo.package) && (<PackageName ellipsisDirection="left">{versionInfo.package}</PackageName>)}
          <TimeSince date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated}/>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) && " | " + lastDeploy.environment}
        </ReleaseInfoSubheader>
      </ReleaseInfo>

      <ReleaseProjects>
        <ReleaseHealth release={release} orgSlug={orgSlug} activeDisplay={activeDisplay} location={location} showPlaceholders={showHealthPlaceholders} reloading={reloading} selection={selection}/>
      </ReleaseProjects>
    </StyledPanel>);
};
var VersionWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledVersion = styled(Version)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var StyledPanel = styled(Panel)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  opacity: ", ";\n  pointer-events: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"], ["\n  opacity: ", ";\n  pointer-events: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return (p.reloading ? 0.5 : 1); }, function (p) { return (p.reloading ? 'none' : 'auto'); }, function (p) { return p.theme.breakpoints[1]; });
var ReleaseInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n  flex-shrink: 0;\n\n  @media (min-width: ", ") {\n    border-right: 1px solid ", ";\n    min-width: 250px;\n    width: 25%;\n  }\n  @media (min-width: ", ") {\n    min-width: 300px;\n  }\n"], ["\n  padding: ", " ", ";\n  flex-shrink: 0;\n\n  @media (min-width: ", ") {\n    border-right: 1px solid ", ";\n    min-width: 250px;\n    width: 25%;\n  }\n  @media (min-width: ", ") {\n    min-width: 300px;\n  }\n"])), space(1.5), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[3]; });
var ReleaseInfoSubheader = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray400; });
var PackageName = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.gray500; });
var ReleaseProjects = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  flex-grow: 1;\n  display: grid;\n\n  @media (min-width: ", ") {\n    border-top: none;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  flex-grow: 1;\n  display: grid;\n\n  @media (min-width: ", ") {\n    border-top: none;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[1]; });
var ReleaseInfoHeader = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(2));
export default ReleaseCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=releaseCard.jsx.map