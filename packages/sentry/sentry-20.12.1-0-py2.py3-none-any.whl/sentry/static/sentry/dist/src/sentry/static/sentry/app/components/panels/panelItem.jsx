import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import { Flex } from 'reflexbox'; // eslint-disable-line no-restricted-imports
var PanelItem = styled(Flex)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n\n  &:last-child {\n    border: 0;\n  }\n"])), function (p) { return p.theme.innerBorder; });
PanelItem.propTypes = {
    p: PropTypes.number,
};
PanelItem.defaultProps = {
    p: 2,
};
export default PanelItem;
var templateObject_1;
//# sourceMappingURL=panelItem.jsx.map