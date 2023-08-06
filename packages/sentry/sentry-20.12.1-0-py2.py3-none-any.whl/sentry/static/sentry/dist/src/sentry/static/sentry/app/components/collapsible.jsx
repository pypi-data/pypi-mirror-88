import { __extends } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import { t, tn } from 'app/locale';
var Collapsible = /** @class */ (function (_super) {
    __extends(Collapsible, _super);
    function Collapsible() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        _this.handleCollapseToggle = function () {
            _this.setState(function (prevState) { return ({
                collapsed: !prevState.collapsed,
            }); });
        };
        return _this;
    }
    Collapsible.prototype.renderCollapseButton = function () {
        var collapseButton = this.props.collapseButton;
        if (typeof collapseButton === 'function') {
            return collapseButton({ onCollapse: this.handleCollapseToggle });
        }
        return (<Button priority="link" onClick={this.handleCollapseToggle}>
        {t('Collapse')}
      </Button>);
    };
    Collapsible.prototype.renderExpandButton = function (numberOfCollapsedItems) {
        var expandButton = this.props.expandButton;
        if (typeof expandButton === 'function') {
            return expandButton({
                onExpand: this.handleCollapseToggle,
                numberOfCollapsedItems: numberOfCollapsedItems,
            });
        }
        return (<Button priority="link" onClick={this.handleCollapseToggle}>
        {tn('Show %s collapsed item', 'Show %s collapsed items', numberOfCollapsedItems)}
      </Button>);
    };
    Collapsible.prototype.render = function () {
        var _a = this.props, maxVisibleItems = _a.maxVisibleItems, children = _a.children;
        var collapsed = this.state.collapsed;
        var items = React.Children.toArray(children);
        var canExpand = items.length > maxVisibleItems;
        var itemsToRender = collapsed && canExpand ? items.slice(0, maxVisibleItems) : items;
        var numberOfCollapsedItems = items.length - itemsToRender.length;
        return (<React.Fragment>
        {itemsToRender}

        {numberOfCollapsedItems > 0 && this.renderExpandButton(numberOfCollapsedItems)}

        {numberOfCollapsedItems === 0 && canExpand && this.renderCollapseButton()}
      </React.Fragment>);
    };
    Collapsible.defaultProps = {
        maxVisibleItems: 5,
    };
    return Collapsible;
}(React.Component));
export default Collapsible;
//# sourceMappingURL=collapsible.jsx.map