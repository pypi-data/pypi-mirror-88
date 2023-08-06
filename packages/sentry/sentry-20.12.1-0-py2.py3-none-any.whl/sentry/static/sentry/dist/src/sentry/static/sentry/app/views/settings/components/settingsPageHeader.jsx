import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { HeaderTitle } from 'app/styles/organization';
import space from 'app/styles/space';
var UnstyledSettingsPageHeader = /** @class */ (function (_super) {
    __extends(UnstyledSettingsPageHeader, _super);
    function UnstyledSettingsPageHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UnstyledSettingsPageHeader.prototype.render = function () {
        var _a = this.props, icon = _a.icon, title = _a.title, subtitle = _a.subtitle, action = _a.action, tabs = _a.tabs, noTitleStyles = _a.noTitleStyles, props = __rest(_a, ["icon", "title", "subtitle", "action", "tabs", "noTitleStyles"]);
        return (<div {...props}>
        <TitleAndActions>
          <TitleWrapper>
            {icon && <Icon>{icon}</Icon>}
            {title && (<Title tabs={tabs} styled={noTitleStyles}>
                <HeaderTitle>{title}</HeaderTitle>
                {subtitle && <Subtitle>{subtitle}</Subtitle>}
              </Title>)}
          </TitleWrapper>
          {action && <Action tabs={tabs}>{action}</Action>}
        </TitleAndActions>

        {tabs && <div>{tabs}</div>}
      </div>);
    };
    UnstyledSettingsPageHeader.defaultProps = {
        noTitleStyles: false,
    };
    return UnstyledSettingsPageHeader;
}(React.Component));
var TitleAndActions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TitleWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  margin: ", ";\n"], ["\n  ",
    ";\n  margin: ",
    ";\n"])), function (p) {
    return !p.styled &&
        "\n    font-size: 20px;\n    font-weight: bold;";
}, function (p) {
    return p.tabs
        ? space(4) + " " + space(2) + " " + space(2) + " 0"
        : space(4) + " " + space(2) + " " + space(4) + " 0";
});
var Subtitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: 400;\n  font-size: ", ";\n  padding: ", " 0 ", ";\n"], ["\n  color: ", ";\n  font-weight: 400;\n  font-size: ", ";\n  padding: ", " 0 ", ";\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeLarge; }, space(1.5), space(3));
var Icon = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Action = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return (p.tabs ? "margin-top: " + space(2) : null); });
var SettingsPageHeader = styled(UnstyledSettingsPageHeader)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: 14px;\n  margin-top: -", ";\n"], ["\n  font-size: 14px;\n  margin-top: -", ";\n"])), space(4));
export default SettingsPageHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=settingsPageHeader.jsx.map