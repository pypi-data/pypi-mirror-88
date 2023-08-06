import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import DateTime from 'app/components/dateTime';
import Tag from 'app/components/tag';
import { t } from 'app/locale';
var GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
    REPROCESSED: 4,
};
function InboxReason(_a) {
    var inbox = _a.inbox;
    var reason = inbox.reason, reason_details = inbox.reason_details, dateAdded = inbox.date_added;
    function getReasonDetails() {
        switch (reason) {
            case GroupInboxReason.UNIGNORED:
                return {
                    tagType: 'default',
                    reasonBadgeText: t('Unignored'),
                    tooltipText: t('%(count)s events within %(window)s', {
                        count: (reason_details === null || reason_details === void 0 ? void 0 : reason_details.count) || 0,
                        window: moment.duration((reason_details === null || reason_details === void 0 ? void 0 : reason_details.window) || 0, 'minutes').humanize(),
                    }),
                };
            case GroupInboxReason.REGRESSION:
                return {
                    tagType: 'error',
                    reasonBadgeText: t('Regression'),
                    tooltipText: t('Issue was resolved'),
                };
            case GroupInboxReason.MANUAL:
                return {
                    tagType: 'highlight',
                    reasonBadgeText: t('Manual'),
                };
            case GroupInboxReason.REPROCESSED:
                return {
                    tagType: 'info',
                    reasonBadgeText: t('Reprocessed'),
                    tooltipText: t('Issue was reprocessed'),
                };
            default:
                return {
                    tagType: 'warning',
                    reasonBadgeText: t('New Issue'),
                };
        }
    }
    var _b = getReasonDetails(), tooltipText = _b.tooltipText, reasonBadgeText = _b.reasonBadgeText, tagType = _b.tagType;
    var tooltip = (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {dateAdded && (<DateWrapper>
          <DateTime date={dateAdded}/>
        </DateWrapper>)}
    </TooltipWrapper>);
    return (<Tag type={tagType} tooltipText={tooltip}>
      {reasonBadgeText}
    </Tag>);
}
export default InboxReason;
var DateWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
var TooltipWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=inboxReason.jsx.map