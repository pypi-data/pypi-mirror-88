import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tag from 'app/components/tag';
import { IconCheckmark, IconClose } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var FEATURE_TOOLTIPS = {
    symtab: t('Symbol tables are used as a fallback when full debug information is not available'),
    debug: t('Debug information provides function names and resolves inlined frames during symbolication'),
    unwind: t('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
    sources: t('Source code information allows Sentry to display source code context for stack frames'),
};
var DebugFileFeature = function (_a) {
    var _b = _a.available, available = _b === void 0 ? true : _b, feature = _a.feature;
    var tooltipText = FEATURE_TOOLTIPS[feature];
    if (available === true) {
        return (<StyledTag type="success" tooltipText={tooltipText} icon={<IconCheckmark />}>
        {feature}
      </StyledTag>);
    }
    return (<StyledTag type="error" tooltipText={tooltipText} icon={<IconClose />}>
      {feature}
    </StyledTag>);
};
export default DebugFileFeature;
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=debugFileFeature.jsx.map