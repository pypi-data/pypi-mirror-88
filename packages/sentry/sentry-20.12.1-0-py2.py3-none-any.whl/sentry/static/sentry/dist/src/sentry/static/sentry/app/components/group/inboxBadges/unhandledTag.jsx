import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Tooltip from 'app/components/tooltip';
import { IconFire } from 'app/icons';
import { t } from 'app/locale';
// TODO(matej): remove "unhandled-issue-flag" feature flag once testing is over (otherwise this won't ever be rendered in a shared event)
var UnhandledTag = function (_a) {
    var organization = _a.organization;
    return (<Feature organization={organization} features={['unhandled-issue-flag']}>
    <Tooltip title={t('An unhandled error was detected in this Issue.')}>
      <UnhandledTagWrapper>
        <StyledIconFire size="xs" color="red300"/>
        {t('Unhandled')}
      </UnhandledTagWrapper>
    </Tooltip>
  </Feature>);
};
export default UnhandledTag;
var UnhandledTagWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  white-space: nowrap;\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
var StyledIconFire = styled(IconFire)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: 3px;\n"], ["\n  margin-right: 3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=unhandledTag.jsx.map