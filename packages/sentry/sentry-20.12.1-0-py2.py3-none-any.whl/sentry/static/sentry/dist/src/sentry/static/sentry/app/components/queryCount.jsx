import React from 'react';
import PropTypes from 'prop-types';
import { defined } from 'app/utils';
/**
 * Displays a number count. If `max` is specified, then give representation
 * of count, i.e. "1000+"
 *
 * Render nothing by default if `count` is falsy.
 */
var QueryCount = function (_a) {
    var count = _a.count, max = _a.max, _b = _a.hideIfEmpty, hideIfEmpty = _b === void 0 ? true : _b, _c = _a.hideParens, hideParens = _c === void 0 ? false : _c;
    var countOrMax = defined(count) && defined(max) && count >= max ? max + "+" : count;
    if (hideIfEmpty && !count) {
        return null;
    }
    return (<span>
      {!hideParens && <span>(</span>}
      <span>{countOrMax}</span>
      {!hideParens && <span>)</span>}
    </span>);
};
QueryCount.propTypes = {
    count: PropTypes.number,
    max: PropTypes.number,
    hideIfEmpty: PropTypes.bool,
    hideParens: PropTypes.bool,
};
export default QueryCount;
//# sourceMappingURL=queryCount.jsx.map