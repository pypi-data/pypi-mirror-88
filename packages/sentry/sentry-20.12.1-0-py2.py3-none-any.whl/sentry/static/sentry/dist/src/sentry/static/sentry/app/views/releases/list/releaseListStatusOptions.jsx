var _a;
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ReleaseListDropdown from './releaseListDropdown';
import { StatusOption } from './utils';
var options = (_a = {},
    _a[StatusOption.ACTIVE] = t('Active'),
    _a[StatusOption.ARCHIVED] = t('Archived'),
    _a);
function ReleaseListStatusOptions(_a) {
    var selected = _a.selected, onSelect = _a.onSelect;
    return (<StyledReleaseListDropdown label={t('Status')} options={options} selected={selected} onSelect={onSelect}/>);
}
export default ReleaseListStatusOptions;
var StyledReleaseListDropdown = styled(ReleaseListDropdown)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: 3;\n  @media (max-width: ", ") {\n    order: 1;\n  }\n"], ["\n  z-index: 3;\n  @media (max-width: ", ") {\n    order: 1;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1;
//# sourceMappingURL=releaseListStatusOptions.jsx.map