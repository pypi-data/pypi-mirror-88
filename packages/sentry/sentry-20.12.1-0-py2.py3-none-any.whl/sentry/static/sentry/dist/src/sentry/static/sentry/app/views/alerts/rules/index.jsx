import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import Pagination from 'app/components/pagination';
import { PanelTable, PanelTableHeader } from 'app/components/panels';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconArrow, IconCheckmark } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import AlertHeader from '../list/header';
import { isIssueAlert } from '../utils';
import RuleListRow from './row';
var DEFAULT_SORT = {
    asc: false,
    field: 'date_added',
};
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
var AlertRulesList = /** @class */ (function (_super) {
    __extends(AlertRulesList, _super);
    function AlertRulesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteRule = function (projectId, rule) { return __awaiter(_this, void 0, void 0, function () {
            var params, orgId, alertPath, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId;
                        alertPath = isIssueAlert(rule) ? 'rules' : 'alert-rules';
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/" + alertPath + "/" + rule.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.reloadData();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRulesList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var query = location.query;
        return [
            [
                'ruleList',
                "/organizations/" + (params && params.orgId) + "/combined-rules/",
                {
                    query: query,
                },
            ],
        ];
    };
    AlertRulesList.prototype.tryRenderEmpty = function () {
        var ruleList = this.state.ruleList;
        if (ruleList && ruleList.length > 0) {
            return null;
        }
        return (<React.Fragment>
        {<IconWrapper>
            <IconCheckmark isCircled size="48"/>
          </IconWrapper>}
        {<Title>{t('No alert rules exist for these projects.')}</Title>}
        {<Description>
            {tct('Learn more about [link:Alerts]', {
            link: <ExternalLink href={DOCS_URL}/>,
        })}
          </Description>}
      </React.Fragment>);
    };
    AlertRulesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    AlertRulesList.prototype.renderList = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, _b = _a.ruleList, ruleList = _b === void 0 ? [] : _b, ruleListPageLinks = _a.ruleListPageLinks;
        var orgId = this.props.params.orgId;
        var query = this.props.location.query;
        var allProjectsFromIncidents = new Set(flatten(ruleList === null || ruleList === void 0 ? void 0 : ruleList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var sort = __assign(__assign({}, DEFAULT_SORT), { asc: query.asc === '1' });
        return (<Layout.Body>
        <Layout.Main fullWidth>
          <StyledPanelTable headers={[
            t('Type'),
            t('Alert Name'),
            t('Project'),
            t('Created By'),
            // eslint-disable-next-line react/jsx-key
            <StyledSortLink to={{
                pathname: "/organizations/" + orgId + "/alerts/rules/",
                query: __assign(__assign({}, query), { asc: sort.asc ? undefined : '1' }),
            }}>
                {t('Created')}{' '}
                <IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>
              </StyledSortLink>,
            t('Actions'),
        ]} isLoading={loading} isEmpty={(ruleList === null || ruleList === void 0 ? void 0 : ruleList.length) === 0} emptyMessage={this.tryRenderEmpty()}>
            <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {function (_a) {
            var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
            return ruleList.map(function (rule) { return (<RuleListRow 
            // Metric and issue alerts can have the same id
            key={(isIssueAlert(rule) ? 'metric' : 'issue') + "-" + rule.id} projectsLoaded={initiallyLoaded} projects={projects} rule={rule} orgId={orgId} onDelete={_this.handleDeleteRule}/>); });
        }}
            </Projects>
          </StyledPanelTable>
          <Pagination pageLinks={ruleListPageLinks}/>
        </Layout.Main>
      </Layout.Body>);
    };
    AlertRulesList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<SentryDocumentTitle title={t('Alerts')} objSlug={orgId}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false}>
          <AlertHeader organization={organization} router={router} activeTab="rules"/>
          {this.renderList()}
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return AlertRulesList;
}(AsyncComponent));
var AlertRulesListContainer = /** @class */ (function (_super) {
    __extends(AlertRulesListContainer, _super);
    function AlertRulesListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertRulesListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    AlertRulesListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.sort) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.sort)) {
            this.trackView();
        }
    };
    AlertRulesListContainer.prototype.trackView = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        trackAnalyticsEvent({
            eventKey: 'alert_rules.viewed',
            eventName: 'Alert Rules: Viewed',
            organization_id: organization.id,
            sort: location.query.sort,
        });
    };
    AlertRulesListContainer.prototype.render = function () {
        return <AlertRulesList {...this.props}/>;
    };
    return AlertRulesListContainer;
}(React.Component));
export default AlertRulesListContainer;
var StyledSortLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"], ["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"])));
var StyledPanelTable = styled(PanelTable)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", " {\n    line-height: normal;\n  }\n  font-size: ", ";\n  grid-template-columns: auto 1.5fr 1fr 1fr 1fr auto;\n  margin-bottom: 0;\n  white-space: nowrap;\n  ", "\n"], ["\n  ", " {\n    line-height: normal;\n  }\n  font-size: ", ";\n  grid-template-columns: auto 1.5fr 1fr 1fr 1fr auto;\n  margin-bottom: 0;\n  white-space: nowrap;\n  ",
    "\n"])), PanelTableHeader, function (p) { return p.theme.fontSizeMedium; }, function (p) {
    return p.emptyMessage &&
        "svg:not([data-test-id='icon-check-mark']) {\n    display: none;";
});
var IconWrapper = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  display: block;\n"], ["\n  color: ", ";\n  display: block;\n"])), function (p) { return p.theme.gray200; });
var Title = styled('strong')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var Description = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  display: block;\n  margin: 0;\n"], ["\n  font-size: ", ";\n  display: block;\n  margin: 0;\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map