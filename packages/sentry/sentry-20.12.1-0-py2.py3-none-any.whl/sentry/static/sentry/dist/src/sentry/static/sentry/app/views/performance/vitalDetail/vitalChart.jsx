import { __assign, __extends, __read, __rest, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import * as ReactRouter from 'react-router';
import ChartZoom from 'app/components/charts/chartZoom';
import MarkLine from 'app/components/charts/components/markLine';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval, getSeriesSelection } from 'app/components/charts/utils';
import { Panel } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { WebVital } from 'app/utils/discover/fields';
import getDynamicText from 'app/utils/getDynamicText';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import { ChartContainer, HeaderTitleLegend } from '../styles';
import { replaceSeriesName, transformEventStatsSmoothed } from '../trends/utils';
import { getMaxOfSeries, vitalNameFromLocation, webVitalMeh, webVitalPoor } from './utils';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var VitalChart = /** @class */ (function (_super) {
    __extends(VitalChart, _super);
    function VitalChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { unselectedSeries: unselected }) });
            browserHistory.push(to);
        };
        return _this;
    }
    VitalChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router;
        var start = this.props.start
            ? getUtcToLocalDateObject(this.props.start)
            : undefined;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : undefined;
        var utc = decodeScalar(router.location.query.utc);
        var vitalName = vitalNameFromLocation(location);
        var yAxis = ["p75(" + vitalName + ")"];
        var legend = {
            right: 10,
            top: 0,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
            selected: getSeriesSelection(location),
        };
        var datetimeSelection = {
            start: start || null,
            end: end || null,
            period: statsPeriod,
        };
        var vitalPoor = webVitalPoor[vitalName];
        var vitalMeh = webVitalMeh[vitalName];
        var markLines = [
            {
                seriesName: 'Thresholds',
                type: 'line',
                data: [],
                markLine: MarkLine({
                    silent: true,
                    lineStyle: {
                        color: theme.textColor,
                        type: 'dashed',
                        width: 1,
                    },
                    label: {
                        show: true,
                        position: 'insideEndBottom',
                        formatter: t('Poor'),
                    },
                    data: [
                        {
                            yAxis: vitalPoor,
                        },
                    ],
                }),
            },
            {
                seriesName: 'Thresholds',
                type: 'line',
                data: [],
                markLine: MarkLine({
                    silent: true,
                    lineStyle: {
                        color: theme.textColor,
                        type: 'dashed',
                        width: 1,
                    },
                    label: {
                        show: true,
                        position: 'insideEndBottom',
                        formatter: t('Meh'),
                    },
                    data: [
                        {
                            yAxis: vitalMeh,
                        },
                    ],
                }),
            },
        ];
        var chartOptions = {
            grid: {
                left: '10px',
                right: '10px',
                top: '20px',
                bottom: '0px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: function (value, seriesName) {
                    return tooltipFormatter(value, vitalName === WebVital.CLS ? seriesName : 'p75()');
                },
            },
            yAxis: {
                min: 0,
                max: vitalPoor,
                axisLabel: {
                    color: theme.chartLabel,
                    // coerces the axis to be time based
                    formatter: function (value) { return axisLabelFormatter(value, 'p75()'); },
                },
            },
        };
        return (<Panel>
        <ChartContainer>
          <HeaderTitleLegend>
            {t('Duration p75')}
            <QuestionTooltip size="sm" position="top" title={t("The durations shown should fall under the vital threshold.")}/>
          </HeaderTitleLegend>
          <ChartZoom router={router} period={statsPeriod} projects={project} environments={environment}>
            {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={__spread(project)} environment={__spread(environment)} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={yAxis}>
                {function (_a) {
            var results = _a.timeseriesData, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
            if (errored) {
                return (<ErrorPanel>
                        <IconWarning color="gray500" size="lg"/>
                      </ErrorPanel>);
            }
            var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
            var smoothedResults = transformEventStatsSmoothed(results).smoothedResults;
            var smoothedSeries = smoothedResults
                ? smoothedResults.map(function (_a, i) {
                    var seriesName = _a.seriesName, rest = __rest(_a, ["seriesName"]);
                    return __assign(__assign({ seriesName: replaceSeriesName(seriesName) || 'p75' }, rest), { color: colors[i], lineStyle: {
                            opacity: 1,
                            width: 2,
                        } });
                })
                : [];
            var seriesMax = getMaxOfSeries(smoothedSeries);
            var yAxisMax = Math.max(seriesMax, vitalPoor);
            chartOptions.yAxis.max = yAxisMax * 1.1;
            // Stack the toolbox under the legend.
            // so all series names are clickable.
            zoomRenderProps.toolBox.z = -1;
            return (<ReleaseSeries start={start} end={end} period={statsPeriod} utc={utc} projects={project} environments={environment}>
                      {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return (<TransitionChart loading={loading} reloading={reloading}>
                          <TransparentLoadingMask visible={reloading}/>
                          {getDynamicText({
                    value: (<LineChart {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spread(markLines, releaseSeries, smoothedSeries)}/>),
                    fixed: 'Web Vitals Chart',
                })}
                        </TransitionChart>);
            }}
                    </ReleaseSeries>);
        }}
              </EventsRequest>); }}
          </ChartZoom>
        </ChartContainer>
      </Panel>);
    };
    return VitalChart;
}(React.Component));
export default withApi(ReactRouter.withRouter(VitalChart));
//# sourceMappingURL=vitalChart.jsx.map