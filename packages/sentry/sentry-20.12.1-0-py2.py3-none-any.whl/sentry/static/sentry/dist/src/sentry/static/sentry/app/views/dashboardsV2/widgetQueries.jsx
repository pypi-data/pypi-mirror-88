import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import { doEventsRequest } from 'app/actionCreators/events';
import { getDiffInMinutes, getInterval, isMultiSeriesStats, } from 'app/components/charts/utils';
import { parsePeriodToHours } from 'app/utils/dates';
// Don't fetch more than 4000 bins as we're plotting on a small area.
var MAX_BIN_COUNT = 4000;
function getWidgetInterval(desired, datetimeObj) {
    var desiredPeriod = parsePeriodToHours(desired);
    var selectedRange = getDiffInMinutes(datetimeObj);
    if (selectedRange / desiredPeriod > MAX_BIN_COUNT) {
        return getInterval(datetimeObj, true);
    }
    return desired;
}
function transformSeries(stats, seriesName) {
    return {
        seriesName: seriesName,
        data: stats.data.map(function (_a) {
            var _b = __read(_a, 2), timestamp = _b[0], counts = _b[1];
            return ({
                name: timestamp * 1000,
                value: counts.reduce(function (acc, _a) {
                    var count = _a.count;
                    return acc + count;
                }, 0),
            });
        }),
    };
}
function transformResult(query, result) {
    var output = [];
    var seriesNamePrefix = query.name;
    if (isMultiSeriesStats(result)) {
        // Convert multi-series results into chartable series. Multi series results
        // are created when multiple yAxis are used. Convert the timeseries
        // data into a multi-series result set.  As the server will have
        // replied with a map like: {[titleString: string]: EventsStats}
        var transformed = Object.keys(result)
            .map(function (seriesName) {
            var prefixedName = seriesNamePrefix
                ? seriesNamePrefix + " : " + seriesName
                : seriesName;
            var seriesData = result[seriesName];
            return [seriesData.order || 0, transformSeries(seriesData, prefixedName)];
        })
            .sort(function (a, b) { return a[0] - b[0]; })
            .map(function (item) { return item[1]; });
        output = output.concat(transformed);
    }
    else {
        var field = query.fields[0];
        var prefixedName = seriesNamePrefix ? seriesNamePrefix + " : " + field : field;
        var transformed = transformSeries(result, prefixedName);
        output.push(transformed);
    }
    return output;
}
var WidgetQueries = /** @class */ (function (_super) {
    __extends(WidgetQueries, _super);
    function WidgetQueries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            results: [],
        };
        return _this;
    }
    WidgetQueries.prototype.componentDidMount = function () {
        this.fetchData();
    };
    WidgetQueries.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, widget = _a.widget;
        if (!isEqual(widget.interval, prevProps.widget.interval) ||
            !isEqual(widget.queries, prevProps.widget.queries) ||
            !isEqual(selection, prevProps.selection)) {
            this.fetchData();
        }
    };
    WidgetQueries.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, selection, api, organization, widget, statsPeriod, _b, start, end, projects, environments, interval, promises, completed;
            var _this = this;
            return __generator(this, function (_c) {
                _a = this.props, selection = _a.selection, api = _a.api, organization = _a.organization, widget = _a.widget;
                this.setState({ loading: true, results: [] });
                statsPeriod = selection.datetime.period;
                _b = selection.datetime, start = _b.start, end = _b.end;
                projects = selection.projects, environments = selection.environments;
                interval = getWidgetInterval(widget.interval, {
                    start: start,
                    end: end,
                    period: statsPeriod,
                });
                promises = widget.queries.map(function (query) {
                    // TODO(mark) adapt this based on the type of widget being built.
                    // Table and stats results will need to do a different request.
                    var requestData = {
                        organization: organization,
                        interval: interval,
                        start: start,
                        end: end,
                        project: projects,
                        environment: environments,
                        period: statsPeriod,
                        query: query.conditions,
                        yAxis: query.fields,
                        includePrevious: false,
                    };
                    return doEventsRequest(api, requestData);
                });
                completed = 0;
                promises.forEach(function (promise, i) { return __awaiter(_this, void 0, void 0, function () {
                    var rawResults_1, e_1;
                    return __generator(this, function (_a) {
                        switch (_a.label) {
                            case 0:
                                _a.trys.push([0, 2, , 3]);
                                return [4 /*yield*/, promise];
                            case 1:
                                rawResults_1 = _a.sent();
                                completed++;
                                this.setState(function (prevState) {
                                    var results = prevState.results.concat(transformResult(widget.queries[i], rawResults_1));
                                    return __assign(__assign({}, prevState), { results: results, loading: completed === promises.length ? false : true });
                                });
                                return [3 /*break*/, 3];
                            case 2:
                                e_1 = _a.sent();
                                this.setState({ error: true });
                                return [3 /*break*/, 3];
                            case 3: return [2 /*return*/];
                        }
                    });
                }); });
                return [2 /*return*/];
            });
        });
    };
    WidgetQueries.prototype.render = function () {
        var children = this.props.children;
        var _a = this.state, loading = _a.loading, results = _a.results, error = _a.error;
        return children({ loading: loading, results: results, error: error });
    };
    return WidgetQueries;
}(React.Component));
export default WidgetQueries;
//# sourceMappingURL=widgetQueries.jsx.map