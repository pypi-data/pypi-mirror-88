import { __read, __spread } from "tslib";
import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
import { vitalsBaseFields, vitalsMehFields, vitalsP75Fields, vitalsPoorFields, } from './utils';
function getRequestPayload(props) {
    var eventView = props.eventView, onlyVital = props.onlyVital;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    var vitalFields = onlyVital
        ? [
            vitalsPoorFields[onlyVital],
            vitalsBaseFields[onlyVital],
            vitalsMehFields[onlyVital],
            vitalsP75Fields[onlyVital],
        ]
        : __spread(Object.values(vitalsPoorFields), Object.values(vitalsMehFields), Object.values(vitalsBaseFields), Object.values(vitalsP75Fields));
    apiPayload.field = __spread(vitalFields);
    delete apiPayload.sort;
    return apiPayload;
}
function VitalsCardDiscoverQuery(props) {
    return (<GenericDiscoverQuery getRequestPayload={getRequestPayload} route="eventsv2" {...props}/>);
}
export default withApi(VitalsCardDiscoverQuery);
//# sourceMappingURL=vitalsCardsDiscoverQuery.jsx.map