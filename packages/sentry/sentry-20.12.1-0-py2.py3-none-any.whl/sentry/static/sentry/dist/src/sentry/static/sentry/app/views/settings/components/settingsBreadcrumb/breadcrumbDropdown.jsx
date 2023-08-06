import { __extends } from "tslib";
import React from 'react';
import DropdownAutoCompleteMenu from 'app/components/dropdownAutoComplete/menu';
import Crumb from 'app/views/settings/components/settingsBreadcrumb/crumb';
import Divider from 'app/views/settings/components/settingsBreadcrumb/divider';
var EXIT_DELAY = 0;
var BreadcrumbDropdown = /** @class */ (function (_super) {
    __extends(BreadcrumbDropdown, _super);
    function BreadcrumbDropdown() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.entering = null;
        _this.leaving = null;
        _this.open = function () {
            _this.setState({ isOpen: true });
        };
        _this.close = function () {
            _this.setState({ isOpen: false });
        };
        _this.handleStateChange = function () { };
        // Adds a delay when mouse hovers on actor (in this case the breadcrumb)
        _this.handleMouseEnterActor = function () {
            var _a;
            if (_this.leaving) {
                clearTimeout(_this.leaving);
            }
            _this.entering = window.setTimeout(function () { return _this.open(); }, (_a = _this.props.enterDelay) !== null && _a !== void 0 ? _a : 0);
        };
        // handles mouseEnter event on actor and menu, should clear the leaving timeout and keep menu open
        _this.handleMouseEnter = function () {
            if (_this.leaving) {
                clearTimeout(_this.leaving);
            }
            _this.open();
        };
        // handles mouseLeave event on actor and menu, adds a timeout before updating state to account for
        // mouseLeave into
        _this.handleMouseLeave = function () {
            if (_this.entering) {
                clearTimeout(_this.entering);
            }
            _this.leaving = window.setTimeout(function () { return _this.close(); }, EXIT_DELAY);
        };
        // Close immediately when actor is clicked clicked
        _this.handleClickActor = function () {
            _this.close();
        };
        // Close immediately when clicked outside
        _this.handleClose = function () {
            _this.close();
        };
        return _this;
    }
    BreadcrumbDropdown.prototype.render = function () {
        var _this = this;
        var _a = this.props, hasMenu = _a.hasMenu, route = _a.route, isLast = _a.isLast, name = _a.name, items = _a.items, onSelect = _a.onSelect;
        return (<DropdownAutoCompleteMenu blendCorner={false} onOpen={this.handleMouseEnter} onClose={this.close} isOpen={this.state.isOpen} menuProps={{
            onMouseEnter: this.handleMouseEnter,
            onMouseLeave: this.handleMouseLeave,
        }} items={items} onSelect={onSelect} virtualizedHeight={41}>
        {function (_a) {
            var getActorProps = _a.getActorProps, actions = _a.actions, isOpen = _a.isOpen;
            return (<Crumb {...getActorProps({
                onClick: _this.handleClickActor.bind(_this, actions),
                onMouseEnter: _this.handleMouseEnterActor.bind(_this, actions),
                onMouseLeave: _this.handleMouseLeave.bind(_this, actions),
            })}>
            <span>{name || route.name} </span>
            <Divider isHover={hasMenu && isOpen} isLast={isLast}/>
          </Crumb>);
        }}
      </DropdownAutoCompleteMenu>);
    };
    return BreadcrumbDropdown;
}(React.Component));
export default BreadcrumbDropdown;
//# sourceMappingURL=breadcrumbDropdown.jsx.map