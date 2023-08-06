import React from 'react';
import Feature from 'app/components/acl/feature';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import PageHeading from 'app/components/pageHeading';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
function Dashboards(_a) {
    var organization = _a.organization, children = _a.children;
    return (<Feature features={['discover', 'discover-query']} renderDisabled requireAll={false}>
      <GlobalSelectionHeader showEnvironmentSelector={false}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <PageHeader>
              <PageHeading withMargins>{t('Dashboards')}</PageHeading>
            </PageHeader>
            {children}
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>
    </Feature>);
}
export default withOrganization(Dashboards);
//# sourceMappingURL=index.jsx.map