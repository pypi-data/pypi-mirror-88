import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import BarChart from 'app/components/charts/barChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getSeriesSelection } from 'app/components/charts/utils';
import ErrorBoundary from 'app/components/errorBoundary';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconDelete, IconEdit, IconGrabbable, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { getAggregateArg, getMeasurementSlug } from 'app/utils/discover/fields';
import getDynamicText from 'app/utils/getDynamicText';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import { ChartContainer, HeaderTitleLegend } from '../performance/styles';
import WidgetQueries from './widgetQueries';
var WidgetCard = /** @class */ (function (_super) {
    __extends(WidgetCard, _super);
    function WidgetCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hovering: false,
        };
        return _this;
    }
    WidgetCard.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (!isEqual(nextProps.widget, this.props.widget) ||
            !isEqual(nextProps.selection, this.props.selection) ||
            nextState.hovering !== this.state.hovering) {
            return true;
        }
        return false;
    };
    WidgetCard.prototype.chartComponent = function (chartProps) {
        var widget = this.props.widget;
        switch (widget.displayType) {
            case 'bar':
                return <BarChart {...chartProps}/>;
            case 'line':
            default:
                return <LineChart {...chartProps}/>;
        }
    };
    WidgetCard.prototype.renderVisual = function () {
        var _this = this;
        var _a, _b, _c;
        var _d = this.props, location = _d.location, router = _d.router, selection = _d.selection, api = _d.api, organization = _d.organization, widget = _d.widget;
        var statsPeriod = selection.datetime.period;
        var _e = selection.datetime, start = _e.start, end = _e.end;
        var projects = selection.projects, environments = selection.environments;
        var legend = {
            right: 10,
            top: 5,
            icon: 'circle',
            itemHeight: 8,
            itemWidth: 8,
            itemGap: 12,
            align: 'left',
            type: 'plain',
            textStyle: {
                verticalAlign: 'top',
                fontSize: 11,
                fontFamily: 'Rubik',
            },
            selected: getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
        };
        var axisField = (_c = (_b = (_a = widget.queries[0]) === null || _a === void 0 ? void 0 : _a.fields) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : 'count()';
        var chartOptions = {
            grid: {
                left: '0px',
                right: '0px',
                top: '40px',
                bottom: '10px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return axisLabelFormatter(value, axisField); },
                },
            },
        };
        return (<ChartZoom router={router} period={statsPeriod} start={start} end={end} projects={projects} environments={environments}>
        {function (zoomRenderProps) {
            return (<WidgetQueries api={api} organization={organization} widget={widget} selection={selection}>
              {function (_a) {
                var results = _a.results, error = _a.error, loading = _a.loading;
                if (error) {
                    return (<ErrorPanel>
                      <IconWarning color="gray500" size="lg"/>
                    </ErrorPanel>);
                }
                var colors = results
                    ? theme.charts.getColorPalette(results.length - 2)
                    : [];
                // Create a list of series based on the order of the fields,
                var series = results
                    ? results.map(function (values, i) { return (__assign(__assign({}, values), { color: colors[i] })); })
                    : [];
                // Stack the toolbox under the legend.
                // so all series names are clickable.
                zoomRenderProps.toolBox.z = -1;
                return (<TransitionChart loading={loading} reloading={loading}>
                    <TransparentLoadingMask visible={loading}/>
                    {getDynamicText({
                    value: _this.chartComponent(__assign(__assign(__assign({}, zoomRenderProps), chartOptions), { legend: legend,
                        series: series })),
                    fixed: 'Widget Chart',
                })}
                  </TransitionChart>);
            }}
            </WidgetQueries>);
        }}
      </ChartZoom>);
    };
    WidgetCard.prototype.renderEditPanel = function () {
        if (!this.state.hovering || !this.props.isEditing) {
            return null;
        }
        var _a = this.props, onEdit = _a.onEdit, onDelete = _a.onDelete;
        return (<EditPanel>
        <IconContainer>
          <IconGrabbable color="gray500" size="lg"/>
          <IconClick onClick={function () {
            onEdit();
        }}>
            <IconEdit color="gray500" size="lg"/>
          </IconClick>
          <IconClick onClick={function () {
            onDelete();
        }}>
            <IconDelete color="gray500" size="lg"/>
          </IconClick>
        </IconContainer>
      </EditPanel>);
    };
    WidgetCard.prototype.render = function () {
        var _this = this;
        var widget = this.props.widget;
        return (<ErrorBoundary customComponent={<ErrorCard>{t('Error loading widget data')}</ErrorCard>}>
        <StyledPanel onMouseLeave={function () {
            if (_this.state.hovering) {
                _this.setState({
                    hovering: false,
                });
            }
        }} onMouseOver={function () {
            if (!_this.state.hovering) {
                _this.setState({
                    hovering: true,
                });
            }
        }}>
          <ChartContainer>
            <HeaderTitleLegend>{widget.title}</HeaderTitleLegend>
            {this.renderVisual()}
            {this.renderEditPanel()}
          </ChartContainer>
        </StyledPanel>
      </ErrorBoundary>);
    };
    return WidgetCard;
}(React.Component));
export default withApi(withOrganization(withGlobalSelection(ReactRouter.withRouter(WidgetCard))));
var ErrorCard = styled(Placeholder)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  border-radius: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.alert.error.backgroundLight; }, function (p) { return p.theme.alert.error.border; }, function (p) { return p.theme.alert.error.textLight; }, function (p) { return p.theme.borderRadius; }, space(2));
var StyledPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var EditPanel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  background-color: rgba(255, 255, 255, 0.5);\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n\n  width: 100%;\n  height: 100%;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  background-color: rgba(255, 255, 255, 0.5);\n"])));
var IconContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n\n  > * + * {\n    margin-left: 50px;\n  }\n"], ["\n  display: flex;\n\n  > * + * {\n    margin-left: 50px;\n  }\n"])));
var IconClick = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  &:hover {\n    cursor: pointer;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=widgetCard.jsx.map