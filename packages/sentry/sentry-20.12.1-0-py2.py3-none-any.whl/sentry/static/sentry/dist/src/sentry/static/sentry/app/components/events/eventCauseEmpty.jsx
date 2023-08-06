import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import codesworth from 'app/../images/spot/codesworth.png';
import { promptsUpdate } from 'app/actionCreators/prompts';
import Button from 'app/components/button';
import CommitRow from 'app/components/commitRow';
import { DataSection } from 'app/components/events/styles';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { RepositoryStatus } from 'app/types';
import { trackAdhocEvent, trackAnalyticsEvent } from 'app/utils/analytics';
import getDynamicText from 'app/utils/getDynamicText';
import { snoozedDays } from 'app/utils/promptsActivity';
import withApi from 'app/utils/withApi';
var EXAMPLE_COMMITS = ['dec0de', 'de1e7e', '5ca1ed'];
var DUMMY_COMMIT = {
    id: getDynamicText({
        value: EXAMPLE_COMMITS[Math.floor(Math.random() * EXAMPLE_COMMITS.length)],
        fixed: '5ca1ed',
    }),
    author: {
        id: '',
        name: 'codesworth',
        username: '',
        email: 'codesworth@example.com',
        ip_address: '',
        lastSeen: '',
        lastLogin: '',
        isSuperuser: false,
        isAuthenticated: false,
        emails: [],
        isManaged: false,
        lastActive: '',
        isStaff: false,
        identities: [],
        isActive: true,
        has2fa: false,
        canReset2fa: false,
        authenticators: [],
        dateJoined: '',
        options: {
            theme: 'system',
            timezone: '',
            stacktraceOrder: 1,
            language: '',
            clock24Hours: false,
            avatarType: '',
        },
        flags: { newsletter_consent_prompt: false },
        hasPasswordAuth: true,
        permissions: new Set([]),
        experiments: {},
    },
    dateCreated: moment().subtract(3, 'day').format(),
    repository: {
        id: '',
        integrationId: '',
        name: '',
        externalSlug: '',
        url: '',
        provider: {
            id: 'integrations:github',
            name: 'GitHub',
        },
        dateCreated: '',
        status: RepositoryStatus.ACTIVE,
    },
    releases: [],
    message: t('This example commit broke something'),
};
var EventCauseEmpty = /** @class */ (function (_super) {
    __extends(EventCauseEmpty, _super);
    function EventCauseEmpty() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: undefined,
        };
        return _this;
    }
    EventCauseEmpty.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventCauseEmpty.prototype.componentDidUpdate = function (_prevProps, prevState) {
        var _a = this.props, project = _a.project, organization = _a.organization;
        var shouldShow = this.state.shouldShow;
        if (!prevState.shouldShow && shouldShow) {
            // send to reload only due to high event volume
            trackAdhocEvent({
                eventKey: 'event_cause.viewed',
                org_id: parseInt(organization.id, 10),
                project_id: parseInt(project.id, 10),
                platform: project.platform,
            });
        }
    };
    EventCauseEmpty.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, project, organization, data;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization;
                        return [4 /*yield*/, api.requestPromise('/promptsactivity/', {
                                query: {
                                    project_id: project.id,
                                    organization_id: organization.id,
                                    feature: 'suspect_commits',
                                },
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: this.shouldShow(data) });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventCauseEmpty.prototype.shouldShow = function (_a) {
        var data = (_a === void 0 ? { data: {} } : _a).data;
        if (data === null || data === void 0 ? void 0 : data.dismissed_ts) {
            return false;
        }
        if (data === null || data === void 0 ? void 0 : data.snoozed_ts) {
            return snoozedDays(data.snoozed_ts) > 7;
        }
        return true;
    };
    EventCauseEmpty.prototype.handleClick = function (_a) {
        var _this = this;
        var action = _a.action, eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, api = _b.api, project = _b.project, organization = _b.organization;
        var data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: 'suspect_commits',
            status: action,
        };
        promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        this.trackAnalytics({ eventKey: eventKey, eventName: eventName });
    };
    EventCauseEmpty.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, project = _b.project, organization = _b.organization;
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    };
    EventCauseEmpty.prototype.render = function () {
        var _this = this;
        var shouldShow = this.state.shouldShow;
        if (!shouldShow) {
            return null;
        }
        return (<DataSection data-test-id="loaded-event-cause-empty">
        <StyledPanel dashedBorder>
          <BoxHeader>
            <Description>
              <h3>{t('Configure Suspect Commits')}</h3>
              <p>{t('To identify which commit caused this issue')}</p>
            </Description>
            <ButtonList>
              <DocsButton size="small" priority="primary" href="https://docs.sentry.io/workflow/releases/#create-release" onClick={function () {
            return _this.trackAnalytics({
                eventKey: 'event_cause.docs_clicked',
                eventName: 'Event Cause Docs Clicked',
            });
        }}>
                {t('Read the docs')}
              </DocsButton>

              <div>
                <SnoozeButton title={t('Remind me next week')} size="small" onClick={function () {
            return _this.handleClick({
                action: 'snoozed',
                eventKey: 'event_cause.snoozed',
                eventName: 'Event Cause Snoozed',
            });
        }}>
                  {t('Snooze')}
                </SnoozeButton>
                <DismissButton title={t('Dismiss for this project')} size="small" onClick={function () {
            return _this.handleClick({
                action: 'dismissed',
                eventKey: 'event_cause.dismissed',
                eventName: 'Event Cause Dismissed',
            });
        }}>
                  {t('Dismiss')}
                </DismissButton>
              </div>
            </ButtonList>
          </BoxHeader>
          <ExampleCommitPanel>
            <CommitRow key={DUMMY_COMMIT.id} commit={DUMMY_COMMIT} customAvatar={<CustomAvatar src={codesworth}/>}/>
          </ExampleCommitPanel>
        </StyledPanel>
      </DataSection>);
    };
    return EventCauseEmpty;
}(React.Component));
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  padding-bottom: 0;\n  background: none;\n"], ["\n  padding: ", ";\n  padding-bottom: 0;\n  background: none;\n"])), space(3));
var Description = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"], ["\n  h3 {\n    font-size: 14px;\n    text-transform: uppercase;\n    margin-bottom: ", ";\n    color: ", ";\n  }\n\n  p {\n    font-size: 13px;\n    font-weight: bold;\n    color: ", ";\n    margin-bottom: ", ";\n  }\n"])), space(0.25), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; }, space(1.5));
var ButtonList = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  justify-self: end;\n  margin-bottom: 16px;\n"])), space(1));
var DocsButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.white; });
var SnoozeButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-right: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  border-right: 0;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"])));
var DismissButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"], ["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0;\n"])));
var ExampleCommitPanel = styled(Panel)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  overflow: hidden;\n  pointer-events: none;\n  position: relative;\n  padding-right: ", ";\n\n  &:after {\n    display: block;\n    content: 'Example';\n    position: absolute;\n    top: 16px;\n    right: -24px;\n    text-transform: uppercase;\n    background: #e46187;\n    padding: 4px 26px;\n    line-height: 11px;\n    font-size: 11px;\n    color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  overflow: hidden;\n  pointer-events: none;\n  position: relative;\n  padding-right: ", ";\n\n  &:after {\n    display: block;\n    content: 'Example';\n    position: absolute;\n    top: 16px;\n    right: -24px;\n    text-transform: uppercase;\n    background: #e46187;\n    padding: 4px 26px;\n    line-height: 11px;\n    font-size: 11px;\n    color: ", ";\n    transform: rotate(45deg);\n  }\n"])), space(3), function (p) { return p.theme.white; });
var CustomAvatar = styled('img')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  height: 48px;\n  padding-right: 12px;\n  margin: -6px 0px -6px -2px;\n"], ["\n  height: 48px;\n  padding-right: 12px;\n  margin: -6px 0px -6px -2px;\n"])));
var BoxHeader = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: grid;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"], ["\n  display: grid;\n  align-items: start;\n  grid-template-columns: repeat(auto-fit, minmax(256px, 1fr));\n"])));
export default withApi(EventCauseEmpty);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=eventCauseEmpty.jsx.map