import { __extends, __read } from "tslib";
import React from 'react';
import MiniBarChart from 'app/components/charts/miniBarChart';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import withApi from 'app/utils/withApi';
var InternalStatChart = /** @class */ (function (_super) {
    __extends(InternalStatChart, _super);
    function InternalStatChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: true,
            data: null,
        };
        return _this;
    }
    InternalStatChart.prototype.componentDidMount = function () {
        this.fetchData();
    };
    InternalStatChart.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.loading !== nextState.loading;
    };
    InternalStatChart.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.since !== this.props.since ||
            prevProps.stat !== this.props.stat ||
            prevProps.resolution !== this.props.resolution) {
            this.fetchData();
        }
    };
    InternalStatChart.prototype.fetchData = function () {
        var _this = this;
        this.setState({ loading: true });
        this.props.api.request('/internal/stats/', {
            method: 'GET',
            data: {
                since: this.props.since,
                resolution: this.props.resolution,
                key: this.props.stat,
            },
            success: function (data) {
                return _this.setState({
                    data: data,
                    loading: false,
                    error: false,
                });
            },
            error: function () { return _this.setState({ error: true }); },
        });
    };
    InternalStatChart.prototype.render = function () {
        var _a;
        var _b = this.state, loading = _b.loading, error = _b.error, data = _b.data;
        var _c = this.props, label = _c.label, height = _c.height;
        if (loading) {
            return <LoadingIndicator />;
        }
        else if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        var series = {
            seriesName: label,
            data: (_a = data === null || data === void 0 ? void 0 : data.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
                return ({
                    name: timestamp * 1000,
                    value: value,
                });
            })) !== null && _a !== void 0 ? _a : [],
        };
        return (<MiniBarChart height={height !== null && height !== void 0 ? height : 150} series={[series]} isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    };
    return InternalStatChart;
}(React.Component));
export default withApi(InternalStatChart);
//# sourceMappingURL=internalStatChart.jsx.map