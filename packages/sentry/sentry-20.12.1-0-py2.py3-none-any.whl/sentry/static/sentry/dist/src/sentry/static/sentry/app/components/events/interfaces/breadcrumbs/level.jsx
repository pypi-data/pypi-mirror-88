import React from 'react';
import Highlight from 'app/components/highlight';
import Tag from 'app/components/tag';
import { t } from 'app/locale';
import { BreadcrumbLevelType } from './types';
var Level = React.memo(function (_a) {
    var level = _a.level, _b = _a.searchTerm, searchTerm = _b === void 0 ? '' : _b;
    switch (level) {
        case BreadcrumbLevelType.FATAL:
            return (<Tag type="error">
          <Highlight text={searchTerm}>{t('fatal')}</Highlight>
        </Tag>);
        case BreadcrumbLevelType.ERROR:
            return (<Tag type="error">
          <Highlight text={searchTerm}>{t('error')}</Highlight>
        </Tag>);
        case BreadcrumbLevelType.INFO:
            return (<Tag type="info">
          <Highlight text={searchTerm}>{t('info')}</Highlight>
        </Tag>);
        case BreadcrumbLevelType.WARNING:
            return (<Tag type="warning">
          <Highlight text={searchTerm}>{t('warning')}</Highlight>
        </Tag>);
        default:
            return (<Tag>
          <Highlight text={searchTerm}>{level || t('undefined')}</Highlight>
        </Tag>);
    }
});
export default Level;
//# sourceMappingURL=level.jsx.map