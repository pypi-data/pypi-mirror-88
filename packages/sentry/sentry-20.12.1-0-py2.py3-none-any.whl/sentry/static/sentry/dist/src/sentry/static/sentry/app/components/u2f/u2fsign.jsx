import { __extends, __rest } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import U2fInterface from './u2finterface';
var MESSAGES = {
    signin: t('Insert your U2F device or tap the button on it to confirm the sign-in request.'),
    sudo: t('Alternatively you can use your U2F device to confirm the action.'),
    enroll: t('To enroll your U2F device insert it now or tap the button on it to activate it.'),
};
var U2fSign = /** @class */ (function (_super) {
    __extends(U2fSign, _super);
    function U2fSign() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    U2fSign.prototype.render = function () {
        var _a = this.props, displayMode = _a.displayMode, props = __rest(_a, ["displayMode"]);
        var flowMode = displayMode === 'enroll' ? 'enroll' : 'sign';
        return (<U2fInterface {...props} silentIfUnsupported={displayMode === 'sudo'} flowMode={flowMode}>
        <p>{MESSAGES[displayMode] || null}</p>
      </U2fInterface>);
    };
    U2fSign.propTypes = {
        challengeData: PropTypes.object,
        displayMode: PropTypes.string,
    };
    U2fSign.defaultProps = {
        displayMode: 'signin',
    };
    return U2fSign;
}(React.Component));
export default U2fSign;
//# sourceMappingURL=u2fsign.jsx.map