import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import JsonViewer from 'app/components/events/attachmentViewers/jsonViewer';
import PanelAlert from 'app/components/panels/panelAlert';
import { tct } from 'app/locale';
var RRWebJsonViewer = /** @class */ (function (_super) {
    __extends(RRWebJsonViewer, _super);
    function RRWebJsonViewer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showRawJson: false,
        };
        return _this;
    }
    RRWebJsonViewer.prototype.render = function () {
        var _this = this;
        var showRawJson = this.state.showRawJson;
        return (<React.Fragment>
        <StyledPanelAlert border={showRawJson} type="info">
          {tct('This is an attachment containing a session replay. [replayLink:View the replay] or [jsonLink:view the raw JSON].', {
            replayLink: <a href="#context-replay"/>,
            jsonLink: (<a onClick={function () {
                return _this.setState(function (state) { return ({
                    showRawJson: !state.showRawJson,
                }); });
            }}/>),
        })}
        </StyledPanelAlert>
        {showRawJson && <JsonViewer {...this.props}/>}
      </React.Fragment>);
    };
    return RRWebJsonViewer;
}(React.Component));
export default RRWebJsonViewer;
var StyledPanelAlert = styled(PanelAlert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: 0;\n  border-bottom: ", ";\n"], ["\n  margin: 0;\n  border-bottom: ", ";\n"])), function (p) { return (p.border ? "1px solid " + p.theme.border : null); });
var templateObject_1;
//# sourceMappingURL=rrwebJsonViewer.jsx.map