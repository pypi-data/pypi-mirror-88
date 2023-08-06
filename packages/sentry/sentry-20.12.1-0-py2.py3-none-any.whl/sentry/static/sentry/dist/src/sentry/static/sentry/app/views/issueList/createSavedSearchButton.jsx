import { __rest } from "tslib";
import React from 'react';
import { openModal } from 'app/actionCreators/modal';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
import CreateSavedSearchModal from './createSavedSearchModal';
var CreateSavedSearchButton = function (_a) {
    var buttonClassName = _a.buttonClassName, withTooltip = _a.withTooltip, iconOnly = _a.iconOnly, organization = _a.organization, rest = __rest(_a, ["buttonClassName", "withTooltip", "iconOnly", "organization"]);
    return (<Access organization={organization} access={['org:write']}>
    <Button title={withTooltip ? t('Add to organization saved searches') : undefined} onClick={function () {
        return openModal(function (deps) { return (<CreateSavedSearchModal organization={organization} {...rest} {...deps}/>); });
    }} data-test-id="save-current-search" size="zero" borderless type="button" aria-label={t('Add to organization saved searches')} icon={<IconAdd size="xs"/>} className={buttonClassName}>
      {!iconOnly && t('Create Saved Search')}
    </Button>
  </Access>);
};
export default CreateSavedSearchButton;
//# sourceMappingURL=createSavedSearchButton.jsx.map