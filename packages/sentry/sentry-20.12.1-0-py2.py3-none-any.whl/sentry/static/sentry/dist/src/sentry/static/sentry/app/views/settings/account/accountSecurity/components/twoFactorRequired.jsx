import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Alert from 'app/components/alert';
import ExternalLink from 'app/components/links/externalLink';
import { IconFlag } from 'app/icons';
import { tct } from 'app/locale';
import space from 'app/styles/space';
import getPendingInvite from 'app/utils/getPendingInvite';
var TwoFactorRequired = function () {
    return !getPendingInvite() ? null : (<StyledAlert data-test-id="require-2fa" type="error" icon={<IconFlag size="md"/>}>
      {tct('You have been invited to an organization that requires [link:two-factor authentication].' +
        ' Setup two-factor authentication below to join your organization.', {
        link: <ExternalLink href="https://docs.sentry.io/accounts/require-2fa/"/>,
    })}
    </StyledAlert>);
};
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(3));
export default TwoFactorRequired;
var templateObject_1;
//# sourceMappingURL=twoFactorRequired.jsx.map