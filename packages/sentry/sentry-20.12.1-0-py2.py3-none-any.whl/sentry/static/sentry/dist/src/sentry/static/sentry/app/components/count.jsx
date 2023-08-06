import React from 'react';
import PropTypes from 'prop-types';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
function Count(props) {
    var value = props.value, className = props.className;
    return (<span className={className} title={value.toLocaleString()}>
      {formatAbbreviatedNumber(value)}
    </span>);
}
Count.propTypes = {
    value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
};
export default Count;
//# sourceMappingURL=count.jsx.map