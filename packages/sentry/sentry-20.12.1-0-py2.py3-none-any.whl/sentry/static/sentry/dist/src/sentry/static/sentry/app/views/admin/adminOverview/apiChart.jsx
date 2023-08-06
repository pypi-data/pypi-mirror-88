import { __extends } from "tslib";
import React from 'react';
import MiniBarChart from 'app/components/charts/miniBarChart';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
var initialState = {
    error: false,
    loading: true,
    rawData: {
        'client-api.all-versions.responses.2xx': [],
        'client-api.all-versions.responses.4xx': [],
        'client-api.all-versions.responses.5xx': [],
    },
};
var ApiChart = /** @class */ (function (_super) {
    __extends(ApiChart, _super);
    function ApiChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.fetchData = function () {
            var statNameList = [
                'client-api.all-versions.responses.2xx',
                'client-api.all-versions.responses.4xx',
                'client-api.all-versions.responses.5xx',
            ];
            statNameList.forEach(function (statName) {
                _this.props.api.request('/internal/stats/', {
                    method: 'GET',
                    data: {
                        since: _this.props.since,
                        resolution: _this.props.resolution,
                        key: statName,
                    },
                    success: function (data) {
                        _this.setState(function (prevState) {
                            var rawData = prevState.rawData;
                            rawData[statName] = data;
                            return {
                                rawData: rawData,
                            };
                        }, _this.requestFinished);
                    },
                    error: function () {
                        _this.setState({
                            error: true,
                        });
                    },
                });
            });
        };
        _this.requestFinished = function () {
            var rawData = _this.state.rawData;
            if (rawData['client-api.all-versions.responses.2xx'] &&
                rawData['client-api.all-versions.responses.4xx'] &&
                rawData['client-api.all-versions.responses.5xx']) {
                _this.setState({
                    loading: false,
                });
            }
        };
        return _this;
    }
    ApiChart.prototype.componentWillMount = function () {
        this.fetchData();
    };
    ApiChart.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.props.since !== nextProps.since) {
            this.setState(initialState, this.fetchData);
        }
    };
    ApiChart.prototype.processRawSeries = function (series) {
        return series.map(function (item) { return ({ name: item[0] * 1000, value: item[1] }); });
    };
    ApiChart.prototype.getChartSeries = function () {
        var rawData = this.state.rawData;
        return [
            {
                seriesName: '2xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.2xx']),
                color: theme.green200,
            },
            {
                seriesName: '4xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.4xx']),
                color: theme.blue300,
            },
            {
                seriesName: '5xx',
                data: this.processRawSeries(rawData['client-api.all-versions.responses.5xx']),
                color: theme.red200,
            },
        ];
    };
    ApiChart.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error;
        if (loading) {
            return <LoadingIndicator />;
        }
        else if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        var series = this.getChartSeries();
        var colors = series.map(function (_a) {
            var color = _a.color;
            return color;
        });
        return (<MiniBarChart series={series} colors={colors} height={110} stacked isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    };
    return ApiChart;
}(React.Component));
export default withApi(ApiChart);
//# sourceMappingURL=apiChart.jsx.map