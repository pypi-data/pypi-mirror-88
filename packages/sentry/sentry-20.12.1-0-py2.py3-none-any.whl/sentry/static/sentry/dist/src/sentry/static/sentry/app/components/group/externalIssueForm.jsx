import { __assign, __extends } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import { closeModal } from 'app/actionCreators/modal';
import AbstractExternalIssueForm from 'app/components/externalIssues/abstractExternalIssueForm';
import NavTabs from 'app/components/navTabs';
import { t, tct } from 'app/locale';
var MESSAGES_BY_ACTION = {
    link: t('Successfully linked issue.'),
    create: t('Successfully created issue.'),
};
var SUBMIT_LABEL_BY_ACTION = {
    link: t('Link Issue'),
    create: t('Create Issue'),
};
var ExternalIssueForm = /** @class */ (function (_super) {
    __extends(ExternalIssueForm, _super);
    function ExternalIssueForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getEndpoints = function () {
            var _a = _this.props, group = _a.group, integration = _a.integration;
            var action = _this.state.action;
            return [
                [
                    'integrationDetails',
                    "/groups/" + group.id + "/integrations/" + integration.id + "/?action=" + action,
                ],
            ];
        };
        _this.handleClick = function (action) {
            _this.setState({ action: action }, function () { return _this.reloadData(); });
        };
        _this.startTransaction = function (type) {
            var _a = _this.props, group = _a.group, integration = _a.integration;
            var action = _this.state.action;
            var transaction = Sentry.startTransaction({ name: "externalIssueForm." + type });
            transaction.setTag('issueAction', action);
            transaction.setTag('groupID', group.id);
            transaction.setTag('projectID', group.project.id);
            transaction.setTag('integrationSlug', integration.provider.slug);
            transaction.setTag('integrationType', 'firstParty');
            return transaction;
        };
        _this.handlePreSubmit = function () {
            _this.submitTransaction = _this.startTransaction('submit');
        };
        _this.onSubmitSuccess = function (_data) {
            var _a;
            var onChange = _this.props.onChange;
            var action = _this.state.action;
            onChange(function () { return addSuccessMessage(MESSAGES_BY_ACTION[action]); });
            closeModal();
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.handleSubmitError = function () {
            var _a;
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.onLoadAllEndpointsSuccess = function () {
            var _a;
            (_a = _this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.onRequestError = function () {
            var _a;
            (_a = _this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.getEndPointString = function () {
            var _a = _this.props, group = _a.group, integration = _a.integration;
            return "/groups/" + group.id + "/integrations/" + integration.id + "/";
        };
        _this.getTitle = function () {
            var integration = _this.props.integration;
            return tct('[integration] Issue', { integration: integration.provider.name });
        };
        _this.getFormProps = function () {
            var action = _this.state.action;
            return __assign(__assign({}, _this.getDefaultFormProps()), { submitLabel: SUBMIT_LABEL_BY_ACTION[action], apiEndpoint: _this.getEndPointString(), apiMethod: action === 'create' ? 'POST' : 'PUT', onPreSubmit: _this.handlePreSubmit, onSubmitError: _this.handleSubmitError, onSubmitSuccess: _this.onSubmitSuccess });
        };
        _this.renderNavTabs = function () {
            var action = _this.state.action;
            return (<NavTabs underlined>
        <li className={action === 'create' ? 'active' : ''}>
          <a onClick={function () { return _this.handleClick('create'); }}>{t('Create')}</a>
        </li>
        <li className={action === 'link' ? 'active' : ''}>
          <a onClick={function () { return _this.handleClick('link'); }}>{t('Link')}</a>
        </li>
      </NavTabs>);
        };
        return _this;
    }
    ExternalIssueForm.prototype.componentDidMount = function () {
        this.loadTransaction = this.startTransaction('load');
    };
    ExternalIssueForm.prototype.renderBody = function () {
        var integrationDetails = this.state.integrationDetails;
        var config = (integrationDetails || {})[this.getConfigName()];
        return this.renderForm(config);
    };
    return ExternalIssueForm;
}(AbstractExternalIssueForm));
export default ExternalIssueForm;
//# sourceMappingURL=externalIssueForm.jsx.map