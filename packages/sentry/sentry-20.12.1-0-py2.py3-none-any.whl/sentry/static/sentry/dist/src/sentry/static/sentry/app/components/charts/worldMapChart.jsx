import { __assign, __awaiter, __extends, __generator, __read, __rest } from "tslib";
import React from 'react';
import echarts from 'echarts';
import { withTheme } from 'emotion-theming';
import max from 'lodash/max';
import theme from 'app/utils/theme';
import VisualMap from './components/visualMap';
import MapSeries from './series/mapSeries';
import BaseChart from './baseChart';
var WorldMapChart = /** @class */ (function (_super) {
    __extends(WorldMapChart, _super);
    function WorldMapChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            countryToCodeMap: null,
            map: null,
            codeToCountryMap: null,
        };
        return _this;
    }
    WorldMapChart.prototype.componentDidMount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, countryToCodeMap, worldMap;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, Promise.all([
                            import(/* webpackChunkName: "countryCodesMap" */ 'app/data/countryCodesMap'),
                            import(/* webpackChunkName: "worldMapGeoJson" */ 'app/data/world.json'),
                        ])];
                    case 1:
                        _a = __read.apply(void 0, [_b.sent(), 2]), countryToCodeMap = _a[0], worldMap = _a[1];
                        echarts.registerMap('sentryWorld', worldMap.default);
                        // eslint-disable-next-line
                        this.setState({
                            countryToCodeMap: countryToCodeMap.default,
                            map: worldMap.default,
                            codeToCountryMap: Object.fromEntries(Object.entries(countryToCodeMap.default).map(function (_a) {
                                var _b = __read(_a, 2), country = _b[0], code = _b[1];
                                return [code, country];
                            })),
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    WorldMapChart.prototype.render = function () {
        var _this = this;
        var _a = this.state, countryToCodeMap = _a.countryToCodeMap, map = _a.map;
        if (countryToCodeMap === null || map === null) {
            return null;
        }
        var _b = this.props, series = _b.series, seriesOptions = _b.seriesOptions, props = __rest(_b, ["series", "seriesOptions"]);
        var processedSeries = series.map(function (_a) {
            var _b;
            var seriesName = _a.seriesName, data = _a.data, options = __rest(_a, ["seriesName", "data"]);
            return MapSeries(__assign(__assign(__assign({}, seriesOptions), options), { map: 'sentryWorld', name: seriesName, nameMap: (_b = _this.state.countryToCodeMap) !== null && _b !== void 0 ? _b : undefined, aspectScale: 0.85, zoom: 1.3, center: [10.97, 9.71], itemStyle: {
                    areaColor: theme.gray200,
                    borderColor: theme.backgroundSecondary,
                    emphasis: {
                        areaColor: theme.orange300,
                    },
                }, label: {
                    emphasis: {
                        show: false,
                    },
                }, data: data }));
        });
        // TODO(billy):
        // For absolute values, we want min/max to based on min/max of series
        // Otherwise it should be 0-100
        var maxValue = max(series.map(function (_a) {
            var data = _a.data;
            return max(data.map(function (_a) {
                var value = _a.value;
                return value;
            }));
        })) || 1;
        var tooltipFormatter = function (format) {
            var _a;
            var _b = Array.isArray(format) ? format[0] : format, marker = _b.marker, name = _b.name, value = _b.value;
            // If value is NaN, don't show anything because we won't have a country code either
            if (isNaN(value)) {
                return '';
            }
            // `value` should be a number
            var formattedValue = typeof value === 'number' ? value.toLocaleString() : '';
            var countryOrCode = ((_a = _this.state.codeToCountryMap) === null || _a === void 0 ? void 0 : _a[name]) || name;
            return [
                "<div class=\"tooltip-series tooltip-series-solo\">\n                 <div><span class=\"tooltip-label\">" + marker + " <strong>" + countryOrCode + "</strong></span> " + formattedValue + "</div>\n              </div>",
                '<div class="tooltip-arrow"></div>',
            ].join('');
        };
        return (<BaseChart options={{
            backgroundColor: theme.backgroundSecondary,
            visualMap: [
                VisualMap({
                    left: 'right',
                    min: 0,
                    max: maxValue,
                    inRange: {
                        color: [theme.purple200, theme.purple300],
                    },
                    text: ['High', 'Low'],
                    // Whether show handles, which can be dragged to adjust "selected range".
                    // False because the handles are pretty ugly
                    calculable: false,
                }),
            ],
        }} {...props} yAxis={null} xAxis={null} series={processedSeries} tooltip={{
            formatter: tooltipFormatter,
        }}/>);
    };
    return WorldMapChart;
}(React.Component));
export default withTheme(WorldMapChart);
//# sourceMappingURL=worldMapChart.jsx.map