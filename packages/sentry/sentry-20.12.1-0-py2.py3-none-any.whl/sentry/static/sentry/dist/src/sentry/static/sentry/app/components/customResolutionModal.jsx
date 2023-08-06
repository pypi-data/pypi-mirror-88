import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import Button from 'app/components/button';
import { SelectAsyncField } from 'app/components/forms';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import { t } from 'app/locale';
import space from 'app/styles/space';
var CustomResolutionModal = /** @class */ (function (_super) {
    __extends(CustomResolutionModal, _super);
    function CustomResolutionModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            version: '',
        };
        _this.onChange = function (value) {
            _this.setState({ version: value });
        };
        _this.onAsyncFieldResults = function (results) {
            return results.map(function (release) { return ({
                value: release.version,
                label: (<div>
          <strong>
            <Version version={release.version} anchor={false}/>
          </strong>
          <br />
          <small>
            {t('Created')} <TimeSince date={release.dateCreated}/>
          </small>
        </div>),
            }); });
        };
        return _this;
    }
    CustomResolutionModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, orgId = _a.orgId, projectId = _a.projectId, closeModal = _a.closeModal, onSelected = _a.onSelected, Header = _a.Header, Body = _a.Body, Footer = _a.Footer;
        var url = projectId
            ? "/projects/" + orgId + "/" + projectId + "/releases/"
            : "/organizations/" + orgId + "/releases/";
        var onSubmit = function (e) {
            e.preventDefault();
            onSelected({ inRelease: _this.state.version });
            closeModal();
        };
        return (<form onSubmit={onSubmit}>
        <Header>{t('Resolved In')}</Header>
        <Body>
          <SelectAsyncField deprecatedSelectControl label={t('Version')} id="version" name="version" onChange={this.onChange} placeholder={t('e.g. 1.0.4')} url={url} onResults={this.onAsyncFieldResults} onQuery={function (query) { return ({ query: query }); }}/>
        </Body>
        <Footer>
          <Button type="button" css={{ marginRight: space(1.5) }} onClick={closeModal}>
            {t('Cancel')}
          </Button>
          <Button type="submit" priority="primary">
            {t('Save Changes')}
          </Button>
        </Footer>
      </form>);
    };
    CustomResolutionModal.propTypes = {
        onSelected: PropTypes.func.isRequired,
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string,
    };
    return CustomResolutionModal;
}(React.Component));
export default CustomResolutionModal;
//# sourceMappingURL=customResolutionModal.jsx.map