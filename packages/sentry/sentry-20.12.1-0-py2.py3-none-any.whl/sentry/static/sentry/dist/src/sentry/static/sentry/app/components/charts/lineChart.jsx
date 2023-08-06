import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import LineSeries from './series/lineSeries';
import BaseChart from './baseChart';
var LineChart = /** @class */ (function (_super) {
    __extends(LineChart, _super);
    function LineChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LineChart.prototype.render = function () {
        var _a = this.props, series = _a.series, seriesOptions = _a.seriesOptions, props = __rest(_a, ["series", "seriesOptions"]);
        return (<BaseChart {...props} series={series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data, dataArray = _a.dataArray, options = __rest(_a, ["seriesName", "data", "dataArray"]);
            return LineSeries(__assign(__assign(__assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(function (_a) {
                    var value = _a.value, name = _a.name;
                    return [name, value];
                }), animation: false, animationThreshold: 1, animationDuration: 0 }));
        })}/>);
    };
    return LineChart;
}(React.Component));
export default LineChart;
//# sourceMappingURL=lineChart.jsx.map