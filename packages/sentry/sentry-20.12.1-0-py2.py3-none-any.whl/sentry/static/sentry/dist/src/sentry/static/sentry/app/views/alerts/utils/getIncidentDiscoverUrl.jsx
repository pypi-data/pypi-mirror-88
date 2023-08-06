import { __assign, __rest } from "tslib";
import EventView from 'app/utils/discover/eventView';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getStartEndFromStats } from 'app/views/alerts/utils';
import { Dataset } from 'app/views/settings/incidentRules/types';
/**
 * Gets the URL for a discover view of the incident with the following default
 * parameters:
 *
 * - Ordered by the incident aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alerts: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alerts: [transaction, count()]
 * - Start and end are scoped to the same period as the alert rule
 */
export function getIncidentDiscoverUrl(opts) {
    var _a;
    var orgSlug = opts.orgSlug, projects = opts.projects, incident = opts.incident, stats = opts.stats, extraQueryParams = opts.extraQueryParams;
    if (!projects || !projects.length || !incident || !stats) {
        return '';
    }
    var timeWindowString = incident.alertRule.timeWindow + "m";
    var _b = getStartEndFromStats(stats), start = _b.start, end = _b.end;
    var discoverQuery = __assign({ id: undefined, name: (incident && incident.title) || '', orderby: "-" + getAggregateAlias(incident.alertRule.aggregate), yAxis: incident.alertRule.aggregate, query: (_a = incident === null || incident === void 0 ? void 0 : incident.discoverQuery) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(function (_a) {
            var slug = _a.slug;
            return incident.projects.includes(slug);
        })
            .map(function (_a) {
            var id = _a.id;
            return Number(id);
        }), version: 2, fields: incident.alertRule.dataset === Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', incident.alertRule.aggregate], start: start,
        end: end }, extraQueryParams);
    var discoverView = EventView.fromSavedQuery(discoverQuery);
    var _c = discoverView.getResultsViewUrlTarget(orgSlug), query = _c.query, toObject = __rest(_c, ["query"]);
    return __assign({ query: __assign(__assign({}, query), { interval: timeWindowString }) }, toObject);
}
//# sourceMappingURL=getIncidentDiscoverUrl.jsx.map