import { __awaiter, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { archiveRelease, restoreRelease } from 'app/actionCreators/release';
import { Client } from 'app/api';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import MenuItem from 'app/components/menuItem';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { IconEllipsis } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import { formatVersion } from 'app/utils/formatters';
import { isReleaseArchived } from '../utils';
function ReleaseActions(_a) {
    var orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, release = _a.release, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    function handleArchive() {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, archiveRelease(new Client(), {
                                orgSlug: orgSlug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        browserHistory.push("/organizations/" + orgSlug + "/releases/");
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function handleRestore() {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, restoreRelease(new Client(), {
                                orgSlug: orgSlug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        refetchData();
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function getProjectList() {
        var maxVisibleProjects = 5;
        var visibleProjects = releaseMeta.projects.slice(0, maxVisibleProjects);
        var numberOfCollapsedProjects = releaseMeta.projects.length - visibleProjects.length;
        return (<React.Fragment>
        {visibleProjects.map(function (project) { return (<ProjectBadge key={project.slug} project={project} avatarSize={18}/>); })}
        {numberOfCollapsedProjects > 0 && (<span>
            <Tooltip title={release.projects
            .slice(maxVisibleProjects)
            .map(function (p) { return p.slug; })
            .join(', ')}>
              + {tn('%s other project', '%s other projects', numberOfCollapsedProjects)}
            </Tooltip>
          </span>)}
      </React.Fragment>);
    }
    function getModalHeader(title) {
        return (<h4>
        <TextOverflow>{title}</TextOverflow>
      </h4>);
    }
    function getModalMessage(message) {
        return (<React.Fragment>
        {message}

        <ProjectsWrapper>{getProjectList()}</ProjectsWrapper>

        {t('Are you sure you want to do this?')}
      </React.Fragment>);
    }
    return (<ButtonBar gap={1}>
      <StyledDropdownLink caret={false} anchorRight={window.innerWidth > 992} title={<ActionsButton icon={<IconEllipsis />} label={t('Actions')}/>}>
        {isReleaseArchived(release) ? (<Confirm onConfirm={handleRestore} header={getModalHeader(tct('Restore Release [release]', {
        release: formatVersion(release.version),
    }))} message={getModalMessage(tn('You are restoring this release for the following project:', 'By restoring this release, you are also restoring it for the following projects:', releaseMeta.projects.length))} cancelText={t('Nevermind')} confirmText={t('Restore')}>
            <MenuItem>{t('Restore')}</MenuItem>
          </Confirm>) : (<Confirm onConfirm={handleArchive} header={getModalHeader(tct('Archive Release [release]', {
        release: formatVersion(release.version),
    }))} message={getModalMessage(tn('You are archiving this release for the following project:', 'By archiving this release, you are also archiving it for the following projects:', releaseMeta.projects.length))} cancelText={t('Nevermind')} confirmText={t('Archive')}>
            <MenuItem>{t('Archive')}</MenuItem>
          </Confirm>)}
      </StyledDropdownLink>
    </ButtonBar>);
}
ReleaseActions.propTypes = {
    orgSlug: PropTypes.string.isRequired,
    projectSlug: PropTypes.string.isRequired,
    release: SentryTypes.Release.isRequired,
    releaseMeta: PropTypes.object.isRequired,
    refetchData: PropTypes.func.isRequired,
};
var ActionsButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"], ["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"], ["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"])));
var ProjectsWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"], ["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"])), space(2), space(2), space(2), space(0.5));
export default ReleaseActions;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseActions.jsx.map