import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EventDataSection from 'app/components/events/eventDataSection';
import RichHttpContent from 'app/components/events/interfaces/richHttpContent/richHttpContent';
import { getCurlCommand, getFullUrl } from 'app/components/events/interfaces/utils';
import ExternalLink from 'app/components/links/externalLink';
import Truncate from 'app/components/truncate';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isUrl } from 'app/utils';
var RequestInterface = /** @class */ (function (_super) {
    __extends(RequestInterface, _super);
    function RequestInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            view: 'formatted',
        };
        _this.isPartial = function () {
            // We assume we only have a partial interface is we're missing
            // an HTTP method. This means we don't have enough information
            // to reliably construct a full HTTP request.
            return !_this.props.data.method || !_this.props.data.url;
        };
        _this.toggleView = function (value) {
            _this.setState({
                view: value,
            });
        };
        return _this;
    }
    RequestInterface.prototype.render = function () {
        var _a = this.props, data = _a.data, type = _a.type;
        var view = this.state.view;
        var fullUrl = getFullUrl(data);
        if (!isUrl(fullUrl)) {
            // Check if the url passed in is a safe url to avoid XSS
            fullUrl = undefined;
        }
        var parsedUrl = null;
        if (fullUrl) {
            // use html tag to parse url, lol
            parsedUrl = document.createElement('a');
            parsedUrl.href = fullUrl;
        }
        var actions = null;
        if (!this.isPartial() && fullUrl) {
            actions = (<ButtonBar merged active={view}>
          <Button barId="formatted" size="xsmall" onClick={this.toggleView.bind(this, 'formatted')}>
            
            {t('Formatted')}
          </Button>
          <MonoButton barId="curl" size="xsmall" onClick={this.toggleView.bind(this, 'curl')}>
            curl
          </MonoButton>
        </ButtonBar>);
        }
        var title = (<Header key="title">
        <ExternalLink href={fullUrl} title={fullUrl}>
          <Path>
            <strong>{data.method || 'GET'}</strong>
            <Truncate value={parsedUrl ? parsedUrl.pathname : ''} maxLength={36} leftTrim/>
          </Path>
          {fullUrl && <StyledIconOpen size="xs"/>}
        </ExternalLink>
        <small>{parsedUrl ? parsedUrl.hostname : ''}</small>
      </Header>);
        return (<EventDataSection type={type} title={title} actions={actions} wrapTitle={false} className="request">
        {view === 'curl' ? (<pre>{getCurlCommand(data)}</pre>) : (<RichHttpContent data={data}/>)}
      </EventDataSection>);
    };
    return RequestInterface;
}(React.Component));
var MonoButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var Path = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  text-transform: none;\n  font-weight: normal;\n\n  & strong {\n    margin-right: ", ";\n  }\n"], ["\n  color: ", ";\n  text-transform: none;\n  font-weight: normal;\n\n  & strong {\n    margin-right: ", ";\n  }\n"])), function (p) { return p.theme.textColor; }, space(0.5));
var Header = styled('h3')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
// Nudge the icon down so it is centered. the `external-icon` class
// doesn't quite get it in place.
var StyledIconOpen = styled(IconOpen)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  color: ", ";\n  position: relative;\n  top: 1px;\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  color: ", ";\n  position: relative;\n  top: 1px;\n\n  &:hover {\n    color: ", ";\n  }\n"])), space(0.5), function (p) { return p.theme.gray200; }, function (p) { return p.theme.subText; });
export default RequestInterface;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=request.jsx.map