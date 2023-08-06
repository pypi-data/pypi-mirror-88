import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import Tooltip from 'app/components/tooltip';
import { IconBell } from 'app/icons';
import { t } from 'app/locale';
import { getSubscriptionReason } from './utils';
function SubscribeAction(_a) {
    var _b, _c;
    var group = _a.group, onClick = _a.onClick, className = _a.className;
    var canChangeSubscriptionState = !((_c = (_b = group.subscriptionDetails) === null || _b === void 0 ? void 0 : _b.disabled) !== null && _c !== void 0 ? _c : false);
    if (!canChangeSubscriptionState) {
        return null;
    }
    var subscribedClassName = "group-subscribe " + (group.isSubscribed ? ' active' : '');
    return (<div className="btn-group">
      <Tooltip title={getSubscriptionReason(group, true)}>
        <div className={classNames(className, subscribedClassName)} title={t('Subscribe')} onClick={onClick}>
          <IconWrapper>
            <IconBell size="xs"/>
          </IconWrapper>
        </div>
      </Tooltip>
    </div>);
}
export default SubscribeAction;
var IconWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var templateObject_1;
//# sourceMappingURL=subscribeAction.jsx.map