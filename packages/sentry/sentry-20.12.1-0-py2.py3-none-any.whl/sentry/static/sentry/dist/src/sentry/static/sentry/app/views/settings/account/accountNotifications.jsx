var _a;
import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AlertLink from 'app/components/alertLink';
import Link from 'app/components/links/link';
import { PanelFooter } from 'app/components/panels';
import accountNotificationFields from 'app/data/forms/accountNotificationSettings';
import { IconChevron, IconMail } from 'app/icons';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var FINE_TUNE_FOOTERS = (_a = {},
    _a[t('Alerts')] = {
        text: t('Fine tune alerts by project'),
        path: 'alerts/',
    },
    _a[t('Workflow Notifications')] = {
        text: t('Fine tune workflow notifications by project'),
        path: 'workflow/',
    },
    _a[t('Email Routing')] = {
        text: t('Fine tune email routing by project'),
        path: 'email/',
    },
    _a[t('Weekly Reports')] = {
        text: t('Fine tune weekly reports by organization'),
        path: 'reports/',
    },
    _a[t('Deploy Notifications')] = {
        text: t('Fine tune deploy notifications by organization'),
        path: 'deploy/',
    },
    _a);
var AccountNotifications = /** @class */ (function (_super) {
    __extends(AccountNotifications, _super);
    function AccountNotifications() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountNotifications.prototype.getEndpoints = function () {
        return [['data', '/users/me/notifications/']];
    };
    AccountNotifications.prototype.getTitle = function () {
        return 'Notifications';
    };
    AccountNotifications.prototype.renderBody = function () {
        var _a;
        return (<div>
        <SettingsPageHeader title="Notifications"/>
        <Form initialData={(_a = this.state.data) !== null && _a !== void 0 ? _a : undefined} saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/">
          <JsonForm forms={accountNotificationFields} renderFooter={function (_a) {
            var title = _a.title;
            if (typeof title !== 'string') {
                return null;
            }
            if (FINE_TUNE_FOOTERS[title]) {
                return <FineTuningFooter {...FINE_TUNE_FOOTERS[title]}/>;
            }
            return null;
        }}/>
          <AlertLink to="/settings/account/emails" icon={<IconMail />}>
            {t('Looking to add or remove an email address? Use the emails panel.')}
          </AlertLink>
        </Form>
      </div>);
    };
    return AccountNotifications;
}(AsyncView));
export default AccountNotifications;
var FineTuneLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  padding: 15px 20px;\n  color: inherit;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  padding: 15px 20px;\n  color: inherit;\n"])));
var FineTuningFooter = function (_a) {
    var path = _a.path, text = _a.text;
    return (<PanelFooter css={{ borderTop: 'none' }}>
    <FineTuneLink to={"/settings/account/notifications/" + path}>
      <span>{text}</span>
      <IconChevron direction="right" size="15px"/>
    </FineTuneLink>
  </PanelFooter>);
};
var templateObject_1;
//# sourceMappingURL=accountNotifications.jsx.map