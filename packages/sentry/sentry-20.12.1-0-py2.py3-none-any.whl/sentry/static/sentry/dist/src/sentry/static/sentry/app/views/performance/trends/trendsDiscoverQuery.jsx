import { __assign, __rest } from "tslib";
import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
import { getCurrentTrendFunction } from 'app/views/performance/trends/utils';
export function getTrendsRequestPayload(props) {
    var eventView = props.eventView;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    var trendFunction = getCurrentTrendFunction(props.location);
    apiPayload.trendFunction = trendFunction.field;
    apiPayload.trendType = eventView === null || eventView === void 0 ? void 0 : eventView.trendType;
    apiPayload.interval = eventView === null || eventView === void 0 ? void 0 : eventView.interval;
    apiPayload.middle = eventView === null || eventView === void 0 ? void 0 : eventView.middle;
    return apiPayload;
}
function TrendsDiscoverQuery(props) {
    return (<GenericDiscoverQuery route="events-trends-stats" getRequestPayload={getTrendsRequestPayload} {...props}>
      {function (_a) {
        var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
        return props.children(__assign({ trendsData: tableData }, rest));
    }}
    </GenericDiscoverQuery>);
}
function EventsDiscoverQuery(props) {
    return (<GenericDiscoverQuery route="events-trends" getRequestPayload={getTrendsRequestPayload} {...props}>
      {function (_a) {
        var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
        return props.children(__assign({ trendsData: tableData }, rest));
    }}
    </GenericDiscoverQuery>);
}
export var TrendsEventsDiscoverQuery = withApi(EventsDiscoverQuery);
export default withApi(TrendsDiscoverQuery);
//# sourceMappingURL=trendsDiscoverQuery.jsx.map