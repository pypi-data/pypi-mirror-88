import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import pick from 'lodash/pick';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import EventsTable from 'app/components/eventsTable/eventsTable';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import { t } from 'app/locale';
import parseApiError from 'app/utils/parseApiError';
import withApi from 'app/utils/withApi';
var GroupEvents = /** @class */ (function (_super) {
    __extends(GroupEvents, _super);
    function GroupEvents(props) {
        var _this = _super.call(this, props) || this;
        _this.handleSearch = function (query) {
            var targetQueryParams = __assign({}, _this.props.location.query);
            targetQueryParams.query = query;
            var _a = _this.props.params, groupId = _a.groupId, orgId = _a.orgId;
            browserHistory.push({
                pathname: "/organizations/" + orgId + "/issues/" + groupId + "/events/",
                query: targetQueryParams,
            });
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            var query = __assign(__assign({}, pick(_this.props.location.query, ['cursor', 'environment'])), { limit: 50, query: _this.state.query });
            _this.props.api.request("/issues/" + _this.props.params.groupId + "/events/", {
                query: query,
                method: 'GET',
                success: function (data, _, jqXHR) {
                    var _a;
                    _this.setState({
                        eventList: data,
                        error: false,
                        loading: false,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : '',
                    });
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError(err),
                        loading: false,
                    });
                },
            });
        };
        var queryParams = _this.props.location.query;
        _this.state = {
            eventList: [],
            loading: true,
            error: false,
            pageLinks: '',
            query: queryParams.query || '',
        };
        return _this;
    }
    GroupEvents.prototype.UNSAFE_componentWillMount = function () {
        this.fetchData();
    };
    GroupEvents.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.location.search !== nextProps.location.search) {
            var queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    };
    GroupEvents.prototype.renderNoQueryResults = function () {
        return (<EmptyStateWarning>
        <p>{t('Sorry, no events match your search query.')}</p>
      </EmptyStateWarning>);
    };
    GroupEvents.prototype.renderEmpty = function () {
        return (<EmptyStateWarning>
        <p>{t("There don't seem to be any events yet.")}</p>
      </EmptyStateWarning>);
    };
    GroupEvents.prototype.renderResults = function () {
        var _a = this.props, group = _a.group, params = _a.params;
        var tagList = group.tags.filter(function (tag) { return tag.key !== 'user'; }) || [];
        return (<EventsTable tagList={tagList} events={this.state.eventList} orgId={params.orgId} projectId={group.project.slug} groupId={params.groupId}/>);
    };
    GroupEvents.prototype.renderBody = function () {
        var body;
        if (this.state.loading) {
            body = <LoadingIndicator />;
        }
        else if (this.state.error) {
            body = <LoadingError message={this.state.error} onRetry={this.fetchData}/>;
        }
        else if (this.state.eventList.length > 0) {
            body = this.renderResults();
        }
        else if (this.state.query && this.state.query !== '') {
            body = this.renderNoQueryResults();
        }
        else {
            body = this.renderEmpty();
        }
        return body;
    };
    GroupEvents.prototype.render = function () {
        return (<div>
        <div style={{ marginBottom: 20 }}>
          <SearchBar defaultQuery="" placeholder={t('search event id, message, or tags')} query={this.state.query} onSearch={this.handleSearch}/>
        </div>
        <Panel className="event-list">
          <PanelBody>{this.renderBody()}</PanelBody>
        </Panel>
        <Pagination pageLinks={this.state.pageLinks}/>
      </div>);
    };
    return GroupEvents;
}(React.Component));
export { GroupEvents };
export default withApi(GroupEvents);
//# sourceMappingURL=groupEvents.jsx.map