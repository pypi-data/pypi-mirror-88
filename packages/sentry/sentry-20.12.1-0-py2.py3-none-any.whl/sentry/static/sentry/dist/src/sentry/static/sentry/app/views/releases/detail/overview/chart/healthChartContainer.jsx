import { __extends } from "tslib";
import React from 'react';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { IconWarning } from 'app/icons';
import HealthChart from './healthChart';
var ReleaseChartContainer = /** @class */ (function (_super) {
    __extends(ReleaseChartContainer, _super);
    function ReleaseChartContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldRecalculateVisibleSeries: true,
        };
        _this.handleVisibleSeriesRecalculated = function () {
            _this.setState({ shouldRecalculateVisibleSeries: false });
        };
        return _this;
    }
    ReleaseChartContainer.prototype.render = function () {
        var _this = this;
        var _a = this.props, loading = _a.loading, errored = _a.errored, reloading = _a.reloading, chartData = _a.chartData, selection = _a.selection, yAxis = _a.yAxis, router = _a.router, platform = _a.platform, title = _a.title, help = _a.help;
        var shouldRecalculateVisibleSeries = this.state.shouldRecalculateVisibleSeries;
        var datetime = selection.datetime;
        var utc = datetime.utc, period = datetime.period, start = datetime.start, end = datetime.end;
        return (<ChartZoom router={router} period={period} utc={utc} start={start} end={end}>
        {function (zoomRenderProps) {
            if (errored) {
                return (<ErrorPanel>
                <IconWarning color="gray300" size="lg"/>
              </ErrorPanel>);
            }
            // Stack the toolbox under the legend.
            // so all series names are clickable.
            zoomRenderProps.toolBox.z = -1;
            return (<TransitionChart loading={loading} reloading={reloading}>
              <TransparentLoadingMask visible={reloading}/>
              <HealthChart utc={utc} timeseriesData={chartData} zoomRenderProps={zoomRenderProps} reloading={reloading} yAxis={yAxis} location={router.location} shouldRecalculateVisibleSeries={shouldRecalculateVisibleSeries} onVisibleSeriesRecalculated={_this.handleVisibleSeriesRecalculated} platform={platform} title={title} help={help}/>
            </TransitionChart>);
        }}
      </ChartZoom>);
    };
    return ReleaseChartContainer;
}(React.Component));
export default ReleaseChartContainer;
//# sourceMappingURL=healthChartContainer.jsx.map