import { __rest } from "tslib";
import React from 'react';
import classnames from 'classnames';
import PropTypes from 'prop-types';
function NavTabs(props) {
    var underlined = props.underlined, className = props.className, tabProps = __rest(props, ["underlined", "className"]);
    var mergedClassName = classnames('nav nav-tabs', className, {
        'border-bottom': underlined,
    });
    return <ul className={mergedClassName} {...tabProps}/>;
}
NavTabs.propTypes = {
    underlined: PropTypes.bool,
};
export default NavTabs;
//# sourceMappingURL=navTabs.jsx.map