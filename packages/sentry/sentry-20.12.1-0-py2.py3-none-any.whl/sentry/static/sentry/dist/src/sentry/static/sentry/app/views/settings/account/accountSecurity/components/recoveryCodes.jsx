import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Clipboard from 'app/components/clipboard';
import Confirm from 'app/components/confirm';
import { Panel, PanelAlert, PanelBody, PanelHeader, PanelItem, } from 'app/components/panels';
import { IconCopy, IconDownload, IconPrint } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var RecoveryCodes = function (_a) {
    var className = _a.className, isEnrolled = _a.isEnrolled, codes = _a.codes, onRegenerateBackupCodes = _a.onRegenerateBackupCodes;
    var printCodes = function () {
        // eslint-disable-next-line dot-notation
        var iframe = window.frames['printable'];
        iframe.document.write(codes.join('<br>'));
        iframe.print();
        iframe.document.close();
    };
    if (!isEnrolled || !codes) {
        return null;
    }
    var formattedCodes = codes.join(' \n');
    return (<CodeContainer className={className}>
      <PanelHeader hasButtons>
        {t('Unused Codes')}

        <Actions>
          <Clipboard hideUnsupported value={formattedCodes}>
            <Button size="small" label={t('copy')}>
              <IconCopy />
            </Button>
          </Clipboard>
          <Button size="small" onClick={printCodes} label={t('print')}>
            <IconPrint />
          </Button>
          <Button size="small" download="sentry-recovery-codes.txt" href={"data:text/plain;charset=utf-8," + formattedCodes} label={t('download')}>
            <IconDownload />
          </Button>
          <Confirm onConfirm={onRegenerateBackupCodes} message={t('Are you sure you want to regenerate recovery codes? Your old codes will no longer work.')}>
            <Button priority="danger" size="small">
              {t('Regenerate Codes')}
            </Button>
          </Confirm>
        </Actions>
      </PanelHeader>
      <PanelBody>
        <PanelAlert type="warning">
          {t('Make sure to save a copy of your recovery codes and store them in a safe place.')}
        </PanelAlert>
        <div>{!!codes.length && codes.map(function (code) { return <Code key={code}>{code}</Code>; })}</div>
        {!codes.length && (<EmptyMessage>{t('You have no more recovery codes to use')}</EmptyMessage>)}
      </PanelBody>
      <iframe name="printable" css={{ display: 'none' }}/>
    </CodeContainer>);
};
export default RecoveryCodes;
var CodeContainer = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(4));
var Actions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space(1));
var Code = styled(PanelItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-family: ", ";\n  padding: ", ";\n"], ["\n  font-family: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.text.familyMono; }, space(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=recoveryCodes.jsx.map