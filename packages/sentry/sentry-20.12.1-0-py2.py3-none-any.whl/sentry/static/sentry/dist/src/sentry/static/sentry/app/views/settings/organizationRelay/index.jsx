import { __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import RelayWrapper from './relayWrapper';
var OrganizationRelay = function (_a) {
    var organization = _a.organization, props = __rest(_a, ["organization"]);
    return (<Feature features={['relay']} organization={organization} renderDisabled={function () { return (<FeatureDisabled alert={PanelAlert} features={organization.features} featureName={t('Relay')}/>); }}>
    <RelayWrapper organization={organization} {...props}/>
  </Feature>);
};
export default withOrganization(OrganizationRelay);
//# sourceMappingURL=index.jsx.map