import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Button from 'app/components/button';
import Hovercard from 'app/components/hovercard';
import { PanelItem } from 'app/components/panels';
import Tag from 'app/components/tag';
import { IconLock } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { descopeFeatureName } from 'app/utils';
var ProviderItem = function (_a) {
    var provider = _a.provider, active = _a.active, onConfigure = _a.onConfigure;
    var handleConfigure = function (e) {
        onConfigure === null || onConfigure === void 0 ? void 0 : onConfigure(provider.key, e);
    };
    var renderDisabledLock = function (p) { return (<LockedFeature provider={p.provider} features={p.features}/>); };
    var defaultRenderInstallButton = function (_a) {
        var hasFeature = _a.hasFeature;
        return (<Access access={['org:write']}>
      {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Button type="submit" name="provider" size="small" value={provider.key} disabled={!hasFeature || !hasAccess} onClick={handleConfigure}>
          {t('Configure')}
        </Button>);
        }}
    </Access>);
    };
    // TODO(epurkhiser): We should probably use a more explicit hook name,
    // instead of just the feature names (sso-basic, sso-saml2, etc).
    var featureKey = provider.requiredFeature;
    var hookName = featureKey
        ? "feature-disabled:" + descopeFeatureName(featureKey)
        : null;
    var featureProps = hookName ? { hookName: hookName } : {};
    return (<Feature {...featureProps} features={[featureKey].filter(function (f) { return f; })} renderDisabled={function (_a) {
        var children = _a.children, props = __rest(_a, ["children"]);
        return typeof children === 'function' &&
            // TODO(ts): the Feature component isn't correctly templatized to allow
            // for custom props in the renderDisabled function
            children(__assign(__assign({}, props), { renderDisabled: renderDisabledLock }));
    }}>
      {function (_a) {
        var hasFeature = _a.hasFeature, features = _a.features, renderDisabled = _a.renderDisabled, renderInstallButton = _a.renderInstallButton;
        return (<PanelItem alignItems="center">
          <ProviderInfo>
            <ProviderLogo className={"provider-logo " + provider.name
            .replace(/\s/g, '-')
            .toLowerCase()}/>
            <div>
              <ProviderName>{provider.name}</ProviderName>
              <ProviderDescription>
                {t('Enable your organization to sign in with %s.', provider.name)}
              </ProviderDescription>
            </div>
          </ProviderInfo>

          <FeatureBadge>
            {!hasFeature && renderDisabled({ provider: provider, features: features })}
          </FeatureBadge>

          <div>
            {active ? (<ActiveIndicator />) : ((renderInstallButton !== null && renderInstallButton !== void 0 ? renderInstallButton : defaultRenderInstallButton)({ provider: provider, hasFeature: hasFeature }))}
          </div>
        </PanelItem>);
    }}
    </Feature>);
};
export default ProviderItem;
var ProviderInfo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  flex: 1;\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), space(2));
var ProviderLogo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 36px;\n  width: 36px;\n  border-radius: 3px;\n  margin-right: 0;\n  top: auto;\n"], ["\n  height: 36px;\n  width: 36px;\n  border-radius: 3px;\n  margin-right: 0;\n  top: auto;\n"])));
var ProviderName = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var ProviderDescription = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-top: ", ";\n  font-size: 0.8em;\n"], ["\n  margin-top: ", ";\n  font-size: 0.8em;\n"])), space(0.75));
var FeatureBadge = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var ActiveIndicator = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background: ", ";\n  color: ", ";\n  padding: ", " ", ";\n  border-radius: 2px;\n  font-size: 0.8em;\n"], ["\n  background: ", ";\n  color: ", ";\n  padding: ", " ", ";\n  border-radius: 2px;\n  font-size: 0.8em;\n"])), function (p) { return p.theme.green300; }, function (p) { return p.theme.white; }, space(1), space(1.5));
ActiveIndicator.defaultProps = {
    children: t('Active'),
};
var DisabledHovercard = styled(Hovercard)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: 350px;\n"], ["\n  width: 350px;\n"])));
var LockedFeature = function (_a) {
    var provider = _a.provider, features = _a.features, className = _a.className;
    return (<DisabledHovercard containerClassName={className} body={<FeatureDisabled features={features} hideHelpToggle message={t('%s SSO is disabled.', provider.name)} featureName={t('SSO Auth')}/>}>
    <Tag icon={<IconLock />}>{t('disabled')}</Tag>
  </DisabledHovercard>);
};
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=providerItem.jsx.map