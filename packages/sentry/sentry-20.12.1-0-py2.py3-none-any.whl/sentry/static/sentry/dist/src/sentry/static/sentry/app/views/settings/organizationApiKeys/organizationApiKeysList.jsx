import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AlertLink from 'app/components/alertLink';
import AutoSelectText from 'app/components/autoSelectText';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import LinkWithConfirmation from 'app/components/links/linkWithConfirmation';
import { PanelTable } from 'app/components/panels';
import { IconAdd, IconDelete } from 'app/icons';
import { t, tct } from 'app/locale';
import { inputStyles } from 'app/styles/input';
import recreateRoute from 'app/utils/recreateRoute';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
function OrganizationApiKeysList(_a) {
    var params = _a.params, routes = _a.routes, keys = _a.keys, busy = _a.busy, loading = _a.loading, onAddApiKey = _a.onAddApiKey, onRemove = _a.onRemove;
    var hasKeys = keys && keys.length;
    var action = (<Button priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>} busy={busy} disabled={busy} onClick={onAddApiKey}>
      {t('New API Key')}
    </Button>);
    return (<div>
      <SettingsPageHeader title={t('API Keys')} action={action}/>

      <TextBlock>
        {tct("API keys grant access to the [api:developer web API].\n          If you're looking to configure a Sentry client, you'll need a\n          client key which is available in your project settings.", {
        api: <ExternalLink href="https://docs.sentry.io/api/"/>,
    })}
      </TextBlock>

      <AlertLink to="/settings/account/api/auth-tokens/" priority="info">
        {tct('Until Sentry supports OAuth, you might want to switch to using [tokens:Auth Tokens] instead.', {
        tokens: <u />,
    })}
      </AlertLink>

      <PanelTable isLoading={loading} isEmpty={!hasKeys} emptyMessage={t('No API keys for this organization')} headers={[t('Name'), t('Key'), t('Actions')]}>
        {keys &&
        keys.map(function (_a) {
            var id = _a.id, key = _a.key, label = _a.label;
            var apiDetailsUrl = recreateRoute(id + "/", {
                params: params,
                routes: routes,
            });
            return (<React.Fragment key={key}>
                <Cell>
                  <Link to={apiDetailsUrl}>{label}</Link>
                </Cell>

                <div>
                  <AutoSelectTextInput readOnly>{key}</AutoSelectTextInput>
                </div>

                <Cell>
                  <LinkWithConfirmation aria-label={t('Remove API Key')} className="btn btn-default btn-sm" onConfirm={function () { return onRemove(id); }} message={t('Are you sure you want to remove this API key?')} title={t('Remove API Key?')}>
                    <IconDelete size="xs" css={{ position: 'relative', top: '2px' }}/>
                  </LinkWithConfirmation>
                </Cell>
              </React.Fragment>);
        })}
      </PanelTable>
    </div>);
}
var Cell = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var AutoSelectTextInput = styled(AutoSelectText)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return inputStyles(p); });
export default OrganizationApiKeysList;
var templateObject_1, templateObject_2;
//# sourceMappingURL=organizationApiKeysList.jsx.map