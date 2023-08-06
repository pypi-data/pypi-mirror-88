import React from 'react';
import capitalize from 'lodash/capitalize';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct, tn } from 'app/locale';
import ExtraDescription from './extraDescription';
export var BULK_LIMIT = 1000;
export var BULK_LIMIT_STR = BULK_LIMIT.toLocaleString();
export var ConfirmAction;
(function (ConfirmAction) {
    ConfirmAction["RESOLVE"] = "resolve";
    ConfirmAction["UNRESOLVE"] = "unresolve";
    ConfirmAction["ACKNOWLEDGE"] = "acknowledge";
    ConfirmAction["IGNORE"] = "ignore";
    ConfirmAction["BOOKMARK"] = "bookmark";
    ConfirmAction["UNBOOKMARK"] = "unbookmark";
    ConfirmAction["MARK"] = "mark";
    ConfirmAction["MERGE"] = "merge";
    ConfirmAction["DELETE"] = "delete";
    ConfirmAction["REMOVE"] = "remove";
})(ConfirmAction || (ConfirmAction = {}));
function getBulkConfirmMessage(action, queryCount) {
    if (queryCount > BULK_LIMIT) {
        return tct('Are you sure you want to [action] the first [bulkNumber] issues that match the search?', {
            action: action,
            bulkNumber: BULK_LIMIT_STR,
        });
    }
    return tct('Are you sure you want to [action] all [bulkNumber] issues that match the search?', {
        action: action,
        bulkNumber: queryCount,
    });
}
export function getConfirm(numIssues, allInQuerySelected, query, queryCount) {
    return function (action, canBeUndone, append) {
        if (append === void 0) { append = ''; }
        var question = allInQuerySelected
            ? getBulkConfirmMessage("" + action + append, queryCount)
            : tn("Are you sure you want to " + action + " this %s issue" + append + "?", "Are you sure you want to " + action + " these %s issues" + append + "?", numIssues);
        var message = action === ConfirmAction.DELETE
            ? tct('Bulk deletion is only recommended for junk data. To clear your stream, consider resolving or ignoring. [link:When should I delete events?]', {
                link: (<ExternalLink href="https://help.sentry.io/hc/en-us/articles/360003443113-When-should-I-delete-events"/>),
            })
            : t('This action cannot be undone.');
        return (<div>
        <p style={{ marginBottom: '20px' }}>
          <strong>{question}</strong>
        </p>
        <ExtraDescription all={allInQuerySelected} query={query} queryCount={queryCount}/>
        {!canBeUndone && <p>{message}</p>}
      </div>);
    };
}
export function getLabel(numIssues, allInQuerySelected) {
    return function (action, append) {
        if (append === void 0) { append = ''; }
        var capitalized = capitalize(action);
        var text = allInQuerySelected
            ? t("Bulk " + action + " issues")
            : tn(capitalized + " %s selected issue", capitalized + " %s selected issues", numIssues);
        return text + append;
    };
}
//# sourceMappingURL=utils.jsx.map