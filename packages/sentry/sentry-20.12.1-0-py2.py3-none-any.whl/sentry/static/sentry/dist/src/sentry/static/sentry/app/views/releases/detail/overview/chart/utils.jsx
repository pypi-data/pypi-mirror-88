import { __assign, __read, __spread } from "tslib";
import { getDiffInMinutes, TWO_WEEKS } from 'app/components/charts/utils';
import { t } from 'app/locale';
import { escapeDoubleQuotes } from 'app/utils';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { formatVersion } from 'app/utils/formatters';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { WEB_VITAL_DETAILS } from 'app/views/performance/transactionVitals/constants';
import { YAxis } from './releaseChartControls';
export function getInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes > TWO_WEEKS) {
        return '6h';
    }
    else {
        return '1h';
    }
}
export function getReleaseEventView(selection, version, yAxis, eventType, organization, 
/**
 * Indicates that we're only interested in the current release.
 * This is useful for the event meta end point where we don't want
 * to include the other releases.
 */
currentOnly) {
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var releaseFilter = currentOnly ? "release:" + version : '';
    var toOther = "to_other(release,\"" + escapeDoubleQuotes(version) + "\",others,current)";
    // this orderby ensures that the order is [others, current]
    var toOtherAlias = getAggregateAlias(toOther);
    var baseQuery = {
        id: undefined,
        version: 2,
        name: t('Release') + " " + formatVersion(version),
        fields: ["count()", toOther],
        orderby: toOtherAlias,
        range: period,
        environment: environments,
        projects: projects,
        start: start ? getUtcDateString(start) : undefined,
        end: end ? getUtcDateString(end) : undefined,
    };
    switch (yAxis) {
        case YAxis.FAILED_TRANSACTIONS:
            var statusFilters = ['ok', 'cancelled', 'unknown'].map(function (s) { return "!transaction.status:" + s; });
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults(__spread(['event.type:transaction', releaseFilter], statusFilters).filter(Boolean))) }));
        case YAxis.COUNT_LCP:
        case YAxis.COUNT_DURATION:
            var column = yAxis === YAxis.COUNT_DURATION ? 'transaction.duration' : 'measurements.lcp';
            var threshold = yAxis === YAxis.COUNT_DURATION
                ? organization === null || organization === void 0 ? void 0 : organization.apdexThreshold : WEB_VITAL_DETAILS[WebVital.LCP].failureThreshold;
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults([
                    'event.type:transaction',
                    releaseFilter,
                    threshold ? column + ":>" + threshold : '',
                ].filter(Boolean))) }));
        case YAxis.EVENTS:
            var eventTypeFilter = eventType === 'all' ? '' : "event.type:" + eventType;
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults([releaseFilter, eventTypeFilter].filter(Boolean))) }));
        default:
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { fields: ['title', 'count()', 'event.type', 'issue', 'last_seen()'], query: stringifyQueryObject(new QueryResults(["release:" + version, '!event.type:transaction'])), orderby: '-last_seen' }));
    }
}
//# sourceMappingURL=utils.jsx.map