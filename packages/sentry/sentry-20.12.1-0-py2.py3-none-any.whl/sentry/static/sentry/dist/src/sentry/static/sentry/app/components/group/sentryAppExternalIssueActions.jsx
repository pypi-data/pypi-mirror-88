import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import { deleteExternalIssue } from 'app/actionCreators/platformExternalIssues';
import { IntegrationLink } from 'app/components/issueSyncListElement';
import { SentryAppIcon } from 'app/components/sentryAppIcon';
import { IconAdd, IconClose } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { recordInteraction } from 'app/utils/recordSentryAppInteraction';
import withApi from 'app/utils/withApi';
import SentryAppExternalIssueModal from './sentryAppExternalIssueModal';
var SentryAppExternalIssueActions = /** @class */ (function (_super) {
    __extends(SentryAppExternalIssueActions, _super);
    function SentryAppExternalIssueActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            action: 'create',
            externalIssue: _this.props.externalIssue,
        };
        _this.doOpenModal = function (e) {
            // Only show the modal when we don't have a linked issue
            if (_this.state.externalIssue) {
                return;
            }
            var _a = _this.props, group = _a.group, event = _a.event, sentryAppComponent = _a.sentryAppComponent, sentryAppInstallation = _a.sentryAppInstallation;
            recordInteraction(sentryAppComponent.sentryApp.slug, 'sentry_app_component_interacted', {
                componentType: 'issue-link',
            });
            e === null || e === void 0 ? void 0 : e.preventDefault();
            openModal(function (deps) { return (<SentryAppExternalIssueModal {...deps} {...{ group: group, event: event, sentryAppComponent: sentryAppComponent, sentryAppInstallation: sentryAppInstallation }} onSubmitSuccess={_this.onSubmitSuccess}/>); });
        };
        _this.deleteIssue = function () {
            var _a = _this.props, api = _a.api, group = _a.group;
            var externalIssue = _this.state.externalIssue;
            externalIssue &&
                deleteExternalIssue(api, group.id, externalIssue.id)
                    .then(function (_data) {
                    _this.setState({ externalIssue: undefined });
                    addSuccessMessage(t('Successfully unlinked issue.'));
                })
                    .catch(function (_error) {
                    addErrorMessage(t('Unable to unlink issue.'));
                });
        };
        _this.onAddRemoveClick = function () {
            var externalIssue = _this.state.externalIssue;
            if (!externalIssue) {
                _this.doOpenModal();
            }
            else {
                _this.deleteIssue();
            }
        };
        _this.onSubmitSuccess = function (externalIssue) {
            _this.setState({ externalIssue: externalIssue });
        };
        return _this;
    }
    SentryAppExternalIssueActions.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.externalIssue !== prevProps.externalIssue) {
            this.updateExternalIssue(this.props.externalIssue);
        }
    };
    SentryAppExternalIssueActions.prototype.updateExternalIssue = function (externalIssue) {
        this.setState({ externalIssue: externalIssue });
    };
    SentryAppExternalIssueActions.prototype.render = function () {
        var sentryAppComponent = this.props.sentryAppComponent;
        var externalIssue = this.state.externalIssue;
        var name = sentryAppComponent.sentryApp.name;
        var url = '#';
        var displayName = tct('Link [name] Issue', { name: name });
        if (externalIssue) {
            url = externalIssue.webUrl;
            displayName = externalIssue.displayName;
        }
        return (<IssueLinkContainer>
        <IssueLink>
          <StyledSentryAppIcon slug={sentryAppComponent.sentryApp.slug}/>
          <IntegrationLink onClick={this.doOpenModal} href={url}>
            {displayName}
          </IntegrationLink>
        </IssueLink>
        <StyledIcon onClick={this.onAddRemoveClick}>
          {!!externalIssue ? <IconClose /> : <IconAdd />}
        </StyledIcon>
      </IssueLinkContainer>);
    };
    return SentryAppExternalIssueActions;
}(React.Component));
var StyledSentryAppIcon = styled(SentryAppIcon)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"], ["\n  color: ", ";\n  width: ", ";\n  height: ", ";\n  cursor: pointer;\n  flex-shrink: 0;\n"])), function (p) { return p.theme.textColor; }, space(3), space(3));
var IssueLink = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  min-width: 0;\n"])));
var IssueLinkContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"], ["\n  line-height: 0;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: 16px;\n"])));
var StyledIcon = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  cursor: pointer;\n"], ["\n  color: ", ";\n  cursor: pointer;\n"])), function (p) { return p.theme.textColor; });
export default withApi(SentryAppExternalIssueActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryAppExternalIssueActions.jsx.map