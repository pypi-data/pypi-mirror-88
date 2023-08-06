import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { withTheme } from 'emotion-theming';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import CHART_PALETTE from 'app/constants/chartPalette';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import { getTermHelp } from '../performance/data';
import { ChartContainer } from '../performance/styles';
import ProjectBaseEventsChart from './charts/projectBaseEventsChart';
var DisplayModes;
(function (DisplayModes) {
    DisplayModes["APDEX"] = "apdex";
    DisplayModes["FAILURE_RATE"] = "failure_rate";
    DisplayModes["TPM"] = "tpm";
    DisplayModes["ERRORS"] = "errors";
    DisplayModes["TRANSACTIONS"] = "transactions";
})(DisplayModes || (DisplayModes = {}));
var DISPLAY_URL_KEY = ['display1', 'display2'];
var DEFAULT_DISPLAY_MODES = [DisplayModes.APDEX, DisplayModes.FAILURE_RATE];
var ProjectCharts = /** @class */ (function (_super) {
    __extends(ProjectCharts, _super);
    function ProjectCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.handleDisplayModeChange = function (value) {
            var _a;
            var _b = _this.props, location = _b.location, index = _b.index, organization = _b.organization;
            trackAnalyticsEvent({
                eventKey: "project_detail.change_chart" + (index + 1),
                eventName: "Project Detail: Change Chart #" + (index + 1),
                organization_id: parseInt(organization.id, 10),
                metric: value,
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), (_a = {}, _a[DISPLAY_URL_KEY[index]] = value, _a)),
            });
        };
        _this.handleTotalValuesChange = function (value) {
            _this.setState({ totalValues: value });
        };
        return _this;
    }
    Object.defineProperty(ProjectCharts.prototype, "otherActiveDisplayModes", {
        get: function () {
            var _a = this.props, location = _a.location, index = _a.index;
            return DISPLAY_URL_KEY.filter(function (_, idx) { return idx !== index; }).map(function (urlKey) {
                var _a;
                return ((_a = decodeScalar(location.query[urlKey])) !== null && _a !== void 0 ? _a : DEFAULT_DISPLAY_MODES[DISPLAY_URL_KEY.findIndex(function (value) { return value === urlKey; })]);
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayMode", {
        get: function () {
            var _a = this.props, location = _a.location, index = _a.index;
            var displayMode = decodeScalar(location.query[DISPLAY_URL_KEY[index]]) ||
                DEFAULT_DISPLAY_MODES[index];
            if (!Object.values(DisplayModes).includes(displayMode)) {
                return DEFAULT_DISPLAY_MODES[index];
            }
            return displayMode;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayModes", {
        get: function () {
            var organization = this.props.organization;
            var hasPerformance = organization.features.includes('performance-view');
            var hasDiscover = organization.features.includes('discover-basic');
            var noPerformanceTooltip = t('This view is only available with Performance Monitoring.');
            var noDiscoverTooltip = t('This view is only available with Discover.');
            return [
                {
                    value: DisplayModes.APDEX,
                    label: t('Apdex'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.APDEX) || !hasPerformance,
                    tooltip: hasPerformance
                        ? getTermHelp(organization, 'apdex')
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.FAILURE_RATE,
                    label: t('Failure Rate'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.FAILURE_RATE) ||
                        !hasPerformance,
                    tooltip: hasPerformance
                        ? getTermHelp(organization, 'failureRate')
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.TPM,
                    label: t('Transactions Per Minute'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TPM) || !hasPerformance,
                    tooltip: hasPerformance ? getTermHelp(organization, 'tpm') : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.ERRORS,
                    label: t('Daily Errors'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.ERRORS) || !hasDiscover,
                    tooltip: hasDiscover ? undefined : noDiscoverTooltip,
                },
                {
                    value: DisplayModes.TRANSACTIONS,
                    label: t('Daily Transactions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TRANSACTIONS) ||
                        !hasPerformance,
                    tooltip: hasPerformance ? undefined : noPerformanceTooltip,
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "summaryHeading", {
        get: function () {
            switch (this.displayMode) {
                case DisplayModes.ERRORS:
                    return t('Total Errors');
                case DisplayModes.APDEX:
                case DisplayModes.FAILURE_RATE:
                case DisplayModes.TPM:
                case DisplayModes.TRANSACTIONS:
                default:
                    return t('Total Transactions');
            }
        },
        enumerable: false,
        configurable: true
    });
    ProjectCharts.prototype.render = function () {
        var _a = this.props, api = _a.api, router = _a.router, organization = _a.organization, theme = _a.theme;
        var totalValues = this.state.totalValues;
        var displayMode = this.displayMode;
        return (<Panel>
        <ChartContainer>
          {displayMode === DisplayModes.APDEX && (<ProjectBaseEventsChart title={t('Apdex')} help={getTermHelp(organization, 'apdex')} query="event.type:transaction" yAxis={"apdex(" + organization.apdexThreshold + ")"} field={["apdex(" + organization.apdexThreshold + ")"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[CHART_PALETTE[0][0], theme.purple200]}/>)}
          {displayMode === DisplayModes.FAILURE_RATE && (<ProjectBaseEventsChart title={t('Failure Rate')} help={getTermHelp(organization, 'failureRate')} query="event.type:transaction" yAxis="failure_rate()" field={["failure_rate()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.red300, theme.purple200]}/>)}
          {displayMode === DisplayModes.TPM && (<ProjectBaseEventsChart title={t('Transactions Per Minute')} help={getTermHelp(organization, 'tpm')} query="event.type:transaction" yAxis="tpm()" field={["tpm()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.yellow300, theme.purple200]} disablePrevious/>)}
          {displayMode === DisplayModes.ERRORS && (<ProjectBaseEventsChart title={t('Daily Errors')} query="event.type:error" yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.purple300, theme.purple200]} showDaily/>)}
          {displayMode === DisplayModes.TRANSACTIONS && (<ProjectBaseEventsChart title={t('Daily Transactions')} query="event.type:transaction" yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.gray200, theme.purple200]} showDaily/>)}
        </ChartContainer>
        <ChartControls>
          <InlineContainer>
            <SectionHeading>{this.summaryHeading}</SectionHeading>
            <SectionValue>
              {typeof totalValues === 'number' ? totalValues.toLocaleString() : '\u2014'}
            </SectionValue>
          </InlineContainer>
          <InlineContainer>
            <OptionSelector title={t('Display')} selected={displayMode} options={this.displayModes} onChange={this.handleDisplayModeChange}/>
          </InlineContainer>
        </ChartControls>
      </Panel>);
    };
    return ProjectCharts;
}(React.Component));
export default withApi(withTheme(ProjectCharts));
//# sourceMappingURL=projectCharts.jsx.map