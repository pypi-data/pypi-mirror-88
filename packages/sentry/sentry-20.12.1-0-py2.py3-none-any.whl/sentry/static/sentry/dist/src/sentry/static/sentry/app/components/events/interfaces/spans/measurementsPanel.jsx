import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { defined } from 'app/utils';
import { LONG_WEB_VITAL_NAMES, WEB_VITAL_ACRONYMS, } from 'app/views/performance/transactionVitals/constants';
import { getMeasurementBounds, getMeasurements, toPercent, } from './utils';
var MeasurementsPanel = /** @class */ (function (_super) {
    __extends(MeasurementsPanel, _super);
    function MeasurementsPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MeasurementsPanel.prototype.render = function () {
        var _a = this.props, event = _a.event, generateBounds = _a.generateBounds, dividerPosition = _a.dividerPosition;
        var measurements = getMeasurements(event);
        return (<Container style={{
            // the width of this component is shrunk to compensate for half of the width of the divider line
            width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
        }}>
        {Array.from(measurements).map(function (_a) {
            var _b = __read(_a, 2), timestamp = _b[0], verticalMark = _b[1];
            var bounds = getMeasurementBounds(timestamp, generateBounds);
            var shouldDisplay = defined(bounds.left) && defined(bounds.width);
            if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                return null;
            }
            var names = Object.keys(verticalMark.marks);
            // generate vertical marker label
            var acronyms = names.map(function (name) { return WEB_VITAL_ACRONYMS[name]; });
            var lastAcronym = acronyms.pop();
            var label = acronyms.length
                ? acronyms.join(', ') + " & " + lastAcronym
                : lastAcronym;
            // generate tooltip labe;l
            var longNames = names.map(function (name) { return LONG_WEB_VITAL_NAMES[name]; });
            var lastName = longNames.pop();
            var tooltipLabel = longNames.length
                ? longNames.join(', ') + " & " + lastName
                : lastName;
            return (<LabelContainer key={String(timestamp)} failedThreshold={verticalMark.failedThreshold} label={label} tooltipLabel={tooltipLabel} left={toPercent(bounds.left || 0)}/>);
        })}
      </Container>);
    };
    return MeasurementsPanel;
}(React.PureComponent));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  overflow: hidden;\n\n  height: 20px;\n"], ["\n  position: relative;\n  overflow: hidden;\n\n  height: 20px;\n"])));
var StyledLabelContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: 100%;\n  user-select: none;\n  white-space: nowrap;\n"], ["\n  position: absolute;\n  top: 0;\n  height: 100%;\n  user-select: none;\n  white-space: nowrap;\n"])));
var Label = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  transform: translateX(-50%);\n  font-size: ", ";\n  font-weight: 600;\n  ", "\n"], ["\n  transform: translateX(-50%);\n  font-size: ", ";\n  font-weight: 600;\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return (p.failedThreshold ? "color: " + p.theme.red300 + ";" : null); });
export default MeasurementsPanel;
var LabelContainer = /** @class */ (function (_super) {
    __extends(LabelContainer, _super);
    function LabelContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: 1,
        };
        _this.elementDOMRef = React.createRef();
        return _this;
    }
    LabelContainer.prototype.componentDidMount = function () {
        var current = this.elementDOMRef.current;
        if (current) {
            // eslint-disable-next-line react/no-did-mount-set-state
            this.setState({
                width: current.clientWidth,
            });
        }
    };
    LabelContainer.prototype.render = function () {
        var _a = this.props, left = _a.left, label = _a.label, tooltipLabel = _a.tooltipLabel, failedThreshold = _a.failedThreshold;
        return (<StyledLabelContainer ref={this.elementDOMRef} style={{
            left: "clamp(calc(0.5 * " + this.state.width + "px), " + left + ", calc(100% - 0.5 * " + this.state.width + "px))",
        }}>
        <Label failedThreshold={failedThreshold}>
          <Tooltip title={tooltipLabel} position="top" containerDisplayMode="inline-block">
            {label}
          </Tooltip>
        </Label>
      </StyledLabelContainer>);
    };
    return LabelContainer;
}(React.Component));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=measurementsPanel.jsx.map