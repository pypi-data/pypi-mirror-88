import React from 'react';
import ResolveActions from 'app/components/actions/resolve';
import { ConfirmAction } from './utils';
function ResolveActionsContainer(_a) {
    var params = _a.params, orgSlug = _a.orgSlug, anySelected = _a.anySelected, onShouldConfirm = _a.onShouldConfirm, onUpdate = _a.onUpdate;
    var hasReleases = params.hasReleases, latestRelease = params.latestRelease, projectId = params.projectId, confirm = params.confirm, label = params.label, loadingProjects = params.loadingProjects, projectFetchError = params.projectFetchError;
    // resolve requires a single project to be active in an org context
    // projectId is null when 0 or >1 projects are selected.
    var resolveDisabled = Boolean(!anySelected || projectFetchError);
    var resolveDropdownDisabled = Boolean(!anySelected || !projectId || loadingProjects || projectFetchError);
    return (<ResolveActions hasRelease={hasReleases} latestRelease={latestRelease} orgId={orgSlug} projectId={projectId} onUpdate={onUpdate} shouldConfirm={onShouldConfirm(ConfirmAction.RESOLVE)} confirmMessage={confirm('resolve', true)} confirmLabel={label('resolve')} disabled={resolveDisabled} disableDropdown={resolveDropdownDisabled} projectFetchError={projectFetchError}/>);
}
export default ResolveActionsContainer;
//# sourceMappingURL=resolveActions.jsx.map