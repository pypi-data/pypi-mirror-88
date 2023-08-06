import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Tag from 'app/components/tag';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
// TODO(matej): remove "unhandled-issue-flag" feature flag once testing is over (otherwise this won't ever be rendered in a shared event)
function UnhandledTag() {
    return (<Feature features={['unhandled-issue-flag']}>
      <TagWrapper>
        <Tooltip title={t('An unhandled error was detected in this Issue.')}>
          <Tag type="error">{t('Unhandled')}</Tag>
        </Tooltip>
      </TagWrapper>
    </Feature>);
}
var TagWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var TagAndMessageWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
export default UnhandledTag;
export { TagAndMessageWrapper };
var templateObject_1, templateObject_2;
//# sourceMappingURL=unhandledTag.jsx.map