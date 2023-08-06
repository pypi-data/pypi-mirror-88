import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import DiscoverButton from 'app/components/discoverButton';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SortLink from 'app/components/gridEditable/sortLink';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import PanelTable from 'app/components/panels/panelTable';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { generateEventSlug } from 'app/utils/discover/urls';
import { getDuration } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import CellAction from 'app/views/eventsV2/table/cellAction';
import HeaderCell from 'app/views/eventsV2/table/headerCell';
import { decodeColumnOrder } from 'app/views/eventsV2/utils';
import { GridCell, GridCellNumber } from 'app/views/performance/styles';
import BaselineQuery from 'app/views/performance/transactionSummary/baselineQuery';
import { TrendsEventsDiscoverQuery } from 'app/views/performance/trends/trendsDiscoverQuery';
import { getTransactionComparisonUrl } from 'app/views/performance/utils';
var DEFAULT_TRANSACTION_LIMIT = 5;
var TransactionsList = /** @class */ (function (_super) {
    __extends(TransactionsList, _super);
    function TransactionsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCursor = function (cursor, pathname, query) {
            var _a;
            var cursorName = _this.props.cursorName;
            browserHistory.push({
                pathname: pathname,
                query: __assign(__assign({}, query), (_a = {}, _a[cursorName] = cursor, _a)),
            });
        };
        return _this;
    }
    TransactionsList.prototype.renderHeader = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, selected = _a.selected, options = _a.options, handleDropdownChange = _a.handleDropdownChange, handleOpenInDiscoverClick = _a.handleOpenInDiscoverClick;
        return (<Header>
        <DropdownControl data-test-id="filter-transactions" button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={t('Filter')} size="small">
              {selected.label}
            </StyledDropdownButton>);
        }}>
          {options.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<DropdownItem data-test-id={"option-" + value} key={value} onSelect={handleDropdownChange} eventKey={value} isActive={value === selected.value}>
              {label}
            </DropdownItem>);
        })}
        </DropdownControl>
        {!this.isTrend() && (<HeaderButtonContainer>
            <DiscoverButton onClick={handleOpenInDiscoverClick} to={eventView
            .withSorts([selected.sort])
            .getResultsViewUrlTarget(organization.slug)} size="small" data-test-id="discover-open">
              {t('Open in Discover')}
            </DiscoverButton>
          </HeaderButtonContainer>)}
      </Header>);
    };
    TransactionsList.prototype.renderTransactionTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, eventView = _b.eventView, location = _b.location, organization = _b.organization, selected = _b.selected, handleCellAction = _b.handleCellAction, cursorName = _b.cursorName, limit = _b.limit, titles = _b.titles, generateLink = _b.generateLink, baseline = _b.baseline;
        var sortedEventView = eventView.withSorts([selected.sort]);
        var columnOrder = sortedEventView.getColumns();
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        if (selected.query) {
            var query_1 = tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = stringifyQueryObject(query_1);
        }
        var baselineTransactionName = organization.features.includes('transaction-comparison')
            ? baseline !== null && baseline !== void 0 ? baseline : null : null;
        var tableRenderer = function (_a) {
            var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData, baselineData = _a.baselineData;
            return (<React.Fragment>
        <TransactionsTable eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={tableData} baselineData={baselineData !== null && baselineData !== void 0 ? baselineData : null} columnOrder={columnOrder} titles={titles} generateLink={generateLink} baselineTransactionName={baselineTransactionName} handleCellAction={handleCellAction}/>
        <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
      </React.Fragment>);
        };
        if (baselineTransactionName) {
            var orgTableRenderer_1 = tableRenderer;
            tableRenderer = function (_a) {
                var isLoading = _a.isLoading, pageLinks = _a.pageLinks, tableData = _a.tableData;
                return (<BaselineQuery eventView={eventView} orgSlug={organization.slug}>
          {function (baselineQueryProps) {
                    return orgTableRenderer_1({
                        isLoading: isLoading || baselineQueryProps.isLoading,
                        pageLinks: pageLinks,
                        tableData: tableData,
                        baselineData: baselineQueryProps.results,
                    });
                }}
        </BaselineQuery>);
            };
        }
        return (<DiscoverQuery location={location} eventView={sortedEventView} orgSlug={organization.slug} limit={limit} cursor={cursor}>
        {tableRenderer}
      </DiscoverQuery>);
    };
    TransactionsList.prototype.renderTrendsTable = function () {
        var _this = this;
        var _a;
        var _b = this.props, trendView = _b.trendView, location = _b.location, selected = _b.selected, organization = _b.organization, cursorName = _b.cursorName, generateLink = _b.generateLink;
        var sortedEventView = trendView.clone();
        sortedEventView.sorts = [selected.sort];
        sortedEventView.trendType = selected.trendType;
        if (selected.query) {
            var query_2 = tokenizeSearch(sortedEventView.query);
            selected.query.forEach(function (item) { return query_2.setTagValues(item[0], [item[1]]); });
            sortedEventView.query = stringifyQueryObject(query_2);
        }
        var cursor = decodeScalar((_a = location.query) === null || _a === void 0 ? void 0 : _a[cursorName]);
        return (<TrendsEventsDiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location} cursor={cursor} limit={5}>
        {function (_a) {
            var isLoading = _a.isLoading, trendsData = _a.trendsData, pageLinks = _a.pageLinks;
            return (<React.Fragment>
            <TransactionsTable eventView={sortedEventView} organization={organization} location={location} isLoading={isLoading} tableData={trendsData} baselineData={null} titles={['transaction', 'percentage', 'difference']} columnOrder={decodeColumnOrder([
                { field: 'transaction' },
                { field: 'trend_percentage()' },
                { field: 'trend_difference()' },
            ])} generateLink={generateLink} baselineTransactionName={null}/>
            <StyledPagination pageLinks={pageLinks} onCursor={_this.handleCursor} size="small"/>
          </React.Fragment>);
        }}
      </TrendsEventsDiscoverQuery>);
    };
    TransactionsList.prototype.isTrend = function () {
        var selected = this.props.selected;
        return selected.trendType !== undefined;
    };
    TransactionsList.prototype.render = function () {
        return (<React.Fragment>
        {this.renderHeader()}
        {this.isTrend() ? this.renderTrendsTable() : this.renderTransactionTable()}
      </React.Fragment>);
    };
    TransactionsList.defaultProps = {
        cursorName: 'transactionCursor',
        limit: DEFAULT_TRANSACTION_LIMIT,
    };
    return TransactionsList;
}(React.Component));
var TransactionsTable = /** @class */ (function (_super) {
    __extends(TransactionsTable, _super);
    function TransactionsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TransactionsTable.prototype.getTitles = function () {
        var _a = this.props, eventView = _a.eventView, titles = _a.titles;
        return titles !== null && titles !== void 0 ? titles : eventView.getFields();
    };
    TransactionsTable.prototype.renderHeader = function () {
        var _a = this.props, tableData = _a.tableData, columnOrder = _a.columnOrder, baselineTransactionName = _a.baselineTransactionName;
        var tableMeta = tableData === null || tableData === void 0 ? void 0 : tableData.meta;
        var generateSortLink = function () { return undefined; };
        var tableTitles = this.getTitles();
        var headers = tableTitles.map(function (title, index) { return (<HeaderCell column={columnOrder[index]} tableMeta={tableMeta} key={index}>
        {function (_a) {
            var align = _a.align;
            return (<HeadCellContainer>
              <SortLink align={align} title={title} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
            </HeadCellContainer>);
        }}
      </HeaderCell>); });
        if (baselineTransactionName) {
            headers.push(<HeadCellContainer key="baseline">
          <SortLink align="right" title={t('Compared to Baseline')} direction={undefined} canSort={false} generateSortLink={generateSortLink}/>
        </HeadCellContainer>);
        }
        return headers;
    };
    TransactionsTable.prototype.renderRow = function (row, rowIndex, columnOrder, tableMeta) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location, generateLink = _a.generateLink, baselineTransactionName = _a.baselineTransactionName, baselineData = _a.baselineData, handleBaselineClick = _a.handleBaselineClick, handleCellAction = _a.handleCellAction;
        var fields = eventView.getFields();
        var tableTitles = this.getTitles();
        var resultsRow = columnOrder.map(function (column, index) {
            var _a;
            var field = String(column.key);
            // TODO add a better abstraction for this in fieldRenderers.
            var fieldName = getAggregateAlias(field);
            var fieldType = tableMeta[fieldName];
            var fieldRenderer = getFieldRenderer(field, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            var target = (_a = generateLink === null || generateLink === void 0 ? void 0 : generateLink[tableTitles[index]]) === null || _a === void 0 ? void 0 : _a.call(generateLink, organization, row, location.query);
            if (target) {
                rendered = (<Link data-test-id={"view-" + fields[index]} to={target}>
            {rendered}
          </Link>);
            }
            var isNumeric = ['integer', 'number', 'duration'].includes(fieldType);
            var key = rowIndex + ":" + column.key + ":" + index;
            rendered = isNumeric ? (<GridCellNumber>{rendered}</GridCellNumber>) : (<GridCell>{rendered}</GridCell>);
            if (handleCellAction) {
                rendered = (<CellAction column={column} dataRow={row} handleCellAction={handleCellAction(column)}>
            {rendered}
          </CellAction>);
            }
            return <BodyCellContainer key={key}>{rendered}</BodyCellContainer>;
        });
        if (baselineTransactionName) {
            if (baselineData) {
                var currentTransactionDuration = Number(row['transaction.duration']) || 0;
                var duration = baselineData['transaction.duration'];
                var delta = Math.abs(currentTransactionDuration - duration);
                var relativeSpeed = currentTransactionDuration < duration
                    ? t('faster')
                    : currentTransactionDuration > duration
                        ? t('slower')
                        : '';
                var target = getTransactionComparisonUrl({
                    organization: organization,
                    baselineEventSlug: generateEventSlug(baselineData),
                    regressionEventSlug: generateEventSlug(row),
                    transaction: baselineTransactionName,
                    query: location.query,
                });
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"} style={{ textAlign: 'right' }}>
            <GridCell>
              <Link to={target} onClick={handleBaselineClick}>
                {getDuration(delta / 1000, delta < 1000 ? 0 : 2) + " " + relativeSpeed}
              </Link>
            </GridCell>
          </BodyCellContainer>);
            }
            else {
                resultsRow.push(<BodyCellContainer data-test-id="baseline-cell" key={rowIndex + "-baseline"}>
            {'\u2014'}
          </BodyCellContainer>);
            }
        }
        return resultsRow;
    };
    TransactionsTable.prototype.renderResults = function () {
        var _this = this;
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData, columnOrder = _a.columnOrder;
        var cells = [];
        if (isLoading) {
            return cells;
        }
        if (!tableData || !tableData.meta || !tableData.data) {
            return cells;
        }
        tableData.data.forEach(function (row, i) {
            // Another check to appease tsc
            if (!tableData.meta) {
                return;
            }
            cells = cells.concat(_this.renderRow(row, i, columnOrder, tableData.meta));
        });
        return cells;
    };
    TransactionsTable.prototype.render = function () {
        var _a = this.props, isLoading = _a.isLoading, tableData = _a.tableData;
        var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
        // Custom set the height so we don't have layout shift when results are loaded.
        var loader = <LoadingIndicator style={{ margin: '70px auto' }}/>;
        return (<StyledPanelTable isEmpty={!hasResults} emptyMessage={t('No transactions found')} headers={this.renderHeader()} isLoading={isLoading} disablePadding loader={loader}>
        {this.renderResults()}
      </StyledPanelTable>);
    };
    return TransactionsTable;
}(React.PureComponent));
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 0 0 ", " 0;\n"])), space(1));
var HeaderButtonContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledPanelTable = styled(PanelTable)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var HeadCellContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var BodyCellContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", " ", ";\n  ", ";\n"], ["\n  padding: ", " ", ";\n  ", ";\n"])), space(1), space(2), overflowEllipsis);
var StyledPagination = styled(Pagination)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n"], ["\n  margin: 0 0 ", " 0;\n"])), space(3));
export default TransactionsList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=transactionsList.jsx.map