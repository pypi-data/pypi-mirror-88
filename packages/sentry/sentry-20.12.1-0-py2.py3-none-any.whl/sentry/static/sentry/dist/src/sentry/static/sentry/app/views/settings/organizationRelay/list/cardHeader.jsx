import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Clipboard from 'app/components/clipboard';
import ConfirmDelete from 'app/components/confirmDelete';
import DateTime from 'app/components/dateTime';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconCopy, IconDelete, IconEdit } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
var CardHeader = function (_a) {
    var publicKey = _a.publicKey, name = _a.name, description = _a.description, created = _a.created, disabled = _a.disabled, onEdit = _a.onEdit, onDelete = _a.onDelete;
    var deleteButton = (<Button size="small" icon={<IconDelete />} label={t('Delete Key')} disabled={disabled} title={disabled ? t('You do not have permission to delete keys') : undefined}/>);
    return (<Header>
      <MainInfo>
        <Name>
          <div>{name}</div>
          {description && (<QuestionTooltip position="top" size="sm" title={description}/>)}
        </Name>
        <Date>
          {tct('Created on [date]', { date: <DateTime date={created} timeAndDate/> })}
        </Date>
      </MainInfo>
      <ButtonBar gap={1}>
        <Clipboard value={publicKey}>
          <Button size="small" icon={<IconCopy />}>
            {t('Copy Key')}
          </Button>
        </Clipboard>
        <Button size="small" onClick={onEdit(publicKey)} icon={<IconEdit />} label={t('Edit Key')} disabled={disabled} title={disabled ? t('You do not have permission to edit keys') : undefined}/>
        {disabled ? (deleteButton) : (<ConfirmDelete message={t('After removing this Public Key, your Relay will no longer be able to communicate with Sentry and events will be dropped.')} onConfirm={onDelete(publicKey)} confirmInput={name}>
            {deleteButton}
          </ConfirmDelete>)}
      </ButtonBar>
    </Header>);
};
export default CardHeader;
var Name = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n"])), space(0.5));
var MainInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  color: ", ";\n  display: grid;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.textColor; }, space(1));
var Date = styled('small')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var Header = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  align-items: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr max-content;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=cardHeader.jsx.map