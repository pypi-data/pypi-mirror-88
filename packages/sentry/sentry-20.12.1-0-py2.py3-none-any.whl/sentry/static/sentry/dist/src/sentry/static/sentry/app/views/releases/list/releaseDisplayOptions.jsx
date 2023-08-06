var _a;
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
import { DisplayOption } from './utils';
var displayOptions = (_a = {},
    _a[DisplayOption.CRASH_FREE_SESSIONS] = t('Crash Free Sessions'),
    _a[DisplayOption.CRASH_FREE_USERS] = t('Crash Free Users'),
    _a);
function ReleaseListDisplayOptions(_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    return (<StyledReleaseListDropdown label={t('Display')} options={displayOptions} selected={selected} onSelect={onSelect}/>);
}
export default ReleaseListDisplayOptions;
var StyledReleaseListDropdown = styled(ReleaseListDropdown)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: 1;\n  @media (max-width: ", ") {\n    order: 3;\n  }\n"], ["\n  z-index: 1;\n  @media (max-width: ", ") {\n    order: 3;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseDisplayOptions.jsx.map