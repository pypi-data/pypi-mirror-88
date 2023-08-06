import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
var SetupWizard = /** @class */ (function (_super) {
    __extends(SetupWizard, _super);
    function SetupWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            finished: false,
        };
        return _this;
    }
    SetupWizard.prototype.UNSAFE_componentWillMount = function () {
        this.pollFinished();
    };
    SetupWizard.prototype.pollFinished = function () {
        var _this = this;
        return new Promise(function (resolve) {
            _this.props.api.request("/wizard/" + _this.props.hash + "/", {
                method: 'GET',
                success: function () {
                    setTimeout(function () { return _this.pollFinished(); }, 1000);
                },
                error: function () {
                    resolve();
                    _this.setState({ finished: true });
                    setTimeout(function () { return window.close(); }, 10000);
                },
            });
        });
    };
    SetupWizard.prototype.renderSuccess = function () {
        return (<div className="row">
        <h5>{t('Return to your terminal to complete your setup')}</h5>
        <h5>{t('(This window will close in 10 seconds)')}</h5>
        <button className="btn btn-default" onClick={function () { return window.close(); }}>
          Close browser tab
        </button>
      </div>);
    };
    SetupWizard.prototype.renderLoading = function () {
        return (<div className="row">
        <h5>{t('Waiting for wizard to connect')}</h5>
      </div>);
    };
    SetupWizard.prototype.render = function () {
        var finished = this.state.finished;
        return (<div className="container">
        <LoadingIndicator style={{ margin: '2em auto' }} finished={finished}>
          {finished ? this.renderSuccess() : this.renderLoading()}
        </LoadingIndicator>
      </div>);
    };
    SetupWizard.propTypes = {
        hash: PropTypes.string.isRequired,
    };
    SetupWizard.defaultProps = {
        hash: false,
    };
    return SetupWizard;
}(React.Component));
export default withApi(SetupWizard);
//# sourceMappingURL=setupWizard.jsx.map