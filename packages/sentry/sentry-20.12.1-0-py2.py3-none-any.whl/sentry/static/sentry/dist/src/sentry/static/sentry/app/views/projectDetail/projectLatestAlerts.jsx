import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import AsyncComponent from 'app/components/asyncComponent';
import { SectionHeading } from 'app/components/charts/styles';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import TimeSince from 'app/components/timeSince';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { IncidentStatus } from '../alerts/types';
import MissingAlertsButtons from './missingFeatureButtons/missingAlertsButtons';
var ProjectLatestAlerts = /** @class */ (function (_super) {
    __extends(ProjectLatestAlerts, _super);
    function ProjectLatestAlerts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderAlertRow = function (alert) {
            var _a = _this.props, organization = _a.organization, theme = _a.theme;
            var isResolved = alert.status === IncidentStatus.CLOSED;
            var isWarning = alert.status === IncidentStatus.WARNING;
            var color = isResolved ? theme.gray200 : isWarning ? theme.yellow300 : theme.red300;
            var Icon = isResolved ? IconCheckmark : isWarning ? IconWarning : IconFire;
            return (<AlertRowLink to={"/organizations/" + organization.slug + "/alerts/" + alert.identifier + "/"} key={alert.id}>
        <AlertBadge color={color} icon={Icon}>
          <AlertIconWrapper>
            <Icon color="white"/>
          </AlertIconWrapper>
        </AlertBadge>
        <AlertDetails>
          <AlertTitle>{alert.title}</AlertTitle>
          <AlertDate color={color}>
            {isResolved
                ? tct('Resolved [date]', { date: <TimeSince date={alert.dateClosed}/> })
                : tct('Triggered [date]', { date: <TimeSince date={alert.dateStarted}/> })}
          </AlertDate>
        </AlertDetails>
      </AlertRowLink>);
        };
        return _this;
    }
    ProjectLatestAlerts.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (this.state !== nextState ||
            !isEqual(pick(this.props.location.query, Object.values(URL_PARAM)), pick(nextProps.location.query, Object.values(URL_PARAM)))) {
            return true;
        }
        return false;
    };
    ProjectLatestAlerts.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var query = __assign(__assign({}, pick(location.query, Object.values(URL_PARAM))), { per_page: 3 });
        // we are listing 3 alerts total, first unresolved and then we fill with resolved
        return [
            [
                'unresolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: __assign(__assign({}, query), { status: 'open' }) },
            ],
            [
                'resolvedAlerts',
                "/organizations/" + organization.slug + "/incidents/",
                { query: __assign(__assign({}, query), { status: 'closed' }) },
            ],
        ];
    };
    /**
     * If our alerts are empty, determine if we've configured alert rules (empty message differs then)
     */
    ProjectLatestAlerts.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, unresolvedAlerts, resolvedAlerts, _b, location, organization, alertRules;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.state, unresolvedAlerts = _a.unresolvedAlerts, resolvedAlerts = _a.resolvedAlerts;
                        _b = this.props, location = _b.location, organization = _b.organization;
                        if (__spread((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []), (resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : [])).length !== 0) {
                            this.setState({ hasAlertRule: true });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/alert-rules/", {
                                method: 'GET',
                                query: __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM)))), { per_page: 1 }),
                            })];
                    case 1:
                        alertRules = _c.sent();
                        this.setState({ hasAlertRule: alertRules.length > 0, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectLatestAlerts.prototype.renderInnerBody = function () {
        var _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug;
        var _b = this.state, loading = _b.loading, unresolvedAlerts = _b.unresolvedAlerts, resolvedAlerts = _b.resolvedAlerts, hasAlertRule = _b.hasAlertRule;
        var alertsUnresolvedAndResolved = __spread((unresolvedAlerts !== null && unresolvedAlerts !== void 0 ? unresolvedAlerts : []), (resolvedAlerts !== null && resolvedAlerts !== void 0 ? resolvedAlerts : []));
        var checkingForAlertRules = alertsUnresolvedAndResolved.length === 0 && hasAlertRule === undefined;
        var showLoadingIndicator = loading || checkingForAlertRules;
        if (showLoadingIndicator) {
            return <Placeholder height="160px"/>;
        }
        if (!hasAlertRule) {
            return (<MissingAlertsButtons organization={organization} projectSlug={projectSlug}/>);
        }
        if (alertsUnresolvedAndResolved.length === 0) {
            return t('No alert triggered so far.');
        }
        return alertsUnresolvedAndResolved.slice(0, 3).map(this.renderAlertRow);
    };
    ProjectLatestAlerts.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectLatestAlerts.prototype.renderBody = function () {
        return (<Section>
        <SectionHeading>{t('Latest Alerts')}</SectionHeading>
        <div>{this.renderInnerBody()}</div>
      </Section>);
    };
    return ProjectLatestAlerts;
}(AsyncComponent));
var Section = styled('section')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var AlertRowLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  height: 40px;\n  margin-bottom: ", ";\n  margin-left: ", ";\n  &,\n  &:hover,\n  &:focus {\n    color: inherit;\n  }\n  &:first-child {\n    margin-top: ", ";\n  }\n"])), space(3), space(0.5), space(1));
var AlertBadge = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n\n  &:before {\n    content: '';\n    width: 30px;\n    height: 30px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.color; });
var AlertIconWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n"], ["\n  position: absolute;\n"])));
var AlertDetails = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  ", "\n"], ["\n  margin-left: ", ";\n  ", "\n"])), space(2), overflowEllipsis);
var AlertTitle = styled('h5')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  margin-bottom: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  margin-bottom: ", ";\n  overflow: hidden;\n  text-overflow: ellipsis;\n"])), function (p) { return p.theme.fontSizeLarge; }, space(0.25));
var AlertDate = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.color; });
export default withTheme(ProjectLatestAlerts);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=projectLatestAlerts.jsx.map