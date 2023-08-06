import { __extends } from "tslib";
import React from 'react';
import AsyncComponent from 'app/components/asyncComponent';
import MiniBarChart from 'app/components/charts/miniBarChart';
import { Panel, PanelBody } from 'app/components/panels';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var MonitorStats = /** @class */ (function (_super) {
    __extends(MonitorStats, _super);
    function MonitorStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MonitorStats.prototype.getEndpoints = function () {
        var monitor = this.props.monitor;
        var until = Math.floor(new Date().getTime() / 1000);
        var since = until - 3600 * 24 * 30;
        return [
            [
                'stats',
                "/monitors/" + monitor.id + "/stats/",
                {
                    query: {
                        since: since,
                        until: until,
                        resolution: '1d',
                    },
                },
            ],
        ];
    };
    MonitorStats.prototype.renderBody = function () {
        var _a;
        var emptyStats = true;
        var success = {
            seriesName: t('Successful'),
            data: [],
        };
        var failed = {
            seriesName: t('Failed'),
            data: [],
        };
        (_a = this.state.stats) === null || _a === void 0 ? void 0 : _a.forEach(function (p) {
            if (p.ok || p.error) {
                emptyStats = false;
            }
            var timestamp = p.ts * 1000;
            success.data.push({ name: timestamp.toString(), value: p.ok });
            failed.data.push({ name: timestamp.toString(), value: p.error });
        });
        var colors = [theme.green300, theme.red300];
        return (<Panel>
        <PanelBody withPadding>
          {!emptyStats ? (<MiniBarChart isGroupedByDate showTimeInTooltip labelYAxisExtents stacked colors={colors} height={150} series={[success, failed]}/>) : (<EmptyMessage title={t('Nothing recorded in the last 30 days.')} description={t('All check-ins for this monitor.')}/>)}
        </PanelBody>
      </Panel>);
    };
    return MonitorStats;
}(AsyncComponent));
export default MonitorStats;
//# sourceMappingURL=monitorStats.jsx.map