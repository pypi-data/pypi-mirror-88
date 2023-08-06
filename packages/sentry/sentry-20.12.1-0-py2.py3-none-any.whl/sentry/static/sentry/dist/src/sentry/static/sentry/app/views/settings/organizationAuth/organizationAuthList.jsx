import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelAlert, PanelBody, PanelHeader } from 'app/components/panels';
import { CSRF_COOKIE_NAME } from 'app/constants';
import { t, tct } from 'app/locale';
import { descopeFeatureName } from 'app/utils';
import getCookie from 'app/utils/getCookie';
import withOrganization from 'app/utils/withOrganization';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import ProviderItem from './providerItem';
var providerPopularity = {
    google: 0,
    github: 1,
    okta: 2,
    'active-directory': 3,
    saml2: 4,
    onelogin: 5,
    rippling: 6,
    auth0: 7,
};
var OrganizationAuthList = function (_a) {
    var organization = _a.organization, providerList = _a.providerList, activeProvider = _a.activeProvider;
    var features = organization.features;
    // Sort provider list twice: first, by popularity,
    // and then a second time, to sort unavailable providers for the current plan to the end of the list.
    var sortedByPopularity = (providerList !== null && providerList !== void 0 ? providerList : []).sort(function (a, b) {
        if (!(a.key in providerPopularity)) {
            return -1;
        }
        if (!(b.key in providerPopularity)) {
            return 1;
        }
        if (providerPopularity[a.key] === providerPopularity[b.key]) {
            return 0;
        }
        return providerPopularity[a.key] > providerPopularity[b.key] ? 1 : -1;
    });
    var list = sortedByPopularity.sort(function (a, b) {
        var aEnabled = features.includes(descopeFeatureName(a.requiredFeature));
        var bEnabled = features.includes(descopeFeatureName(b.requiredFeature));
        if (aEnabled === bEnabled) {
            return 0;
        }
        return aEnabled ? -1 : 1;
    });
    var warn2FADisable = organization.require2FA &&
        list.some(function (_a) {
            var requiredFeature = _a.requiredFeature;
            return features.includes(descopeFeatureName(requiredFeature));
        });
    return (<div className="sso">
      <SettingsPageHeader title="Authentication"/>
      <PermissionAlert />
      <Panel>
        <PanelHeader>{t('Choose a provider')}</PanelHeader>
        <PanelBody>
          {!activeProvider && (<PanelAlert type="info">
              {tct('Get started with Single Sign-on for your organization by selecting a provider. Read more in our [link:SSO documentation].', {
        link: <ExternalLink href="https://docs.sentry.io/learn/sso/"/>,
    })}
            </PanelAlert>)}

          {warn2FADisable && (<PanelAlert type="warning">
              {t('Require 2FA will be disabled if you enable SSO.')}
            </PanelAlert>)}

          <form action={"/organizations/" + organization.slug + "/auth/configure/"} method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value={getCookie(CSRF_COOKIE_NAME) || ''}/>
            <input type="hidden" name="init" value="1"/>

            {list.map(function (provider) { return (<ProviderItem key={provider.key} provider={provider} active={!!activeProvider && provider.key === activeProvider.key}/>); })}
            {list.length === 0 && (<EmptyMessage>
                {t('No authentication providers are available.')}
              </EmptyMessage>)}
          </form>
        </PanelBody>
      </Panel>
    </div>);
};
export default withOrganization(OrganizationAuthList);
//# sourceMappingURL=organizationAuthList.jsx.map