import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { formatPercentage } from 'app/utils/formatters';
import theme from 'app/utils/theme';
import { VitalState, vitalStateColors } from './utils';
export default function VitalPercents(props) {
    return (<VitalSet>
      {props.percents.map(function (p) {
        return (<VitalStatus key={p.vitalState}>
            {p.vitalState === VitalState.POOR && (<IconFire color={vitalStateColors[p.vitalState]}/>)}
            {p.vitalState === VitalState.MEH && (<IconWarning color={vitalStateColors[p.vitalState]}/>)}
            {p.vitalState === VitalState.GOOD && (<IconCheckmark color={vitalStateColors[p.vitalState]} isCircled/>)}
            <span>
              {props.showVitalPercentNames && t("" + p.vitalState)}{' '}
              {formatPercentage(p.percent, 0)}
            </span>
          </VitalStatus>);
    })}
    </VitalSet>);
}
var VitalSet = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"])), space(2));
var VitalStatus = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"])), space(0.5), theme.fontSizeMedium);
var templateObject_1, templateObject_2;
//# sourceMappingURL=vitalPercents.jsx.map