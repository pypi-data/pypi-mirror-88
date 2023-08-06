import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { forceCheck } from 'react-lazyload';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import SearchBar from 'app/components/searchBar';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { ReleaseStatus } from 'app/types';
import { defined } from 'app/utils';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import ReleaseArchivedNotice from '../detail/overview/releaseArchivedNotice';
import ReleaseCard from './releaseCard';
import ReleaseDisplayOptions from './releaseDisplayOptions';
import ReleaseLanding from './releaseLanding';
import ReleaseListSortOptions from './releaseListSortOptions';
import ReleaseListStatusOptions from './releaseListStatusOptions';
import { DisplayOption, SortOption, StatusOption } from './utils';
var ReleasesList = /** @class */ (function (_super) {
    __extends(ReleasesList, _super);
    function ReleasesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleSortBy = function (sort) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, sort: sort }) }));
        };
        _this.handleDisplay = function (display) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, display: display }) }));
        };
        _this.handleStatus = function (status) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, status: status }) }));
        };
        return _this;
    }
    ReleasesList.prototype.getTitle = function () {
        return routeTitleGen(t('Releases'), this.props.organization.slug, false);
    };
    ReleasesList.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var statsPeriod = location.query.statsPeriod;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var activeDisplay = this.getDisplay();
        var query = __assign(__assign({}, pick(location.query, [
            'project',
            'environment',
            'cursor',
            'query',
            'sort',
            'healthStatsPeriod',
        ])), { summaryStatsPeriod: statsPeriod, per_page: 25, health: 1, healthStat: activeDisplay === DisplayOption.CRASH_FREE_USERS ? 'users' : 'sessions', flatten: activeSort === SortOption.DATE ? 0 : 1, status: activeStatus === StatusOption.ARCHIVED
                ? ReleaseStatus.Archived
                : ReleaseStatus.Active });
        var endpoints = [
            ['releasesWithHealth', "/organizations/" + organization.slug + "/releases/", { query: query }],
        ];
        // when sorting by date we fetch releases without health and then fetch health lazily
        if (activeSort === SortOption.DATE) {
            endpoints.push([
                'releasesWithoutHealth',
                "/organizations/" + organization.slug + "/releases/",
                { query: __assign(__assign({}, query), { health: 0 }) },
            ]);
        }
        return endpoints;
    };
    ReleasesList.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data, jqXHR = _a.jqXHR;
        var remainingRequests = this.state.remainingRequests;
        // make sure there's no withHealth/withoutHealth race condition and set proper loading state
        if (stateKey === 'releasesWithHealth' || remainingRequests === 1) {
            this.setState({
                reloading: false,
                loading: false,
                loadingHealth: stateKey === 'releasesWithoutHealth',
                releases: data,
                releasesPageLinks: jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link'),
            });
        }
    };
    ReleasesList.prototype.componentDidUpdate = function (prevProps, prevState) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
        if (prevState.releases !== this.state.releases) {
            /**
             * Manually trigger checking for elements in viewport.
             * Helpful when LazyLoad components enter the viewport without resize or scroll events,
             * https://github.com/twobin/react-lazyload#forcecheck
             *
             * HealthStatsCharts are being rendered only when they are scrolled into viewport.
             * This is how we re-check them without scrolling once releases change as this view
             * uses shouldReload=true and there is no reloading happening.
             */
            forceCheck();
        }
    };
    ReleasesList.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ReleasesList.prototype.getSort = function () {
        var sort = this.props.location.query.sort;
        switch (sort) {
            case SortOption.CRASH_FREE_USERS:
                return SortOption.CRASH_FREE_USERS;
            case SortOption.CRASH_FREE_SESSIONS:
                return SortOption.CRASH_FREE_SESSIONS;
            case SortOption.SESSIONS:
                return SortOption.SESSIONS;
            case SortOption.USERS_24_HOURS:
                return SortOption.USERS_24_HOURS;
            default:
                return SortOption.DATE;
        }
    };
    ReleasesList.prototype.getDisplay = function () {
        var display = this.props.location.query.display;
        switch (display) {
            case DisplayOption.CRASH_FREE_USERS:
                return DisplayOption.CRASH_FREE_USERS;
            default:
                return DisplayOption.CRASH_FREE_SESSIONS;
        }
    };
    ReleasesList.prototype.getStatus = function () {
        var status = this.props.location.query.status;
        switch (status) {
            case StatusOption.ARCHIVED:
                return StatusOption.ARCHIVED;
            default:
                return StatusOption.ACTIVE;
        }
    };
    ReleasesList.prototype.shouldShowLoadingIndicator = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases, reloading = _a.reloading;
        return (loading && !reloading) || (loading && !(releases === null || releases === void 0 ? void 0 : releases.length));
    };
    ReleasesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderEmptyMessage = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, selection = _a.selection;
        var statsPeriod = location.query.statsPeriod;
        var searchQuery = this.getQuery();
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        if (searchQuery && searchQuery.length) {
            return (<EmptyStateWarning small>{t('There are no releases that match') + ": '" + searchQuery + "'."}</EmptyStateWarning>);
        }
        if (activeSort === SortOption.USERS_24_HOURS) {
            return (<EmptyStateWarning small>
          {t('There are no releases with active user data (users in the last 24 hours).')}
        </EmptyStateWarning>);
        }
        if (activeSort !== SortOption.DATE) {
            var relativePeriod = getRelativeSummary(statsPeriod || DEFAULT_STATS_PERIOD).toLowerCase();
            return (<EmptyStateWarning small>
          {t('There are no releases with data in the') + " " + relativePeriod + "."}
        </EmptyStateWarning>);
        }
        if (activeStatus === StatusOption.ARCHIVED) {
            return (<EmptyStateWarning small>
          {t('There are no archived releases.')}
        </EmptyStateWarning>);
        }
        if (defined(statsPeriod) && statsPeriod !== '14d') {
            return <EmptyStateWarning small>{t('There are no releases.')}</EmptyStateWarning>;
        }
        return (<ReleaseLanding organization={organization} projectId={selection.projects.filter(function (p) { return p !== ALL_ACCESS_PROJECTS; })[0]}/>);
    };
    ReleasesList.prototype.renderInnerBody = function (activeDisplay) {
        var _a = this.props, location = _a.location, selection = _a.selection, organization = _a.organization;
        var _b = this.state, releases = _b.releases, reloading = _b.reloading, loadingHealth = _b.loadingHealth, releasesPageLinks = _b.releasesPageLinks;
        if (this.shouldShowLoadingIndicator()) {
            return <LoadingIndicator />;
        }
        if (!(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return this.renderEmptyMessage();
        }
        return (<React.Fragment>
        {releases.map(function (release) { return (<ReleaseCard key={release.version + "-" + release.projects[0].slug} activeDisplay={activeDisplay} release={release} orgSlug={organization.slug} location={location} selection={selection} reloading={reloading} showHealthPlaceholders={loadingHealth}/>); })}
        <Pagination pageLinks={releasesPageLinks}/>
      </React.Fragment>);
    };
    ReleasesList.prototype.renderBody = function () {
        var organization = this.props.organization;
        var _a = this.state, releases = _a.releases, reloading = _a.reloading;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var activeDisplay = this.getDisplay();
        return (<GlobalSelectionHeader showAbsolute={false} timeRangeHint={t('Changing this date range will recalculate the release metrics.')}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <StyledPageHeader>
              <PageHeading>{t('Releases')}</PageHeading>
              <SortAndFilterWrapper>
                <StyledSearchBar placeholder={t('Search')} onSearch={this.handleSearch} query={this.getQuery()}/>
                <ReleaseListStatusOptions selected={activeStatus} onSelect={this.handleStatus}/>
                <ReleaseListSortOptions selected={activeSort} onSelect={this.handleSortBy}/>
                <ReleaseDisplayOptions selected={activeDisplay} onSelect={this.handleDisplay}/>
              </SortAndFilterWrapper>
            </StyledPageHeader>

            {!reloading &&
            activeStatus === StatusOption.ARCHIVED &&
            !!(releases === null || releases === void 0 ? void 0 : releases.length) && <ReleaseArchivedNotice multi/>}

            {this.renderInnerBody(activeDisplay)}
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    return ReleasesList;
}(AsyncView));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    order: 4;\n  }\n"], ["\n  @media (max-width: ", ") {\n    order: 4;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var StyledPageHeader = styled(PageHeader)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr;\n  justify-content: flex-start;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr;\n  justify-content: flex-start;\n  margin-bottom: ", ";\n"])), space(2), space(3));
var SortAndFilterWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[2]; });
export default withOrganization(withGlobalSelection(ReleasesList));
export { ReleasesList };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map