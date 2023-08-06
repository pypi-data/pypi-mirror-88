import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { InlineContainer, SectionHeading } from 'app/components/charts/styles';
import DropdownBubble from 'app/components/dropdownBubble';
import DropdownButton from 'app/components/dropdownButton';
import { DropdownItem } from 'app/components/dropdownControl';
import DropdownMenu from 'app/components/dropdownMenu';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var defaultProps = {
    menuWidth: 'auto',
};
var OptionSelector = /** @class */ (function (_super) {
    __extends(OptionSelector, _super);
    function OptionSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.menuContainerRef = React.createRef();
        return _this;
    }
    OptionSelector.prototype.componentDidMount = function () {
        this.setMenuContainerWidth();
    };
    OptionSelector.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        return !isEqual(nextProps, this.props) || !isEqual(nextState, this.state);
    };
    OptionSelector.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.selected !== this.props.selected) {
            this.setMenuContainerWidth();
        }
    };
    OptionSelector.prototype.setMenuContainerWidth = function () {
        var _a, _b;
        var menuContainerWidth = (_b = (_a = this.menuContainerRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetWidth;
        if (menuContainerWidth) {
            this.setState({ menuContainerWidth: menuContainerWidth });
        }
    };
    OptionSelector.prototype.render = function () {
        var menuContainerWidth = this.state.menuContainerWidth;
        var _a = this.props, options = _a.options, onChange = _a.onChange, selected = _a.selected, title = _a.title, menuWidth = _a.menuWidth;
        var selectedOption = options.find(function (opt) { return selected === opt.value; }) || options[0];
        return (<InlineContainer>
        <SectionHeading>{title}</SectionHeading>
        <MenuContainer ref={this.menuContainerRef}>
          <DropdownMenu alwaysRenderMenu={false}>
            {function (_a) {
            var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
            return (<React.Fragment>
                <StyledDropdownButton {...getActorProps()} size="zero" isOpen={isOpen}>
                  {selectedOption.label}
                </StyledDropdownButton>
                <StyledDropdownBubble {...getMenuProps()} alignMenu="right" width={menuWidth} minWidth={menuContainerWidth} isOpen={isOpen} blendWithActor={false} blendCorner>
                  {options.map(function (opt) { return (<StyledDropdownItem key={opt.value} onSelect={onChange} eventKey={opt.value} disabled={opt.disabled} isActive={selected === opt.value} data-test-id={"option-" + opt.value}>
                      <Tooltip title={opt.tooltip} containerDisplayMode="inline">
                        {opt.label}
                      </Tooltip>
                    </StyledDropdownItem>); })}
                </StyledDropdownBubble>
              </React.Fragment>);
        }}
          </DropdownMenu>
        </MenuContainer>
      </InlineContainer>);
    };
    OptionSelector.defaultProps = defaultProps;
    return OptionSelector;
}(React.Component));
var MenuContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n"], ["\n  display: inline-block;\n  position: relative;\n"])));
var StyledDropdownButton = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-weight: normal;\n  z-index: ", ";\n"], ["\n  padding: ", " ", ";\n  font-weight: normal;\n  z-index: ", ";\n"])), space(1), space(2), function (p) { return (p.isOpen ? p.theme.zIndex.dropdownAutocomplete.actor : 'auto'); });
var StyledDropdownBubble = styled(DropdownBubble)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: ", ";\n  ", ";\n"], ["\n  display: ", ";\n  ",
    ";\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); }, function (p) {
    return p.minWidth && p.width === 'auto' && "min-width: calc(" + p.minWidth + "px + " + space(3) + ")";
});
var StyledDropdownItem = styled(DropdownItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
export default OptionSelector;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=optionSelector.jsx.map