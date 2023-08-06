import { __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import UserAvatar from 'app/components/avatar/userAvatar';
import DateTime from 'app/components/dateTime';
import SelectField from 'app/components/forms/selectField';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var avatarStyle = {
    width: 36,
    height: 36,
    marginRight: 8,
};
var AuditLogList = function (_a) {
    var pageLinks = _a.pageLinks, entries = _a.entries, eventType = _a.eventType, eventTypes = _a.eventTypes, onEventSelect = _a.onEventSelect;
    var hasEntries = entries && entries.length > 0;
    var ipv4Length = 15;
    var options = __spread([
        { value: '', label: t('Any action'), clearableVaue: false }
    ], eventTypes.map(function (type) { return ({ label: type, value: type, clearableValue: false }); }));
    var action = (<form>
      <SelectField name="event" onChange={onEventSelect} value={eventType} style={{ width: 250 }} options={options}/>
    </form>);
    return (<div>
      <SettingsPageHeader title={t('Audit Log')} action={action}/>
      <Panel>
        <StyledPanelHeader disablePadding>
          <div>{t('Member')}</div>
          <div>{t('Action')}</div>
          <div>{t('IP')}</div>
          <div>{t('Time')}</div>
        </StyledPanelHeader>

        <PanelBody>
          {!hasEntries && <EmptyMessage>{t('No audit entries available')}</EmptyMessage>}

          {hasEntries &&
        entries.map(function (entry) { return (<StyledPanelItem alignItems="center" key={entry.id}>
                <UserInfo>
                  <div>
                    {entry.actor.email && (<UserAvatar style={avatarStyle} user={entry.actor}/>)}
                  </div>
                  <NameContainer>
                    <Name data-test-id="actor-name">
                      {entry.actor.isSuperuser
            ? t('%s (Sentry Staff)', entry.actor.name)
            : entry.actor.name}
                    </Name>
                    <Note>{entry.note}</Note>
                  </NameContainer>
                </UserInfo>
                <div>
                  <MonoDetail>{entry.event}</MonoDetail>
                </div>
                <TimestampOverflow>
                  <Tooltip title={entry.ipAddress} disabled={entry.ipAddress && entry.ipAddress.length <= ipv4Length}>
                    <MonoDetail>{entry.ipAddress}</MonoDetail>
                  </Tooltip>
                </TimestampOverflow>
                <TimestampInfo>
                  <DateTime dateOnly date={entry.dateCreated}/>
                  <DateTime timeOnly format="LT zz" date={entry.dateCreated}/>
                </TimestampInfo>
              </StyledPanelItem>); })}
        </PanelBody>
      </Panel>
      {pageLinks && <Pagination pageLinks={pageLinks}/>}
    </div>);
};
var UserInfo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  line-height: 1.2;\n  font-size: 13px;\n  flex: 1;\n"], ["\n  display: flex;\n  line-height: 1.2;\n  font-size: 13px;\n  flex: 1;\n"])));
var NameContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n"])));
var Name = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: 600;\n  font-size: 15px;\n"], ["\n  font-weight: 600;\n  font-size: 15px;\n"])));
var Note = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 13px;\n  word-break: break-word;\n"], ["\n  font-size: 13px;\n  word-break: break-word;\n"])));
var TimestampOverflow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var MonoDetail = styled('code')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledPanelHeader = styled(PanelHeader)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"])), space(2), space(2));
var StyledPanelItem = styled(PanelItem)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content 130px 150px;\n  grid-column-gap: ", ";\n  padding: ", ";\n"])), space(2), space(2));
var TimestampInfo = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeMedium; });
export default AuditLogList;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=auditLogList.jsx.map