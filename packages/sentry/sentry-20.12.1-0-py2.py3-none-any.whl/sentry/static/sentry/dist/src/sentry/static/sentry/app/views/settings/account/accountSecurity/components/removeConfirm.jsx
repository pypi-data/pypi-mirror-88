import { __extends } from "tslib";
import React from 'react';
import Confirm from 'app/components/confirm';
import { t } from 'app/locale';
import ConfirmHeader from 'app/views/settings/account/accountSecurity/components/confirmHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var message = (<React.Fragment>
    <ConfirmHeader>{t('Do you want to remove this method?')}</ConfirmHeader>
    <TextBlock>
      {t('Removing the last authentication method will disable two-factor authentication completely.')}
    </TextBlock>
  </React.Fragment>);
var RemoveConfirm = /** @class */ (function (_super) {
    __extends(RemoveConfirm, _super);
    function RemoveConfirm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RemoveConfirm.prototype.render = function () {
        return <Confirm {...this.props} message={message}/>;
    };
    RemoveConfirm.defaultProps = Confirm.defaultProps;
    return RemoveConfirm;
}(React.Component));
export default RemoveConfirm;
//# sourceMappingURL=removeConfirm.jsx.map