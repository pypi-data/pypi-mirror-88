import { __assign, __awaiter, __extends, __generator, __rest } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import { fetchTotalCount } from 'app/actionCreators/events';
import EventsChart from 'app/components/charts/eventsChart';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { HeaderTitleLegend } from 'app/views/performance/styles';
var ProjectBaseEventsChart = /** @class */ (function (_super) {
    __extends(ProjectBaseEventsChart, _super);
    function ProjectBaseEventsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectBaseEventsChart.prototype.componentDidMount = function () {
        this.fetchTotalCount();
    };
    ProjectBaseEventsChart.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(this.props.selection, prevProps.selection)) {
            this.fetchTotalCount();
        }
    };
    ProjectBaseEventsChart.prototype.fetchTotalCount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, selection, onTotalValuesChange, query, projects, environments, datetime, totals, err_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection, onTotalValuesChange = _a.onTotalValuesChange, query = _a.query;
                        projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, __assign({ field: [], query: query, environment: environments, project: projects.map(function (proj) { return String(proj); }) }, getParams(datetime)))];
                    case 2:
                        totals = _b.sent();
                        onTotalValuesChange(totals);
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        onTotalValuesChange(null);
                        Sentry.captureException(err_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ProjectBaseEventsChart.prototype.render = function () {
        var _a = this.props, router = _a.router, organization = _a.organization, selection = _a.selection, api = _a.api, yAxis = _a.yAxis, query = _a.query, field = _a.field, title = _a.title, theme = _a.theme, help = _a.help, eventsChartProps = __rest(_a, ["router", "organization", "selection", "api", "yAxis", "query", "field", "title", "theme", "help"]);
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
        return getDynamicText({
            value: (<EventsChart {...eventsChartProps} router={router} organization={organization} showLegend yAxis={yAxis} query={query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} field={field} currentSeriesName={t('This Period')} previousSeriesName={t('Previous Period')} disableableSeries={[t('This Period'), t('Previous Period')]} chartHeader={<HeaderTitleLegend>
              {title}
              {help && <QuestionTooltip size="sm" position="top" title={help}/>}
            </HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{
                grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                yAxis: {
                    axisLabel: {
                        color: theme.gray200,
                        formatter: function (value) { return axisLabelFormatter(value, yAxis); },
                    },
                    scale: true,
                },
            }}/>),
            fixed: title + " Chart",
        });
    };
    return ProjectBaseEventsChart;
}(React.Component));
export default withGlobalSelection(withTheme(ProjectBaseEventsChart));
//# sourceMappingURL=projectBaseEventsChart.jsx.map