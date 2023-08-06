import React from 'react';
import { t, tct } from 'app/locale';
import { BULK_LIMIT, BULK_LIMIT_STR } from './utils';
function ExtraDescription(_a) {
    var all = _a.all, query = _a.query, queryCount = _a.queryCount;
    if (!all) {
        return null;
    }
    if (query) {
        return (<div>
        <p>{t('This will apply to the current search query') + ':'}</p>
        <pre>{query}</pre>
      </div>);
    }
    return (<p className="error">
      <strong>
        {queryCount > BULK_LIMIT
        ? tct('This will apply to the first [bulkNumber] issues matched in this project!', {
            bulkNumber: BULK_LIMIT_STR,
        })
        : tct('This will apply to all [bulkNumber] issues matched in this project!', {
            bulkNumber: queryCount,
        })}
      </strong>
    </p>);
}
export default ExtraDescription;
//# sourceMappingURL=extraDescription.jsx.map