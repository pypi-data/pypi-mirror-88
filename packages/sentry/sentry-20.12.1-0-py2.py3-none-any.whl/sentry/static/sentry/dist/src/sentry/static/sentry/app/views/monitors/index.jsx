import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { PageContent } from 'app/styles/organization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
var Body = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  flex-direction: column;\n  flex: 1;\n"], ["\n  background-color: ", ";\n  flex-direction: column;\n  flex: 1;\n"])), function (p) { return p.theme.backgroundSecondary; });
var MonitorsContainer = function (_a) {
    var children = _a.children;
    return (<Feature features={['monitors']} renderDisabled>
    <GlobalSelectionHeader showEnvironmentSelector={false} showDateSelector={false} resetParamsOnChange={['cursor']}>
      <PageContent>
        <Body>{children}</Body>
      </PageContent>
    </GlobalSelectionHeader>
  </Feature>);
};
export default withGlobalSelection(MonitorsContainer);
export { MonitorsContainer };
var templateObject_1;
//# sourceMappingURL=index.jsx.map