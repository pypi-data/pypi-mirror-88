import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import Pagination from 'app/components/pagination';
import Tag from 'app/components/tag';
import { IconStar, IconUser } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { isFieldSortable } from 'app/utils/discover/eventView';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction, { Actions, updateQuery } from 'app/views/eventsV2/table/cellAction';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import { DisplayModes } from '../transactionSummary/charts';
import { TransactionFilterOptions, transactionSummaryRouteWithQuery, } from '../transactionSummary/utils';
import { getVitalDetailTableMehStatusFunction, getVitalDetailTablePoorStatusFunction, vitalAbbreviations, vitalNameFromLocation, VitalState, vitalStateColors, } from './utils';
var COLUMN_TITLES = ['Transaction', 'Project', 'Unique Users', 'Count'];
var getTableColumnTitle = function (index, vitalName) {
    var abbrev = vitalAbbreviations[vitalName];
    var titles = __spread(COLUMN_TITLES, [
        "p50(" + abbrev + ")",
        "p75(" + abbrev + ")",
        "p95(" + abbrev + ")",
        "Status",
    ]);
    return titles[index];
};
export function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location, organization = _a.organization;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.overview.cellaction',
                    eventName: 'Performance Views: Cell Action Clicked',
                    organization_id: parseInt(organization.id, 10),
                    action: action,
                });
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                updateQuery(searchConditions, action, column.name, value);
                ReactRouter.browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: stringifyQueryObject(searchConditions) }),
                });
            };
        };
        _this.renderBodyCellWithData = function (tableData, vitalName) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow, vitalName); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta, vitalName) {
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, getTableColumnTitle(index, vitalName));
            };
        };
        _this.renderPrependCellWithData = function (tableData, vitalName) {
            var eventView = _this.props.eventView;
            var keyTransactionColumn = eventView
                .getColumns()
                .find(function (col) { return col.name === 'key_transaction'; });
            return function (isHeader, dataRow) {
                if (!keyTransactionColumn) {
                    return [];
                }
                if (isHeader) {
                    var star = (<IconStar key="keyTransaction" color="yellow300" isSolid data-test-id="key-transaction-header"/>);
                    return [_this.renderHeadCell(tableData === null || tableData === void 0 ? void 0 : tableData.meta, keyTransactionColumn, star)];
                }
                else {
                    return [_this.renderBodyCell(tableData, keyTransactionColumn, dataRow, vitalName)];
                }
            };
        };
        _this.handleSummaryClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.navigate.summary',
                eventName: 'Performance Views: Overview view summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spread(_this.state.widths);
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    Table.prototype.renderBodyCell = function (tableData, column, dataRow, vitalName) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location, summaryConditions = _a.summaryConditions;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        if (field === getVitalDetailTablePoorStatusFunction(vitalName)) {
            if (dataRow[getAggregateAlias(field)]) {
                return (<UniqueTagCell>
            <PoorTag>{t('Poor')}</PoorTag>
          </UniqueTagCell>);
            }
            else if (dataRow[getAggregateAlias(getVitalDetailTableMehStatusFunction(vitalName))]) {
                return (<UniqueTagCell>
            <MehTag>{t('Meh')}</MehTag>
          </UniqueTagCell>);
            }
            else {
                return (<UniqueTagCell>
            <GoodTag>{t('Good')}</GoodTag>
          </UniqueTagCell>);
            }
        }
        var fieldRenderer = getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        var allowActions = [
            Actions.ADD,
            Actions.EXCLUDE,
            Actions.SHOW_GREATER_THAN,
            Actions.SHOW_LESS_THAN,
        ];
        if (field === 'count_unique(user)') {
            return (<UniqueUserCell>
          {rendered}
          <StyledUserIcon size="20"/>
        </UniqueUserCell>);
        }
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            var conditions = tokenizeSearch(summaryConditions);
            conditions.addTagValues('has', ["" + vitalName]);
            summaryView.query = stringifyQueryObject(conditions);
            var target = transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
                showTransactions: TransactionFilterOptions.RECENT,
                display: DisplayModes.VITALS,
            });
            return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
          <Link to={target} onClick={this.handleSummaryClick}>
            {rendered}
          </Link>
        </CellAction>);
        }
        if (field.startsWith('key_transaction') || field.startsWith('user_misery')) {
            return rendered;
        }
        return (<CellAction column={column} dataRow={dataRow} handleCellAction={this.handleCellAction(column)} allowActions={allowActions}>
        {rendered}
      </CellAction>);
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
        var _a = this.props, eventView = _a.eventView, location = _a.location;
        return (<HeaderCell column={column} tableMeta={tableMeta}>
        {function (_a) {
            var align = _a.align;
            var field = { field: column.name, width: column.width };
            function generateSortLink() {
                if (!tableMeta) {
                    return undefined;
                }
                var nextEventView = eventView.sortOnField(field, tableMeta);
                var queryStringObject = nextEventView.generateQueryStringObject();
                return __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { sort: queryStringObject.sort }) });
            }
            var currentSort = eventView.sortForField(field, tableMeta);
            var canSort = isFieldSortable(field, tableMeta);
            return (<SortLink align={align} title={title || field.field} direction={currentSort ? currentSort.kind : undefined} canSort={canSort} generateSortLink={generateSortLink}/>);
        }}
      </HeaderCell>);
    };
    Table.prototype.getSortedEventView = function (vitalName) {
        var eventView = this.props.eventView;
        var aggregateFieldPoor = getAggregateAlias(getVitalDetailTablePoorStatusFunction(vitalName));
        var aggregateFieldMeh = getAggregateAlias(getVitalDetailTableMehStatusFunction(vitalName));
        var isSortingByStatus = eventView.sorts.some(function (sort) {
            return sort.field.includes(aggregateFieldPoor) || sort.field.includes(aggregateFieldMeh);
        });
        var additionalSorts = isSortingByStatus
            ? []
            : [
                {
                    field: 'key_transaction',
                    kind: 'desc',
                },
                {
                    field: aggregateFieldPoor,
                    kind: 'desc',
                },
                {
                    field: aggregateFieldMeh,
                    kind: 'desc',
                },
            ];
        return eventView.withSorts(__spread(additionalSorts, eventView.sorts));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var widths = this.state.widths;
        var fakeColumnView = eventView.clone();
        fakeColumnView.fields = __spread(eventView.fields);
        var columnOrder = fakeColumnView
            .getColumns()
            // remove key_transactions from the column order as we'll be rendering it
            // via a prepended column
            .filter(function (col) { return col.name !== 'key_transaction'; })
            .slice(0, -1)
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var vitalName = vitalNameFromLocation(location);
        var sortedEventView = this.getSortedEventView(vitalName);
        var columnSortBy = sortedEventView.getSorts();
        return (<div>
        <DiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} limit={10}>
          {function (_a) {
            var pageLinks = _a.pageLinks, isLoading = _a.isLoading, tableData = _a.tableData;
            return (<React.Fragment>
              <GridEditable isLoading={isLoading} data={tableData ? tableData.data : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                onResizeColumn: _this.handleResizeColumn,
                renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta, vitalName),
                renderBodyCell: _this.renderBodyCellWithData(tableData, vitalName),
                renderPrependColumns: _this.renderPrependCellWithData(tableData, vitalName),
                prependColumnWidths: ['max-content'],
            }} location={location}/>
              <Pagination pageLinks={pageLinks}/>
            </React.Fragment>);
        }}
        </DiscoverQuery>
      </div>);
    };
    return Table;
}(React.Component));
var UniqueUserCell = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var UniqueTagCell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var GoodTag = styled(Tag)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), vitalStateColors[VitalState.GOOD], function (p) { return p.theme.white; });
var MehTag = styled(Tag)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), vitalStateColors[VitalState.MEH], function (p) { return p.theme.white; });
var PoorTag = styled(Tag)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"], ["\n  div {\n    background-color: ", ";\n  }\n  span {\n    color: ", ";\n  }\n"])), vitalStateColors[VitalState.POOR], function (p) { return p.theme.white; });
var StyledUserIcon = styled(IconUser)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme.gray400; });
export default Table;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=table.jsx.map