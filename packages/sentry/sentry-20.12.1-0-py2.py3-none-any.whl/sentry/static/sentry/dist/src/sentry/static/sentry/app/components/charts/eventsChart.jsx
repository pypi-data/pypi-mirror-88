import { __assign, __extends, __read, __rest, __spread } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import AreaChart from 'app/components/charts/areaChart';
import BarChart from 'app/components/charts/barChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval } from 'app/components/charts/utils';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { aggregateMultiPlotType } from 'app/utils/discover/fields';
import theme from 'app/utils/theme';
import EventsRequest from './eventsRequest';
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        _this.handleLegendSelectChanged = function (legendChange) {
            var _a = _this.props.disableableSeries, disableableSeries = _a === void 0 ? [] : _a;
            var selected = legendChange.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                // we only want them to be able to disable the Releases series,
                // and not any of the other possible series here
                var disableable = key === 'Releases' || disableableSeries.includes(key);
                state[key] = disableable ? selected[key] : true;
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (isEqual(this.props.timeseriesData, nextProps.timeseriesData) &&
            isEqual(this.props.releaseSeries, nextProps.releaseSeries) &&
            isEqual(this.props.previousTimeseriesData, nextProps.previousTimeseriesData)) {
            return false;
        }
        return true;
    };
    Chart.prototype.getChartComponent = function () {
        var _a = this.props, showDaily = _a.showDaily, timeseriesData = _a.timeseriesData, yAxis = _a.yAxis;
        if (showDaily) {
            return BarChart;
        }
        if (timeseriesData.length > 1) {
            switch (aggregateMultiPlotType(yAxis)) {
                case 'line':
                    return LineChart;
                case 'area':
                    return AreaChart;
                default:
                    throw new Error("Unknown multi plot type for " + yAxis);
            }
        }
        return AreaChart;
    };
    Chart.prototype.render = function () {
        var _a = this.props, _loading = _a.loading, _reloading = _a.reloading, yAxis = _a.yAxis, releaseSeries = _a.releaseSeries, zoomRenderProps = _a.zoomRenderProps, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData, showLegend = _a.showLegend, legendOptions = _a.legendOptions, chartOptionsProp = _a.chartOptions, currentSeriesName = _a.currentSeriesName, previousSeriesName = _a.previousSeriesName, seriesNameTransformer = _a.seriesNameTransformer, colors = _a.colors, props = __rest(_a, ["loading", "reloading", "yAxis", "releaseSeries", "zoomRenderProps", "timeseriesData", "previousTimeseriesData", "showLegend", "legendOptions", "chartOptions", "currentSeriesName", "previousSeriesName", "seriesNameTransformer", "colors"]);
        var seriesSelection = this.state.seriesSelection;
        var data = [currentSeriesName !== null && currentSeriesName !== void 0 ? currentSeriesName : t('Current'), previousSeriesName !== null && previousSeriesName !== void 0 ? previousSeriesName : t('Previous')];
        if (Array.isArray(releaseSeries)) {
            data.push(t('Releases'));
        }
        var legend = showLegend && __assign({ right: 16, top: 12, icon: 'circle', itemHeight: 8, itemWidth: 8, itemGap: 12, align: 'left', textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            }, data: data, selected: seriesSelection }, (legendOptions !== null && legendOptions !== void 0 ? legendOptions : {}));
        var chartOptions = __assign({ colors: colors !== null && colors !== void 0 ? colors : theme.charts.getColorPalette(timeseriesData.length - 2), grid: {
                left: '24px',
                right: '24px',
                top: '32px',
                bottom: '12px',
            }, seriesOptions: {
                showSymbol: false,
            }, tooltip: {
                trigger: 'axis',
                truncate: 80,
                valueFormatter: function (value) { return tooltipFormatter(value, yAxis); },
            }, yAxis: {
                axisLabel: {
                    color: theme.gray200,
                    formatter: function (value) { return axisLabelFormatter(value, yAxis); },
                },
            } }, (chartOptionsProp !== null && chartOptionsProp !== void 0 ? chartOptionsProp : {}));
        var Component = this.getChartComponent();
        var series = Array.isArray(releaseSeries)
            ? __spread(timeseriesData, releaseSeries) : timeseriesData;
        if (seriesNameTransformer) {
            series.forEach(function (s) {
                s.seriesName = seriesNameTransformer(s.seriesName);
            });
        }
        return (<Component {...props} {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={this.handleLegendSelectChanged} series={series} previousPeriod={previousTimeseriesData ? [previousTimeseriesData] : null}/>);
    };
    Chart.propTypes = {
        loading: PropTypes.bool,
        reloading: PropTypes.bool,
        releaseSeries: PropTypes.array,
        zoomRenderProps: PropTypes.object,
        timeseriesData: PropTypes.array,
        showLegend: PropTypes.bool,
        previousTimeseriesData: PropTypes.object,
        currentSeriesName: PropTypes.string,
        previousSeriesName: PropTypes.string,
        seriesNameTransformer: PropTypes.func,
        showDaily: PropTypes.bool,
        yAxis: PropTypes.string,
        colors: PropTypes.array,
        disableableSeries: PropTypes.array,
        legendOptions: PropTypes.object,
        chartOptions: PropTypes.object,
    };
    return Chart;
}(React.Component));
var EventsChart = /** @class */ (function (_super) {
    __extends(EventsChart, _super);
    function EventsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsChart.prototype.render = function () {
        var _a = this.props, api = _a.api, period = _a.period, utc = _a.utc, query = _a.query, router = _a.router, start = _a.start, end = _a.end, projects = _a.projects, environments = _a.environments, showLegend = _a.showLegend, yAxis = _a.yAxis, disablePrevious = _a.disablePrevious, disableReleases = _a.disableReleases, emphasizeReleases = _a.emphasizeReleases, currentName = _a.currentSeriesName, previousName = _a.previousSeriesName, seriesNameTransformer = _a.seriesNameTransformer, field = _a.field, interval = _a.interval, showDaily = _a.showDaily, topEvents = _a.topEvents, orderby = _a.orderby, confirmedQuery = _a.confirmedQuery, colors = _a.colors, chartHeader = _a.chartHeader, legendOptions = _a.legendOptions, chartOptions = _a.chartOptions, preserveReleaseQueryParams = _a.preserveReleaseQueryParams, releaseQueryExtra = _a.releaseQueryExtra, props = __rest(_a, ["api", "period", "utc", "query", "router", "start", "end", "projects", "environments", "showLegend", "yAxis", "disablePrevious", "disableReleases", "emphasizeReleases", "currentSeriesName", "previousSeriesName", "seriesNameTransformer", "field", "interval", "showDaily", "topEvents", "orderby", "confirmedQuery", "colors", "chartHeader", "legendOptions", "chartOptions", "preserveReleaseQueryParams", "releaseQueryExtra"]);
        // Include previous only on relative dates (defaults to relative if no start and end)
        var includePrevious = !disablePrevious && !start && !end;
        var previousSeriesName = previousName !== null && previousName !== void 0 ? previousName : (yAxis ? t('previous %s', yAxis) : undefined);
        var currentSeriesName = currentName !== null && currentName !== void 0 ? currentName : yAxis;
        var intervalVal = showDaily ? '1d' : interval || getInterval(this.props, true);
        var chartImplementation = function (_a) {
            var zoomRenderProps = _a.zoomRenderProps, releaseSeries = _a.releaseSeries, errored = _a.errored, loading = _a.loading, reloading = _a.reloading, results = _a.results, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData;
            if (errored) {
                return (<ErrorPanel>
            <IconWarning color="gray300" size="lg"/>
          </ErrorPanel>);
            }
            var seriesData = results ? results : timeseriesData;
            // Stack the toolbox under the legend.
            // so all series names are clickable.
            zoomRenderProps.toolBox.z = -1;
            return (<TransitionChart loading={loading} reloading={reloading}>
          <TransparentLoadingMask visible={reloading}/>

          {React.isValidElement(chartHeader) && chartHeader}

          <Chart {...zoomRenderProps} loading={loading} reloading={reloading} utc={utc} showLegend={showLegend} releaseSeries={releaseSeries || []} timeseriesData={seriesData} previousTimeseriesData={previousTimeseriesData} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} seriesNameTransformer={seriesNameTransformer} stacked={typeof topEvents === 'number' && topEvents > 0} yAxis={yAxis} showDaily={showDaily} colors={colors} legendOptions={legendOptions} chartOptions={chartOptions}/>
        </TransitionChart>);
        };
        if (!disableReleases) {
            var previousChart_1 = chartImplementation;
            chartImplementation = function (chartProps) { return (<ReleaseSeries utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} emphasizeReleases={emphasizeReleases} preserveQueryParams={preserveReleaseQueryParams} queryExtra={releaseQueryExtra}>
          {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return previousChart_1(__assign(__assign({}, chartProps), { releaseSeries: releaseSeries }));
            }}
        </ReleaseSeries>); };
        }
        return (<ChartZoom router={router} period={period} utc={utc} projects={projects} environments={environments} {...props}>
        {function (zoomRenderProps) { return (<EventsRequest {...props} api={api} period={period} project={projects} environment={environments} start={start} end={end} interval={intervalVal} query={query} includePrevious={includePrevious} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} yAxis={yAxis} field={field} orderby={orderby} topEvents={topEvents} confirmedQuery={confirmedQuery}>
            {function (eventData) {
            return chartImplementation(__assign(__assign({}, eventData), { zoomRenderProps: zoomRenderProps }));
        }}
          </EventsRequest>); }}
      </ChartZoom>);
    };
    EventsChart.propTypes = {
        api: PropTypes.object,
        projects: PropTypes.arrayOf(PropTypes.number),
        environments: PropTypes.arrayOf(PropTypes.string),
        period: PropTypes.string,
        query: PropTypes.string,
        start: PropTypes.instanceOf(Date),
        end: PropTypes.instanceOf(Date),
        utc: PropTypes.bool,
        router: PropTypes.object,
        showLegend: PropTypes.bool,
        yAxis: PropTypes.string,
        disablePrevious: PropTypes.bool,
        disableReleases: PropTypes.bool,
        emphasizeReleases: PropTypes.array,
        currentSeriesName: PropTypes.string,
        previousSeriesName: PropTypes.string,
        seriesNameTransformer: PropTypes.func,
        topEvents: PropTypes.number,
        field: PropTypes.arrayOf(PropTypes.string),
        showDaily: PropTypes.bool,
        orderby: PropTypes.string,
        confirmedQuery: PropTypes.bool,
        colors: PropTypes.array,
        preserveReleaseQueryParams: PropTypes.bool,
        releaseQueryExtras: PropTypes.object,
        disableableSeries: PropTypes.array,
        chartHeader: PropTypes.object,
        legendOptions: PropTypes.object,
        chartOptions: PropTypes.object,
    };
    return EventsChart;
}(React.Component));
export default EventsChart;
//# sourceMappingURL=eventsChart.jsx.map