import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var ColorBar = function (props) {
    return (<VitalBar fractions={props.colorStops.map(function (_a) {
        var percent = _a.percent;
        return percent;
    })}>
      {props.colorStops.map(function (colorStop) {
        return <BarStatus color={colorStop.color} key={colorStop.color}/>;
    })}
    </VitalBar>);
};
var VitalBar = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 16px;\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  background: ", ";\n  display: grid;\n  grid-template-columns: ", ";\n  margin-bottom: ", ";\n  border-radius: ", ";\n"], ["\n  height: 16px;\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  background: ", ";\n  display: grid;\n  grid-template-columns: ", ";\n  margin-bottom: ", ";\n  border-radius: ", ";\n"])), function (p) { return p.theme.gray100; }, function (p) { return p.fractions.map(function (f) { return f + "fr"; }).join(' '); }, space(1), function (p) { return p.theme.borderRadius; });
var BarStatus = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background-color: ", ";\n"], ["\n  background-color: ", ";\n"])), function (p) { return p.color; });
export default ColorBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=colorBar.jsx.map