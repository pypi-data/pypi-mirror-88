import { __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import ActionLink from 'app/components/actions/actionLink';
import IgnoreActions from 'app/components/actions/ignore';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconEllipsis, IconIssues, IconPause, IconPlay } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { ResolutionStatus } from 'app/types';
import Projects from 'app/utils/projects';
import ResolveActions from './resolveActions';
import { ConfirmAction, getConfirm, getLabel } from './utils';
function ActionSet(_a) {
    var orgSlug = _a.orgSlug, queryCount = _a.queryCount, query = _a.query, realtimeActive = _a.realtimeActive, allInQuerySelected = _a.allInQuerySelected, anySelected = _a.anySelected, multiSelected = _a.multiSelected, issues = _a.issues, onUpdate = _a.onUpdate, onShouldConfirm = _a.onShouldConfirm, onDelete = _a.onDelete, onRealtimeChange = _a.onRealtimeChange, onMerge = _a.onMerge, selectedProjectSlug = _a.selectedProjectSlug, hasInbox = _a.hasInbox;
    var numIssues = issues.size;
    var confirm = getConfirm(numIssues, allInQuerySelected, query, queryCount);
    var label = getLabel(numIssues, allInQuerySelected);
    // merges require a single project to be active in an org context
    // selectedProjectSlug is null when 0 or >1 projects are selected.
    var mergeDisabled = !(multiSelected && selectedProjectSlug);
    return (<Wrapper hasInbox={hasInbox}>
      {hasInbox && (<div className="btn-group hidden-sm hidden-xs">
          <StyledActionLink className="btn btn-default btn-sm action-merge" data-test-id="button-acknowledge" disabled={!anySelected} onAction={function () { return onUpdate({ inbox: false }); }} shouldConfirm={onShouldConfirm(ConfirmAction.ACKNOWLEDGE)} message={confirm(ConfirmAction.MARK, false, ' as reviewed')} confirmLabel={label('Mark', ' as reviewed')} title={t('Mark Reviewed')}>
            <StyledIconIssues size="xs"/>
            {t('Mark Reviewed')}
          </StyledActionLink>
        </div>)}
      {selectedProjectSlug ? (<Projects orgId={orgSlug} slugs={[selectedProjectSlug]}>
          {function (_a) {
        var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
        var selectedProject = projects[0];
        return (<ResolveActions onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
            hasReleases: selectedProject.hasOwnProperty('features')
                ? selectedProject.features.includes('releases')
                : false,
            latestRelease: selectedProject.hasOwnProperty('latestRelease')
                ? selectedProject.latestRelease
                : undefined,
            projectId: selectedProject.slug,
            confirm: confirm,
            label: label,
            loadingProjects: !initiallyLoaded,
            projectFetchError: !!fetchError,
        }}/>);
    }}
        </Projects>) : (<ResolveActions onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
        hasReleases: false,
        latestRelease: null,
        projectId: null,
        confirm: confirm,
        label: label,
    }}/>)}
      <IgnoreActions onUpdate={onUpdate} shouldConfirm={onShouldConfirm(ConfirmAction.IGNORE)} confirmMessage={confirm(ConfirmAction.IGNORE, true)} confirmLabel={label('ignore')} disabled={!anySelected}/>
      <div className="btn-group hidden-md hidden-sm hidden-xs">
        <ActionLink className="btn btn-default btn-sm action-merge" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(ConfirmAction.MERGE)} message={confirm(ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
          {t('Merge')}
        </ActionLink>
      </div>
      <div className="btn-group">
        <DropdownLink key="actions" caret={false} className="btn btn-sm btn-default action-more" title={<IconPad>
              <IconEllipsis size="xs"/>
            </IconPad>}>
          <MenuItem noAnchor>
            <ActionLink className="action-merge hidden-lg hidden-xl" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(ConfirmAction.MERGE)} message={confirm(ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
              {t('Merge')}
            </ActionLink>
          </MenuItem>
          {hasInbox && (<React.Fragment>
              <MenuItem divider className="hidden-md hidden-lg hidden-xl"/>
              <MenuItem noAnchor>
                <ActionLink className="action-acknowledge hidden-md hidden-lg hidden-xl" disabled={!anySelected} onAction={function () { return onUpdate({ inbox: false }); }} shouldConfirm={onShouldConfirm(ConfirmAction.ACKNOWLEDGE)} message={confirm(ConfirmAction.ACKNOWLEDGE, false)} confirmLabel={label('acknowledge')} title={t('Acknowledge')}>
                  {t('Acknowledge')}
                </ActionLink>
              </MenuItem>
            </React.Fragment>)}
          <MenuItem divider className="hidden-lg hidden-xl"/>
          <MenuItem noAnchor>
            <ActionLink className="action-bookmark" disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: true }); }} shouldConfirm={onShouldConfirm(ConfirmAction.BOOKMARK)} message={confirm(ConfirmAction.BOOKMARK, false)} confirmLabel={label('bookmark')} title={t('Add to Bookmarks')}>
              {t('Add to Bookmarks')}
            </ActionLink>
          </MenuItem>
          <MenuItem divider/>
          <MenuItem noAnchor>
            <ActionLink className="action-remove-bookmark" disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: false }); }} shouldConfirm={onShouldConfirm(ConfirmAction.UNBOOKMARK)} message={confirm(ConfirmAction.REMOVE, false, ' from your bookmarks')} confirmLabel={label('remove', ' from your bookmarks')} title={t('Remove from Bookmarks')}>
              {t('Remove from Bookmarks')}
            </ActionLink>
          </MenuItem>
          <MenuItem divider/>
          <MenuItem noAnchor>
            <ActionLink className="action-unresolve" disabled={!anySelected} onAction={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }} shouldConfirm={onShouldConfirm(ConfirmAction.UNRESOLVE)} message={confirm(ConfirmAction.UNRESOLVE, true)} confirmLabel={label('unresolve')} title={t('Set status to: Unresolved')}>
              {t('Set status to: Unresolved')}
            </ActionLink>
          </MenuItem>
          <MenuItem divider/>
          <MenuItem noAnchor>
            <ActionLink className="action-delete" disabled={!anySelected} onAction={onDelete} shouldConfirm={onShouldConfirm(ConfirmAction.DELETE)} message={confirm(ConfirmAction.DELETE, false)} confirmLabel={label('delete')} title={t('Delete Issues')}>
              {t('Delete Issues')}
            </ActionLink>
          </MenuItem>
        </DropdownLink>
      </div>
      {!hasInbox && (<div className="btn-group">
          <Tooltip title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))}>
            <a data-test-id="realtime-control" className="btn btn-default btn-sm hidden-xs" onClick={onRealtimeChange}>
              <IconPad>
                {realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}
              </IconPad>
            </a>
          </Tooltip>
        </div>)}
    </Wrapper>);
}
export default ActionSet;
var StyledActionLink = styled(ActionLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
// New icons are misaligned inside bootstrap buttons.
// This is a shim that can be removed when buttons are upgraded
// to styled components.
var IconPad = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  top: ", ";\n"], ["\n  position: relative;\n  top: ", ";\n"])), space(0.25));
var StyledIconIssues = styled(IconIssues)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var Wrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  display: flex;\n  ", ";\n\n  .btn-group {\n    display: flex;\n    margin-right: 6px;\n  }\n\n  @keyframes ZoomUp {\n    0% {\n      opacity: 0;\n      transform: translateY(5px);\n    }\n    100% {\n      opacity: 1;\n      transform: tranlsateY(0);\n    }\n  }\n"], ["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  display: flex;\n  ",
    ";\n\n  .btn-group {\n    display: flex;\n    margin-right: 6px;\n  }\n\n  @keyframes ZoomUp {\n    0% {\n      opacity: 0;\n      transform: translateY(5px);\n    }\n    100% {\n      opacity: 1;\n      transform: tranlsateY(0);\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, space(1), space(1), function (p) {
    return p.hasInbox && css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n      animation: 0.15s linear ZoomUp forwards;\n    "], ["\n      animation: 0.15s linear ZoomUp forwards;\n    "])));
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=actionSet.jsx.map