import { __extends } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import PropTypes from 'prop-types';
import u2f from 'u2f-api';
import { t, tct } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
var U2fInterface = /** @class */ (function (_super) {
    __extends(U2fInterface, _super);
    function U2fInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSupported: null,
            formElement: null,
            challengeElement: null,
            hasBeenTapped: false,
            deviceFailure: null,
            responseElement: null,
        };
        _this.onTryAgain = function () {
            _this.setState({
                hasBeenTapped: false,
                deviceFailure: null,
            }, function () {
                _this.invokeU2fFlow();
            });
        };
        _this.invokeU2fFlow = function () {
            var promise;
            if (_this.props.flowMode === 'sign') {
                promise = u2f.sign(_this.props.challengeData.authenticateRequests);
            }
            else if (_this.props.flowMode === 'enroll') {
                var _a = _this.props.challengeData, registerRequests = _a.registerRequests, authenticateRequests = _a.authenticateRequests;
                promise = u2f.register(registerRequests, authenticateRequests);
            }
            else {
                throw new Error("Unsupported flow mode '" + _this.props.flowMode + "'");
            }
            promise
                .then(function (data) {
                _this.setState({
                    hasBeenTapped: true,
                }, function () {
                    var u2fResponse = JSON.stringify(data);
                    var challenge = JSON.stringify(_this.props.challengeData);
                    if (_this.state.responseElement) {
                        // eslint-disable-next-line react/no-direct-mutation-state
                        _this.state.responseElement.value = u2fResponse;
                    }
                    if (!_this.props.onTap) {
                        _this.state.formElement && _this.state.formElement.submit();
                    }
                    else {
                        _this.props
                            .onTap({
                            response: u2fResponse,
                            challenge: challenge,
                        })
                            .catch(function () {
                            // This is kind of gross but I want to limit the amount of changes to this component
                            _this.setState({
                                deviceFailure: 'UNKNOWN_ERROR',
                                hasBeenTapped: false,
                            });
                        });
                    }
                });
            })
                .catch(function (err) {
                var failure = 'DEVICE_ERROR';
                // in some rare cases there is no metadata on the error which
                // causes this to blow up badly.
                if (err.metaData) {
                    if (err.metaData.type === 'DEVICE_INELIGIBLE') {
                        if (_this.props.flowMode === 'enroll') {
                            failure = 'DUPLICATE_DEVICE';
                        }
                        else {
                            failure = 'UNKNOWN_DEVICE';
                        }
                    }
                    else if (err.metaData.type === 'BAD_REQUEST') {
                        failure = 'BAD_APPID';
                    }
                }
                // we want to know what is happening here.  There are some indicators
                // that users are getting errors that should not happen through the
                // regular u2f flow.
                Sentry.captureException(err);
                _this.setState({
                    deviceFailure: failure,
                    hasBeenTapped: false,
                });
            });
        };
        _this.bindChallengeElement = function (ref) {
            _this.setState({
                challengeElement: ref,
                formElement: ref && ref.form,
            });
            if (ref) {
                ref.value = JSON.stringify(_this.props.challengeData);
            }
        };
        _this.bindResponseElement = function (ref) {
            _this.setState({
                responseElement: ref,
            });
        };
        _this.renderUnsupported = function () {
            if (_this.props.silentIfUnsupported) {
                return null;
            }
            return (<div className="u2f-box">
        <div className="inner">
          <p className="error">
            {t("\n             Unfortunately your browser does not support U2F. You need to use\n             a different two-factor method or switch to a browser that supports\n             it (Google Chrome or Microsoft Edge).")}
          </p>
        </div>
      </div>);
        };
        _this.canTryAgain = function () { return _this.state.deviceFailure !== 'BAD_APPID'; };
        _this.renderFailure = function () {
            var deviceFailure = _this.state.deviceFailure;
            var supportMail = ConfigStore.get('supportEmail');
            var support = supportMail ? (<a href={'mailto:' + supportMail}>{supportMail}</a>) : (<span>{t('Support')}</span>);
            return (<div className="failure-message">
        <div>
          <strong>{t('Error: ')}</strong>{' '}
          {{
                UNKNOWN_ERROR: t('There was an unknown problem, please try again'),
                DEVICE_ERROR: t('Your U2F device reported an error.'),
                DUPLICATE_DEVICE: t('This device is already in use.'),
                UNKNOWN_DEVICE: t('The device you used for sign-in is unknown.'),
                BAD_APPID: tct('[p1:The Sentry server administrator modified the ' +
                    'device registrations.]' +
                    '[p2:You need to remove and re-add the device to continue ' +
                    'using your U2F device. Use a different sign-in method or ' +
                    'contact [support] for assistance.]', {
                    p1: <p />,
                    p2: <p />,
                    support: support,
                }),
            }[deviceFailure || '']}
        </div>
        {_this.canTryAgain() && (<div style={{ marginTop: 18 }}>
            <a onClick={_this.onTryAgain} className="btn btn-primary">
              {t('Try Again')}
            </a>
          </div>)}
      </div>);
        };
        _this.renderBody = function () {
            if (_this.state.deviceFailure) {
                return _this.renderFailure();
            }
            else {
                return _this.props.children;
            }
        };
        _this.renderPrompt = function () {
            var style = _this.props.style;
            return (<div style={style} className={'u2f-box' +
                (_this.state.hasBeenTapped ? ' tapped' : '') +
                (_this.state.deviceFailure ? ' device-failure' : '')}>
        <div className="device-animation-frame">
          <div className="device-failed"/>
          <div className="device-animation"/>
          <div className="loading-dots">
            <span className="dot"/>
            <span className="dot"/>
            <span className="dot"/>
          </div>
        </div>
        <input type="hidden" name="challenge" ref={_this.bindChallengeElement}/>
        <input type="hidden" name="response" ref={_this.bindResponseElement}/>
        <div className="inner">{_this.renderBody()}</div>
      </div>);
        };
        return _this;
    }
    U2fInterface.prototype.componentDidMount = function () {
        var _this = this;
        u2f.isSupported().then(function (supported) {
            _this.setState({
                isSupported: supported,
            });
            if (!supported) {
                return;
            }
            _this.invokeU2fFlow();
        });
    };
    U2fInterface.prototype.render = function () {
        var isSupported = this.state.isSupported;
        // if we are still waiting for the browser to tell us if we can do u2f
        // this will be null.
        if (isSupported === null) {
            return null;
        }
        else if (!isSupported) {
            return this.renderUnsupported();
        }
        else {
            return this.renderPrompt();
        }
    };
    U2fInterface.propTypes = {
        challengeData: PropTypes.object.isRequired,
        flowMode: PropTypes.string.isRequired,
        onTap: PropTypes.func,
        silentIfUnsupported: PropTypes.bool,
    };
    U2fInterface.defaultProps = {
        silentIfUnsupported: false,
    };
    return U2fInterface;
}(React.Component));
export default U2fInterface;
//# sourceMappingURL=u2finterface.jsx.map