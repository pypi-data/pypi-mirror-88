import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ansicolor from 'ansicolor';
import AsyncComponent from 'app/components/asyncComponent';
import PreviewPanelItem from 'app/components/events/attachmentViewers/previewPanelItem';
import { getAttachmentUrl, } from 'app/components/events/attachmentViewers/utils';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
var COLORS = {
    black: theme.black,
    white: theme.white,
    redDim: theme.red200,
    red: theme.red300,
    greenDim: theme.green200,
    green: theme.green300,
    yellowDim: theme.yellow300,
    yellow: theme.orange300,
    blueDim: theme.blue200,
    blue: theme.blue300,
    magentaDim: theme.pink200,
    magenta: theme.pink300,
    cyanDim: theme.blue200,
    cyan: theme.blue300,
};
var LogFileViewer = /** @class */ (function (_super) {
    __extends(LogFileViewer, _super);
    function LogFileViewer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LogFileViewer.prototype.getEndpoints = function () {
        return [['attachmentText', getAttachmentUrl(this.props)]];
    };
    LogFileViewer.prototype.renderBody = function () {
        var attachmentText = this.state.attachmentText;
        if (!attachmentText) {
            return null;
        }
        var spans = ansicolor
            .parse(attachmentText)
            .spans.map(function (_a, idx) {
            var color = _a.color, bgColor = _a.bgColor, text = _a.text;
            var style = {};
            if (color) {
                if (color.name) {
                    style.color =
                        COLORS[color.name + (color.dim ? 'Dim' : '')] || COLORS[color.name] || '';
                }
                if (color.bright) {
                    style.fontWeight = 500;
                }
            }
            if (bgColor && bgColor.name) {
                style.background =
                    COLORS[bgColor.name + (bgColor.dim ? 'Dim' : '')] ||
                        COLORS[bgColor.name] ||
                        '';
            }
            return (<span style={style} key={idx}>
            {text}
          </span>);
        });
        return (<PreviewPanelItem>
        <CodeWrapper>{spans}</CodeWrapper>
      </PreviewPanelItem>);
    };
    return LogFileViewer;
}(AsyncComponent));
export default LogFileViewer;
var CodeWrapper = styled('pre')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  width: 100%;\n  margin-bottom: 0;\n  &:after {\n    content: '';\n  }\n"], ["\n  padding: ", " ", ";\n  width: 100%;\n  margin-bottom: 0;\n  &:after {\n    content: '';\n  }\n"])), space(1), space(2));
var templateObject_1;
//# sourceMappingURL=logFileViewer.jsx.map