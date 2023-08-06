import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import partition from 'lodash/partition';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { tct, tn } from 'app/locale';
import space from 'app/styles/space';
import Content from './content';
var ReleaseHealth = /** @class */ (function (_super) {
    __extends(ReleaseHealth, _super);
    function ReleaseHealth() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ReleaseHealth.prototype.shouldComponentUpdate = function (nextProps) {
        // we don't want project health rows to reorder/jump while the whole card is loading
        if (this.props.reloading && nextProps.reloading) {
            return false;
        }
        return true;
    };
    ReleaseHealth.prototype.render = function () {
        var _a = this.props, release = _a.release, orgSlug = _a.orgSlug, activeDisplay = _a.activeDisplay, location = _a.location, showPlaceholders = _a.showPlaceholders, selection = _a.selection;
        // sort health rows inside release card alphabetically by project name,
        // show only the ones that are selected in global header
        var _b = __read(partition(release.projects.sort(function (a, b) { return a.slug.localeCompare(b.slug); }), function (p) {
            // do not filter for My Projects & All Projects
            return selection.projects.length > 0 && !selection.projects.includes(-1)
                ? selection.projects.includes(p.id)
                : true;
        }), 2), projectsToShow = _b[0], projectsToHide = _b[1];
        function getHiddenProjectsTooltip() {
            var limitedProjects = projectsToHide.map(function (p) { return p.slug; }).slice(0, 5);
            var remainderLength = projectsToHide.length - limitedProjects.length;
            if (remainderLength) {
                limitedProjects.push(tn('and %s more', 'and %s more', remainderLength));
            }
            return limitedProjects.join(', ');
        }
        return (<React.Fragment>
        <Content activeDisplay={activeDisplay} orgSlug={orgSlug} releaseVersion={release.version} projects={projectsToShow} location={location} showPlaceholders={showPlaceholders}/>

        {projectsToHide.length > 0 && (<HiddenProjectsMessage>
            <Tooltip title={getHiddenProjectsTooltip()}>
              <TextOverflow>
                {projectsToHide.length === 1
            ? tct('[number:1] hidden project', { number: <strong /> })
            : tct('[number] hidden projects', {
                number: <strong>{projectsToHide.length}</strong>,
            })}
              </TextOverflow>
            </Tooltip>
          </HiddenProjectsMessage>)}
      </React.Fragment>);
    };
    return ReleaseHealth;
}(React.Component));
var HiddenProjectsMessage = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  padding: 0 ", ";\n  border-top: 1px solid ", ";\n  overflow: hidden;\n  height: 24px;\n  line-height: 24px;\n  color: ", ";\n  background-color: ", ";\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"], ["\n  font-size: ", ";\n  padding: 0 ", ";\n  border-top: 1px solid ", ";\n  overflow: hidden;\n  height: 24px;\n  line-height: 24px;\n  color: ", ";\n  background-color: ", ";\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.borderRadius; });
export default ReleaseHealth;
var templateObject_1;
//# sourceMappingURL=index.jsx.map