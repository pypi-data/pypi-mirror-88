import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import * as Sentry from '@sentry/react';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import * as qs from 'query-string';
import { fetchOrgMembers, indexMembersByProject } from 'app/actionCreators/members';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import StreamGroup from 'app/components/stream/group';
import { t } from 'app/locale';
import GroupStore from 'app/stores/groupStore';
import { callIfFunction } from 'app/utils/callIfFunction';
import StreamManager from 'app/utils/streamManager';
import withApi from 'app/utils/withApi';
import GroupListHeader from './groupListHeader';
var defaultProps = {
    canSelectGroups: true,
    withChart: true,
    withPagination: true,
};
var GroupList = /** @class */ (function (_super) {
    __extends(GroupList, _super);
    function GroupList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: false,
            groups: [],
            pageLinks: null,
        };
        _this.listener = GroupStore.listen(function () { return _this.onGroupChange(); }, undefined);
        _this._streamManager = new StreamManager(GroupStore);
        _this.fetchData = function () {
            GroupStore.loadInitialData([]);
            var _a = _this.props, api = _a.api, orgId = _a.orgId;
            _this.setState({ loading: true, error: false });
            fetchOrgMembers(api, orgId).then(function (members) {
                _this.setState({ memberList: indexMembersByProject(members) });
            });
            var endpoint = _this.getGroupListEndpoint();
            api.request(endpoint, {
                success: function (data, _, jqXHR) {
                    var _a;
                    _this._streamManager.push(data);
                    _this.setState({
                        error: false,
                        loading: false,
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: function (err) {
                    Sentry.captureException(err);
                    _this.setState({ error: true, loading: false });
                },
            });
        };
        return _this;
    }
    GroupList.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupList.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return (!isEqual(this.state, nextState) ||
            nextProps.endpointPath !== this.props.endpointPath ||
            nextProps.query !== this.props.query ||
            !isEqual(nextProps.queryParams, this.props.queryParams));
    };
    GroupList.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.orgId !== this.props.orgId ||
            prevProps.endpointPath !== this.props.endpointPath ||
            prevProps.query !== this.props.query ||
            !isEqual(prevProps.queryParams, this.props.queryParams)) {
            this.fetchData();
        }
    };
    GroupList.prototype.componentWillUnmount = function () {
        GroupStore.reset();
        callIfFunction(this.listener);
    };
    GroupList.prototype.getGroupListEndpoint = function () {
        var _a = this.props, orgId = _a.orgId, endpointPath = _a.endpointPath, queryParams = _a.queryParams;
        var path = endpointPath !== null && endpointPath !== void 0 ? endpointPath : "/organizations/" + orgId + "/issues/";
        var queryParameters = queryParams !== null && queryParams !== void 0 ? queryParams : this.getQueryParams();
        return path + "?" + qs.stringify(queryParameters);
    };
    GroupList.prototype.getQueryParams = function () {
        var query = this.props.query;
        var queryParams = this.context.location.query;
        queryParams.limit = 50;
        queryParams.sort = 'new';
        queryParams.query = query;
        return queryParams;
    };
    GroupList.prototype.handleCursorChange = function (cursor, path, query, pageDiff) {
        var queryPageInt = parseInt(query.page, 10);
        var nextPage = isNaN(queryPageInt)
            ? pageDiff
            : queryPageInt + pageDiff;
        var nextCursor = cursor;
        // unset cursor and page when we navigate back to the first page
        // also reset cursor if somehow the previous button is enabled on
        // first page and user attempts to go backwards
        if (nextPage <= 0) {
            nextCursor = undefined;
            nextPage = undefined;
        }
        browserHistory.push({
            pathname: path,
            query: __assign(__assign({}, query), { cursor: nextCursor }),
        });
    };
    GroupList.prototype.onGroupChange = function () {
        var groups = this._streamManager.getAllItems();
        if (!isEqual(groups, this.state.groups)) {
            this.setState({ groups: groups });
        }
    };
    GroupList.prototype.render = function () {
        var _a = this.props, canSelectGroups = _a.canSelectGroups, withChart = _a.withChart, renderEmptyMessage = _a.renderEmptyMessage, withPagination = _a.withPagination;
        var _b = this.state, loading = _b.loading, error = _b.error, groups = _b.groups, memberList = _b.memberList, pageLinks = _b.pageLinks;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        if (groups.length === 0) {
            if (typeof renderEmptyMessage === 'function') {
                return renderEmptyMessage();
            }
            return (<Panel>
          <PanelBody>
            <EmptyStateWarning>
              <p>{t("There don't seem to be any events fitting the query.")}</p>
            </EmptyStateWarning>
          </PanelBody>
        </Panel>);
        }
        return (<React.Fragment>
        <Panel>
          <GroupListHeader withChart={!!withChart}/>
          <PanelBody>
            {groups.map(function (_a) {
            var id = _a.id, project = _a.project;
            var members = (memberList === null || memberList === void 0 ? void 0 : memberList.hasOwnProperty(project.slug)) ? memberList[project.slug]
                : undefined;
            return (<StreamGroup key={id} id={id} canSelect={canSelectGroups} withChart={withChart} memberList={members} useFilteredStats/>);
        })}
          </PanelBody>
        </Panel>
        {withPagination && (<Pagination pageLinks={pageLinks} onCursor={this.handleCursorChange}/>)}
      </React.Fragment>);
    };
    GroupList.contextTypes = {
        location: PropTypes.object,
    };
    GroupList.defaultProps = defaultProps;
    return GroupList;
}(React.Component));
export { GroupList };
export default withApi(GroupList);
//# sourceMappingURL=groupList.jsx.map