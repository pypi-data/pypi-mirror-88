import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import uniq from 'lodash/uniq';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import Checkbox from 'app/components/checkbox';
import QueryCount from 'app/components/queryCount';
import ToolbarHeader from 'app/components/toolbarHeader';
import { t, tct, tn } from 'app/locale';
import GroupStore from 'app/stores/groupStore';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import ActionSet from './actionSet';
import { BULK_LIMIT, BULK_LIMIT_STR, ConfirmAction } from './utils';
var IssueListActions = /** @class */ (function (_super) {
    __extends(IssueListActions, _super);
    function IssueListActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            datePickerActive: false,
            anySelected: false,
            multiSelected: false,
            pageSelected: false,
            allInQuerySelected: false,
            selectedIds: new Set(),
        };
        _this.listener = SelectedGroupStore.listen(function () { return _this.handleSelectedGroupChange(); }, undefined);
        _this.handleApplyToAll = function () {
            _this.setState({ allInQuerySelected: true });
        };
        _this.handleUpdate = function (data) {
            var _a = _this.props, selection = _a.selection, api = _a.api, orgId = _a.orgSlug, query = _a.query;
            _this.actionSelectedGroups(function (itemIds) {
                addLoadingMessage(t('Saving changes\u2026'));
                // If `itemIds` is undefined then it means we expect to bulk update all items
                // that match the query.
                //
                // We need to always respect the projects selected in the global selection header:
                // * users with no global views requires a project to be specified
                // * users with global views need to be explicit about what projects the query will run against
                var projectConstraints = { project: selection.projects };
                api.bulkUpdate(__assign(__assign({ orgId: orgId,
                    itemIds: itemIds,
                    data: data,
                    query: query, environment: selection.environments }, projectConstraints), selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleDelete = function () {
            var _a = _this.props, selection = _a.selection, api = _a.api, orgId = _a.orgSlug, query = _a.query;
            addLoadingMessage(t('Removing events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                api.bulkDelete(__assign({ orgId: orgId,
                    itemIds: itemIds,
                    query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleMerge = function () {
            var _a = _this.props, selection = _a.selection, api = _a.api, orgId = _a.orgSlug, query = _a.query;
            addLoadingMessage(t('Merging events\u2026'));
            _this.actionSelectedGroups(function (itemIds) {
                api.merge(__assign({ orgId: orgId,
                    itemIds: itemIds,
                    query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                    complete: function () {
                        clearIndicators();
                    },
                });
            });
        };
        _this.handleRealtimeChange = function () {
            _this.props.onRealtimeChange(!_this.props.realtimeActive);
        };
        _this.shouldConfirm = function (action) {
            var selectedItems = SelectedGroupStore.getSelectedIds();
            switch (action) {
                case ConfirmAction.RESOLVE:
                case ConfirmAction.UNRESOLVE:
                case ConfirmAction.IGNORE:
                case ConfirmAction.UNBOOKMARK: {
                    var pageSelected = _this.state.pageSelected;
                    return pageSelected && selectedItems.size > 1;
                }
                case ConfirmAction.ACKNOWLEDGE:
                case ConfirmAction.BOOKMARK:
                    return selectedItems.size > 1;
                case ConfirmAction.MERGE:
                case ConfirmAction.DELETE:
                default:
                    return true; // By default, should confirm ...
            }
        };
        return _this;
    }
    IssueListActions.prototype.componentDidMount = function () {
        this.handleSelectedGroupChange();
    };
    IssueListActions.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    IssueListActions.prototype.actionSelectedGroups = function (callback) {
        var selectedIds;
        if (this.state.allInQuerySelected) {
            selectedIds = undefined; // undefined means "all"
        }
        else {
            var itemIdSet_1 = SelectedGroupStore.getSelectedIds();
            selectedIds = this.props.groupIds.filter(function (itemId) { return itemIdSet_1.has(itemId); });
        }
        callback(selectedIds);
        this.deselectAll();
    };
    IssueListActions.prototype.deselectAll = function () {
        SelectedGroupStore.deselectAll();
        this.setState({ allInQuerySelected: false });
    };
    // Handler for when `SelectedGroupStore` changes
    IssueListActions.prototype.handleSelectedGroupChange = function () {
        var selected = SelectedGroupStore.getSelectedIds();
        var projects = __spread(selected).map(function (id) { return GroupStore.get(id); })
            .filter(function (group) { return !!(group && group.project); })
            .map(function (group) { return group.project.slug; });
        var uniqProjects = uniq(projects);
        // we only want selectedProjectSlug set if there is 1 project
        // more or fewer should result in a null so that the action toolbar
        // can behave correctly.
        var selectedProjectSlug = uniqProjects.length === 1 ? uniqProjects[0] : undefined;
        this.setState({
            pageSelected: SelectedGroupStore.allSelected(),
            multiSelected: SelectedGroupStore.multiSelected(),
            anySelected: SelectedGroupStore.anySelected(),
            allInQuerySelected: false,
            selectedIds: SelectedGroupStore.getSelectedIds(),
            selectedProjectSlug: selectedProjectSlug,
        });
    };
    IssueListActions.prototype.handleSelectStatsPeriod = function (period) {
        return this.props.onSelectStatsPeriod(period);
    };
    IssueListActions.prototype.handleSelectAll = function () {
        SelectedGroupStore.toggleSelectAll();
    };
    IssueListActions.prototype.renderHeaders = function () {
        var _a = this.props, selection = _a.selection, statsPeriod = _a.statsPeriod, pageCount = _a.pageCount, queryCount = _a.queryCount, queryMaxCount = _a.queryMaxCount, hasInbox = _a.hasInbox;
        return (<React.Fragment>
        {hasInbox && (<React.Fragment>
            <ActionSetPlaceholder>
              
              {tct('Select [count] of [total]', {
            count: <React.Fragment>{pageCount}</React.Fragment>,
            total: (<QueryCount hideParens hideIfEmpty={false} count={queryCount || 0} max={queryMaxCount || 1}/>),
        })}
            </ActionSetPlaceholder>
          </React.Fragment>)}
        <GraphHeaderWrapper className="hidden-xs hidden-sm">
          <GraphHeader>
            <StyledToolbarHeader>{t('Graph:')}</StyledToolbarHeader>
            <GraphToggle active={statsPeriod === '24h'} onClick={this.handleSelectStatsPeriod.bind(this, '24h')}>
              {t('24h')}
            </GraphToggle>
            <GraphToggle active={statsPeriod === 'auto'} onClick={this.handleSelectStatsPeriod.bind(this, 'auto')}>
              {selection.datetime.period || t('Custom')}
            </GraphToggle>
          </GraphHeader>
        </GraphHeaderWrapper>
        <React.Fragment>
          <EventsOrUsersLabel>{t('Events')}</EventsOrUsersLabel>
          <EventsOrUsersLabel>{t('Users')}</EventsOrUsersLabel>
        </React.Fragment>
        <AssigneesLabel className="hidden-xs hidden-sm">
          <IssueToolbarHeader>{t('Assignee')}</IssueToolbarHeader>
        </AssigneesLabel>
        {hasInbox && (<ActionsLabel>
            <IssueToolbarHeader>{t('Actions')}</IssueToolbarHeader>
          </ActionsLabel>)}
      </React.Fragment>);
    };
    IssueListActions.prototype.render = function () {
        var _a = this.props, allResultsVisible = _a.allResultsVisible, queryCount = _a.queryCount, hasInbox = _a.hasInbox, orgSlug = _a.orgSlug, query = _a.query, realtimeActive = _a.realtimeActive;
        var _b = this.state, allInQuerySelected = _b.allInQuerySelected, anySelected = _b.anySelected, pageSelected = _b.pageSelected, issues = _b.selectedIds, multiSelected = _b.multiSelected, selectedProjectSlug = _b.selectedProjectSlug;
        var numIssues = issues.size;
        return (<Sticky>
        <StyledFlex>
          <ActionsCheckbox>
            <Checkbox onChange={this.handleSelectAll} checked={pageSelected}/>
          </ActionsCheckbox>
          {(anySelected || !hasInbox) && (<ActionSet orgSlug={orgSlug} queryCount={queryCount} query={query} realtimeActive={realtimeActive} hasInbox={hasInbox} issues={issues} allInQuerySelected={allInQuerySelected} anySelected={anySelected} multiSelected={multiSelected} selectedProjectSlug={selectedProjectSlug} onShouldConfirm={this.shouldConfirm} onDelete={this.handleDelete} onRealtimeChange={this.handleRealtimeChange} onMerge={this.handleMerge} onUpdate={this.handleUpdate}/>)}
          {(!anySelected || !hasInbox) && this.renderHeaders()}
        </StyledFlex>
        {!allResultsVisible && pageSelected && (<SelectAllNotice>
            {allInQuerySelected ? (queryCount >= BULK_LIMIT ? (tct('Selected up to the first [count] issues that match this search query.', {
            count: BULK_LIMIT_STR,
        })) : (tct('Selected all [count] issues that match this search query.', {
            count: queryCount,
        }))) : (<React.Fragment>
                {tn('%s issue on this page selected.', '%s issues on this page selected.', numIssues)}
                <SelectAllLink onClick={this.handleApplyToAll}>
                  {queryCount >= BULK_LIMIT
            ? tct('Select the first [count] issues that match this search query.', {
                count: BULK_LIMIT_STR,
            })
            : tct('Select all [count] issues that match this search query.', {
                count: queryCount,
            })}
                </SelectAllLink>
              </React.Fragment>)}
          </SelectAllNotice>)}
      </Sticky>);
    };
    return IssueListActions;
}(React.Component));
var IssueToolbarHeader = styled(ToolbarHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  animation: 0.3s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"], ["\n  animation: 0.3s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"])));
var Sticky = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"], ["\n  position: sticky;\n  z-index: ", ";\n  top: -1px;\n"])), function (p) { return p.theme.zIndex.header; });
var StyledFlex = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  box-sizing: border-box;\n  min-height: 45px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  margin-bottom: -1px;\n"], ["\n  display: flex;\n  box-sizing: border-box;\n  min-height: 45px;\n  padding-top: ", ";\n  padding-bottom: ", ";\n  align-items: center;\n  background: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n  margin-bottom: -1px;\n"])), space(1), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var ActionsCheckbox = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-left: ", ";\n  margin-bottom: 1px;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  padding-left: ", ";\n  margin-bottom: 1px;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])), space(2));
var ActionSetPlaceholder = styled(IssueToolbarHeader)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  @media (min-width: 800px) {\n    width: 66.66666666666666%;\n  }\n  @media (min-width: 992px) {\n    width: 50%;\n  }\n\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  overflow: hidden;\n  min-width: 0;\n  white-space: nowrap;\n"], ["\n  @media (min-width: 800px) {\n    width: 66.66666666666666%;\n  }\n  @media (min-width: 992px) {\n    width: 50%;\n  }\n\n  flex: 1;\n  margin-left: ", ";\n  margin-right: ", ";\n  overflow: hidden;\n  min-width: 0;\n  white-space: nowrap;\n"])), space(1), space(1));
var GraphHeaderWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"], ["\n  width: 160px;\n  margin-left: ", ";\n  margin-right: ", ";\n  animation: 0.25s FadeIn linear forwards;\n\n  @keyframes FadeIn {\n    0% {\n      opacity: 0;\n    }\n    100% {\n      opacity: 1;\n    }\n  }\n"])), space(2), space(2));
var GraphHeader = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledToolbarHeader = styled(IssueToolbarHeader)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var GraphToggle = styled('a')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  font-size: 13px;\n  padding-left: 8px;\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"], ["\n  font-size: 13px;\n  padding-left: 8px;\n\n  &,\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n"])), function (p) { return (p.active ? p.theme.textColor : p.theme.disabled); });
var EventsOrUsersLabel = styled(IssueToolbarHeader)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: inline-grid;\n  align-items: center;\n  justify-content: flex-end;\n  text-align: right;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space(2), theme.breakpoints[3]);
var AssigneesLabel = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"], ["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin-left: ", ";\n  margin-right: ", ";\n"])), space(2), space(2));
var ActionsLabel = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin: 0 ", ";\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  justify-content: flex-end;\n  text-align: right;\n  width: 80px;\n  margin: 0 ", ";\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; });
var SelectAllNotice = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"], ["\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  border-bottom: 1px solid ", ";\n  font-size: ", ";\n  text-align: center;\n  padding: ", " ", ";\n"])), function (p) { return p.theme.yellow100; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5), space(1.5));
var SelectAllLink = styled('a')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
export { IssueListActions };
export default withApi(IssueListActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14;
//# sourceMappingURL=index.jsx.map