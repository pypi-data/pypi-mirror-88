import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { WebVital } from 'app/utils/discover/fields';
import { WEB_VITAL_DETAILS } from 'app/views/performance/transactionVitals/constants';
export var YAxis;
(function (YAxis) {
    YAxis["SESSIONS"] = "sessions";
    YAxis["USERS"] = "users";
    YAxis["CRASH_FREE"] = "crashFree";
    YAxis["SESSION_DURATION"] = "sessionDuration";
    YAxis["EVENTS"] = "events";
    YAxis["FAILED_TRANSACTIONS"] = "failedTransactions";
    YAxis["COUNT_DURATION"] = "countDuration";
    YAxis["COUNT_LCP"] = "countLCP";
})(YAxis || (YAxis = {}));
export var EventType;
(function (EventType) {
    EventType["ALL"] = "all";
    EventType["CSP"] = "csp";
    EventType["DEFAULT"] = "default";
    EventType["ERROR"] = "error";
    EventType["TRANSACTION"] = "transaction";
})(EventType || (EventType = {}));
export var PERFORMANCE_AXIS = [
    YAxis.FAILED_TRANSACTIONS,
    YAxis.COUNT_DURATION,
    YAxis.COUNT_LCP,
];
var ReleaseChartControls = function (_a) {
    var summary = _a.summary, yAxis = _a.yAxis, onYAxisChange = _a.onYAxisChange, organization = _a.organization, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover, hasPerformance = _a.hasPerformance, eventType = _a.eventType, onEventTypeChange = _a.onEventTypeChange;
    var noHealthDataTooltip = !hasHealthData
        ? t('This view is only available with release health data.')
        : undefined;
    var noDiscoverTooltip = !hasDiscover
        ? t('This view is only available with Discover.')
        : undefined;
    var noPerformanceTooltip = !hasPerformance
        ? t('This view is only available with Performance Monitoring.')
        : undefined;
    var yAxisOptions = [
        {
            value: YAxis.SESSIONS,
            label: t('Session Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.SESSION_DURATION,
            label: t('Session Duration'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.USERS,
            label: t('User Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.CRASH_FREE,
            label: t('Crash Free Rate'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.FAILED_TRANSACTIONS,
            label: t('Failure Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_DURATION,
            label: t('Slow Count (duration)'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_LCP,
            label: t('Slow Count (LCP)'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.EVENTS,
            label: t('Event Count'),
            disabled: !hasDiscover,
            tooltip: noDiscoverTooltip,
        },
    ];
    var eventTypeOptions = [
        { value: EventType.ALL, label: t('All') },
        { value: EventType.CSP, label: t('CSP') },
        { value: EventType.DEFAULT, label: t('Default') },
        { value: EventType.ERROR, label: 'Error' },
        { value: EventType.TRANSACTION, label: t('Transaction') },
    ];
    var getSummaryHeading = function () {
        switch (yAxis) {
            case YAxis.USERS:
                return t('Total Active Users');
            case YAxis.CRASH_FREE:
                return t('Average Rate');
            case YAxis.SESSION_DURATION:
                return t('Median Duration');
            case YAxis.EVENTS:
                return t('Total Events');
            case YAxis.FAILED_TRANSACTIONS:
                return t('Failed Transactions');
            case YAxis.COUNT_DURATION:
                return t("Count over " + organization.apdexThreshold + "ms");
            case YAxis.COUNT_LCP:
                return t("Count over " + WEB_VITAL_DETAILS[WebVital.LCP].failureThreshold + "ms");
            case YAxis.SESSIONS:
            default:
                return t('Total Sessions');
        }
    };
    return (<StyledChartControls>
      <InlineContainer>
        <SectionHeading key="total-label">{getSummaryHeading()}</SectionHeading>
        <SectionValue key="total-value">{summary}</SectionValue>
        {(yAxis === YAxis.EVENTS || PERFORMANCE_AXIS.includes(yAxis)) && (<QuestionTooltip position="top" size="sm" title="This count includes only the current release."/>)}
      </InlineContainer>
      <InlineContainer>
        {yAxis === YAxis.EVENTS && (<OptionSelector title={t('Event Type')} selected={eventType !== null && eventType !== void 0 ? eventType : EventType.ALL} options={eventTypeOptions} onChange={onEventTypeChange}/>)}
        <OptionSelector title={t('Display')} selected={yAxis} options={yAxisOptions} onChange={onYAxisChange}/>
      </InlineContainer>
    </StyledChartControls>);
};
var StyledChartControls = styled(ChartControls)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    padding-bottom: ", ";\n    button {\n      font-size: ", ";\n    }\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    padding-bottom: ", ";\n    button {\n      font-size: ", ";\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1), space(1.5), function (p) { return p.theme.fontSizeSmall; });
export default ReleaseChartControls;
var templateObject_1;
//# sourceMappingURL=releaseChartControls.jsx.map