export var TransactionFilterOptions;
(function (TransactionFilterOptions) {
    TransactionFilterOptions["FASTEST"] = "fastest";
    TransactionFilterOptions["SLOW"] = "slow";
    TransactionFilterOptions["OUTLIER"] = "outlier";
    TransactionFilterOptions["RECENT"] = "recent";
})(TransactionFilterOptions || (TransactionFilterOptions = {}));
export function generateTransactionSummaryRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/";
}
export function transactionSummaryRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query, _b = _a.unselectedSeries, unselectedSeries = _b === void 0 ? 'p100()' : _b, display = _a.display, trendDisplay = _a.trendDisplay, showTransactions = _a.showTransactions;
    var pathname = generateTransactionSummaryRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
            unselectedSeries: unselectedSeries,
            showTransactions: showTransactions,
            display: display,
            trendDisplay: trendDisplay,
        },
    };
}
//# sourceMappingURL=utils.jsx.map