import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import classNames from 'classnames';
import omit from 'lodash/omit';
import PropTypes from 'prop-types';
var ListLink = /** @class */ (function (_super) {
    __extends(ListLink, _super);
    function ListLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.isActive = function () {
            var _a = _this.props, isActive = _a.isActive, to = _a.to, query = _a.query, index = _a.index;
            return (isActive || _this.context.router.isActive)({ pathname: to, query: query }, index);
        };
        _this.getClassName = function () {
            var _classNames = {};
            var _a = _this.props, className = _a.className, activeClassName = _a.activeClassName;
            if (className) {
                _classNames[className] = true;
            }
            if (_this.isActive()) {
                _classNames[activeClassName] = true;
            }
            return classNames(_classNames);
        };
        return _this;
    }
    ListLink.prototype.render = function () {
        var _a = this.props, index = _a.index, children = _a.children, to = _a.to, disabled = _a.disabled, props = __rest(_a, ["index", "children", "to", "disabled"]);
        var carriedProps = omit(props, 'activeClassName', 'isActive', 'index');
        return (<StyledLi className={this.getClassName()} disabled={disabled}>
        <Link {...carriedProps} onlyActiveOnIndex={index} to={disabled ? '' : to}>
          {children}
        </Link>
      </StyledLi>);
    };
    ListLink.displayName = 'ListLink';
    ListLink.contextTypes = {
        router: PropTypes.object.isRequired,
    };
    ListLink.defaultProps = {
        activeClassName: 'active',
        index: false,
        disabled: false,
    };
    return ListLink;
}(React.Component));
export default ListLink;
var StyledLi = styled('li', {
    shouldForwardProp: function (prop) { return prop !== 'disabled'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.disabled &&
        "\n   a {\n    color:" + p.theme.disabled + " !important;\n    pointer-events: none;\n    :hover {\n      color: " + p.theme.disabled + "  !important;\n    }\n   }\n";
});
var templateObject_1;
//# sourceMappingURL=listLink.jsx.map