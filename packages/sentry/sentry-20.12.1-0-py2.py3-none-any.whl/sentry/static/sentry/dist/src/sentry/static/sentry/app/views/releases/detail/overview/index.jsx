import { __assign, __awaiter, __extends, __generator, __rest } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { restoreRelease } from 'app/actionCreators/release';
import { Client } from 'app/api';
import Feature from 'app/components/acl/feature';
import TransactionsList from 'app/components/discover/transactionsList';
import { Body, Main, Side } from 'app/components/layouts/thirds';
import { t } from 'app/locale';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
import { formatVersion } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import routeTitleGen from 'app/utils/routeTitle';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import { DisplayModes } from 'app/views/performance/transactionSummary/charts';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { TrendChangeType } from 'app/views/performance/trends/types';
import { isReleaseArchived } from '../../utils';
import { ReleaseContext } from '..';
import ReleaseChart from './chart/';
import { EventType, YAxis } from './chart/releaseChartControls';
import CommitAuthorBreakdown from './commitAuthorBreakdown';
import Deploys from './deploys';
import Issues from './issues';
import OtherProjects from './otherProjects';
import ProjectReleaseDetails from './projectReleaseDetails';
import ReleaseArchivedNotice from './releaseArchivedNotice';
import ReleaseStats from './releaseStats';
import ReleaseStatsRequest from './releaseStatsRequest';
import TotalCrashFreeUsers from './totalCrashFreeUsers';
export var TransactionsListOption;
(function (TransactionsListOption) {
    TransactionsListOption["FAILURE_COUNT"] = "failure_count";
    TransactionsListOption["TPM"] = "tpm";
    TransactionsListOption["SLOW"] = "slow";
    TransactionsListOption["SLOW_LCP"] = "slow_lcp";
    TransactionsListOption["REGRESSION"] = "regression";
    TransactionsListOption["IMPROVEMENT"] = "improved";
})(TransactionsListOption || (TransactionsListOption = {}));
var ReleaseOverview = /** @class */ (function (_super) {
    __extends(ReleaseOverview, _super);
    function ReleaseOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleYAxisChange = function (yAxis) {
            var _a = _this.props, location = _a.location, router = _a.router;
            var _b = location.query, _eventType = _b.eventType, query = __rest(_b, ["eventType"]);
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, query), { yAxis: yAxis }) }));
        };
        _this.handleEventTypeChange = function (eventType) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { eventType: eventType }) }));
        };
        _this.handleRestore = function (project, successCallback) { return __awaiter(_this, void 0, void 0, function () {
            var _a, params, organization, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, params = _a.params, organization = _a.organization;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, restoreRelease(new Client(), {
                                orgSlug: organization.slug,
                                projectSlug: project.slug,
                                releaseVersion: params.release,
                            })];
                    case 2:
                        _c.sent();
                        successCallback();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTransactionsListSortChange = function (value) {
            var location = _this.props.location;
            var target = {
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            browserHistory.push(target);
        };
        return _this;
    }
    ReleaseOverview.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseOverview.prototype.getYAxis = function (hasHealthData, hasPerformance) {
        var yAxis = this.props.location.query.yAxis;
        if (typeof yAxis === 'string') {
            if (Object.values(YAxis).includes(yAxis)) {
                return yAxis;
            }
        }
        if (hasHealthData) {
            return YAxis.SESSIONS;
        }
        if (hasPerformance) {
            return YAxis.FAILED_TRANSACTIONS;
        }
        return YAxis.EVENTS;
    };
    ReleaseOverview.prototype.getEventType = function (yAxis) {
        if (yAxis === YAxis.EVENTS) {
            var eventType = this.props.location.query.eventType;
            if (typeof eventType === 'string') {
                if (Object.values(EventType).includes(eventType)) {
                    return eventType;
                }
            }
        }
        return EventType.ALL;
    };
    ReleaseOverview.prototype.getReleaseEventView = function (version, projectId, selectedSort) {
        var selection = this.props.selection;
        var environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        var baseQuery = {
            id: undefined,
            version: 2,
            name: "Release " + formatVersion(version),
            query: "event.type:transaction release:" + version,
            fields: ['transaction', 'failure_count()', 'epm()', 'p50()'],
            orderby: '-failure_count',
            range: period,
            environment: environments,
            projects: [projectId],
            start: start ? getUtcDateString(start) : undefined,
            end: end ? getUtcDateString(end) : undefined,
        };
        switch (selectedSort.value) {
            case TransactionsListOption.SLOW_LCP:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01 has:measurements.lcp", fields: ['transaction', 'failure_count()', 'epm()', 'p75(measurements.lcp)'], orderby: 'p75_measurements_lcp' }));
            case TransactionsListOption.SLOW:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " epm():>0.01" }));
            case TransactionsListOption.FAILURE_COUNT:
                return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: "event.type:transaction release:" + version + " failure_count():>0" }));
            default:
                return EventView.fromSavedQuery(baseQuery);
        }
    };
    ReleaseOverview.prototype.getReleaseTrendView = function (version, projectId, versionDate) {
        var selection = this.props.selection;
        var environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        var trendView = EventView.fromSavedQuery({
            id: undefined,
            version: 2,
            name: "Release " + formatVersion(version),
            fields: ['transaction'],
            query: 'tpm():>0.01 trend_percentage():>0%',
            range: period,
            environment: environments,
            projects: [projectId],
            start: start ? getUtcDateString(start) : undefined,
            end: end ? getUtcDateString(end) : undefined,
        });
        trendView.middle = versionDate;
        return trendView;
    };
    ReleaseOverview.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection, location = _a.location, api = _a.api, router = _a.router;
        return (<ReleaseContext.Consumer>
        {function (_a) {
            var release = _a.release, project = _a.project, deploys = _a.deploys, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
            var commitCount = release.commitCount, version = release.version;
            var hasHealthData = (project.healthData || {}).hasHealthData;
            var hasDiscover = organization.features.includes('discover-basic');
            var hasPerformance = organization.features.includes('performance-view');
            var yAxis = _this.getYAxis(hasHealthData, hasPerformance);
            var eventType = _this.getEventType(yAxis);
            var _b = getTransactionsListSort(location), selectedSort = _b.selectedSort, sortOptions = _b.sortOptions;
            var releaseEventView = _this.getReleaseEventView(version, project.id, selectedSort);
            var titles = selectedSort.value !== TransactionsListOption.SLOW_LCP
                ? [t('transaction'), t('failure_count()'), t('tpm()'), t('p50()')]
                : [t('transaction'), t('failure_count()'), t('tpm()'), t('p75(lcp)')];
            var releaseTrendView = _this.getReleaseTrendView(version, project.id, releaseMeta.released);
            var generateLink = {
                transaction: generateTransactionLink(version, project.id, selection, location.query.showTransactions),
            };
            return (<ReleaseStatsRequest api={api} organization={organization} projectSlug={project.slug} version={version} selection={selection} location={location} yAxis={yAxis} eventType={eventType} hasHealthData={hasHealthData} hasDiscover={hasDiscover} hasPerformance={hasPerformance}>
              {function (_a) {
                var crashFreeTimeBreakdown = _a.crashFreeTimeBreakdown, releaseStatsProps = __rest(_a, ["crashFreeTimeBreakdown"]);
                return (<Body>
                  <Main>
                    {isReleaseArchived(release) && (<ReleaseArchivedNotice onRestore={function () { return _this.handleRestore(project, refetchData); }}/>)}

                    {(hasDiscover || hasPerformance || hasHealthData) && (<ReleaseChart {...releaseStatsProps} releaseMeta={releaseMeta} selection={selection} yAxis={yAxis} onYAxisChange={_this.handleYAxisChange} eventType={eventType} onEventTypeChange={_this.handleEventTypeChange} router={router} organization={organization} hasHealthData={hasHealthData} location={location} api={api} version={version} hasDiscover={hasDiscover} hasPerformance={hasPerformance} platform={project.platform}/>)}
                    <Issues orgId={organization.slug} selection={selection} version={version} location={location}/>
                    <Feature features={['performance-view']}>
                      <TransactionsList location={location} organization={organization} eventView={releaseEventView} trendView={releaseTrendView} selected={selectedSort} options={sortOptions} handleDropdownChange={_this.handleTransactionsListSortChange} titles={titles} generateLink={generateLink}/>
                    </Feature>
                  </Main>
                  <Side>
                    <ReleaseStats organization={organization} release={release} project={project} location={location} selection={selection}/>
                    <ProjectReleaseDetails release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                    {commitCount > 0 && (<CommitAuthorBreakdown version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                    {releaseMeta.projects.length > 1 && (<OtherProjects projects={releaseMeta.projects.filter(function (p) { return p.slug !== project.slug; })} location={location}/>)}
                    {hasHealthData && (<TotalCrashFreeUsers crashFreeTimeBreakdown={crashFreeTimeBreakdown}/>)}
                    {deploys.length > 0 && (<Deploys version={version} orgSlug={organization.slug} deploys={deploys} projectId={project.id}/>)}
                  </Side>
                </Body>);
            }}
            </ReleaseStatsRequest>);
        }}
      </ReleaseContext.Consumer>);
    };
    return ReleaseOverview;
}(AsyncView));
function generateTransactionLink(version, projectId, selection, value) {
    return function (organization, tableRow, _query) {
        var transaction = tableRow.transaction;
        var trendTransaction = ['regression', 'improved'].includes(value);
        var environments = selection.environments, datetime = selection.datetime;
        var start = datetime.start, end = datetime.end, period = datetime.period;
        return transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transaction,
            query: {
                query: trendTransaction ? '' : "release:" + version,
                environment: environments,
                start: start ? getUtcDateString(start) : undefined,
                end: end ? getUtcDateString(end) : undefined,
                statsPeriod: period,
            },
            projectID: projectId.toString(),
            display: trendTransaction ? DisplayModes.TREND : DisplayModes.DURATION,
        });
    };
}
function getDropdownOptions() {
    return [
        {
            sort: { kind: 'desc', field: 'failure_count' },
            value: TransactionsListOption.FAILURE_COUNT,
            label: t('Failing Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'epm' },
            value: TransactionsListOption.TPM,
            label: t('Frequent Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p50' },
            value: TransactionsListOption.SLOW,
            label: t('Slow Transactions'),
        },
        {
            sort: { kind: 'desc', field: 'p75_measurements_lcp' },
            value: TransactionsListOption.SLOW_LCP,
            label: t('Slow LCP'),
        },
        {
            sort: { kind: 'desc', field: 'trend_percentage()' },
            query: [['t_test()', '<-6']],
            trendType: TrendChangeType.REGRESSION,
            value: TransactionsListOption.REGRESSION,
            label: t('Trending Regressions'),
        },
        {
            sort: { kind: 'asc', field: 'trend_percentage()' },
            query: [['t_test()', '>6']],
            trendType: TrendChangeType.IMPROVED,
            value: TransactionsListOption.IMPROVEMENT,
            label: t('Trending Improvements'),
        },
    ];
}
function getTransactionsListSort(location) {
    var sortOptions = getDropdownOptions();
    var urlParam = decodeScalar(location.query.showTransactions) || TransactionsListOption.FAILURE_COUNT;
    var selectedSort = sortOptions.find(function (opt) { return opt.value === urlParam; }) || sortOptions[0];
    return { selectedSort: selectedSort, sortOptions: sortOptions };
}
export default withApi(withGlobalSelection(withOrganization(ReleaseOverview)));
//# sourceMappingURL=index.jsx.map