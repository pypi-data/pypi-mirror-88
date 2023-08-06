var _a;
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
import { SortOption } from './utils';
var sortOptions = (_a = {},
    _a[SortOption.DATE] = t('Date Created'),
    _a[SortOption.SESSIONS] = t('Total Sessions'),
    _a[SortOption.USERS_24_HOURS] = t('Active Users'),
    _a[SortOption.CRASH_FREE_USERS] = t('Crash Free Users'),
    _a[SortOption.CRASH_FREE_SESSIONS] = t('Crash Free Sessions'),
    _a);
function ReleaseListSortOptions(_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    return (<StyledReleaseListDropdown label={t('Sort By')} options={sortOptions} selected={selected} onSelect={onSelect}/>);
}
export default ReleaseListSortOptions;
var StyledReleaseListDropdown = styled(ReleaseListDropdown)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"], ["\n  z-index: 2;\n  @media (max-width: ", ") {\n    order: 2;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseListSortOptions.jsx.map