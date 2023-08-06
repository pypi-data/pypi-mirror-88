import { __extends } from "tslib";
import React from 'react';
import SentryAppExternalIssueForm from 'app/components/group/sentryAppExternalIssueForm';
import NavTabs from 'app/components/navTabs';
import { t, tct } from 'app/locale';
import withApi from 'app/utils/withApi';
var SentryAppExternalIssueModal = /** @class */ (function (_super) {
    __extends(SentryAppExternalIssueModal, _super);
    function SentryAppExternalIssueModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            action: 'create',
        };
        _this.showLink = function () {
            _this.setState({ action: 'link' });
        };
        _this.showCreate = function () {
            _this.setState({ action: 'create' });
        };
        _this.onSubmitSuccess = function (externalIssue) {
            _this.props.onSubmitSuccess(externalIssue);
            _this.props.closeModal();
        };
        return _this;
    }
    SentryAppExternalIssueModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, sentryAppComponent = _a.sentryAppComponent, sentryAppInstallation = _a.sentryAppInstallation, group = _a.group;
        var action = this.state.action;
        var name = sentryAppComponent.sentryApp.name;
        var config = sentryAppComponent.schema[action];
        return (<React.Fragment>
        <Header closeButton>{tct('[name] Issue', { name: name })}</Header>
        <NavTabs underlined>
          <li className={action === 'create' ? 'active create' : 'create'}>
            <a onClick={this.showCreate}>{t('Create')}</a>
          </li>
          <li className={action === 'link' ? 'active link' : 'link'}>
            <a onClick={this.showLink}>{t('Link')}</a>
          </li>
        </NavTabs>
        <Body>
          <SentryAppExternalIssueForm group={group} sentryAppInstallation={sentryAppInstallation} appName={name} config={config} action={action} onSubmitSuccess={this.onSubmitSuccess} event={this.props.event}/>
        </Body>
      </React.Fragment>);
    };
    return SentryAppExternalIssueModal;
}(React.Component));
export default withApi(SentryAppExternalIssueModal);
//# sourceMappingURL=sentryAppExternalIssueModal.jsx.map