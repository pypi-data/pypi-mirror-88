import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import StacktraceContent from 'app/components/events/interfaces/stacktraceContent';
import Hovercard, { Body } from 'app/components/hovercard';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var StacktracePreview = /** @class */ (function (_super) {
    __extends(StacktracePreview, _super);
    function StacktracePreview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, issueId, event_1, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (this.state.event) {
                            return [2 /*return*/];
                        }
                        _a = this.props, api = _a.api, issueId = _a.issueId;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/issues/" + issueId + "/events/latest/")];
                    case 2:
                        event_1 = _c.sent();
                        this.setState({ event: event_1, loading: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleStacktracePreviewClick = function (event) {
            event.stopPropagation();
            event.preventDefault();
        };
        return _this;
    }
    StacktracePreview.prototype.renderHovercardBody = function (stacktrace) {
        var _a;
        var _b = this.state, event = _b.event, loading = _b.loading;
        if (loading) {
            return null;
        }
        if (!stacktrace) {
            return (<NoStacktraceMessage onClick={this.handleStacktracePreviewClick}>
          {t('There is no stack trace.')}
        </NoStacktraceMessage>);
        }
        if (event) {
            return (<div onClick={this.handleStacktracePreviewClick}>
          <StacktraceContent data={stacktrace} expandFirstFrame={false} 
            // includeSystemFrames={!exception.hasSystemFrames} // (chainedException && stacktrace.frames.every(frame => !frame.inApp))
            includeSystemFrames={stacktrace.frames.every(function (frame) { return !frame.inApp; })} platform={((_a = event.platform) !== null && _a !== void 0 ? _a : 'other')} newestFirst={isStacktraceNewestFirst()} event={event} hideStacktraceLink/>
        </div>);
        }
        return null;
    };
    StacktracePreview.prototype.render = function () {
        var _a, _b, _c, _d;
        var _e = this.props, children = _e.children, organization = _e.organization, theme = _e.theme;
        var stacktrace = ((_d = (_c = (_b = (_a = this.state.event) === null || _a === void 0 ? void 0 : _a.entries.find(function (e) { return e.type === 'exception'; })) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values[0]) !== null && _d !== void 0 ? _d : {}).stacktrace;
        if (!organization.features.includes('stacktrace-hover-preview')) {
            return children;
        }
        return (<span onMouseEnter={this.fetchData}>
        <StyledHovercard body={this.renderHovercardBody(stacktrace)} hasStacktrace={!!stacktrace} position="right" tipColor={theme.background}>
          {children}
        </StyledHovercard>
      </span>);
    };
    return StacktracePreview;
}(React.Component));
var StyledHovercard = styled(Hovercard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: ", ";\n  border-color: ", ";\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow: scroll;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  width: ", ";\n  border-color: ", ";\n\n  ", " {\n    padding: 0;\n    max-height: 300px;\n    overflow: scroll;\n    border-bottom-left-radius: ", ";\n    border-bottom-right-radius: ", ";\n  }\n\n  .traceback {\n    margin-bottom: 0;\n    border: 0;\n    box-shadow: none;\n  }\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return (p.hasStacktrace ? '700px' : 'auto'); }, function (p) { return p.theme.background; }, Body, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[2]; });
var NoStacktraceMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  min-width: 250px;\n  min-height: 50px;\n"], ["\n  font-size: ", ";\n  color: ", ";\n  padding: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  min-width: 250px;\n  min-height: 50px;\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.gray400; }, space(1.5));
export default withTheme(withApi(StacktracePreview));
var templateObject_1, templateObject_2;
//# sourceMappingURL=stacktracePreview.jsx.map