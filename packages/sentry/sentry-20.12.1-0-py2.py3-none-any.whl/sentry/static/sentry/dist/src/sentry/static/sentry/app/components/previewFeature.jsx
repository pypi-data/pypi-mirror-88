import React from 'react';
import PropTypes from 'prop-types';
import Alert from 'app/components/alert';
import { IconLab } from 'app/icons';
import { t } from 'app/locale';
var PreviewFeature = function (_a) {
    var _b = _a.type, type = _b === void 0 ? 'info' : _b;
    return (<Alert type={type} icon={<IconLab size="sm"/>}>
    {t('This feature is a preview and may change in the future. Thanks for being an early adopter!')}
  </Alert>);
};
PreviewFeature.propTypes = {
    type: PropTypes.oneOf(['success', 'error', 'warning', 'info']),
};
export default PreviewFeature;
//# sourceMappingURL=previewFeature.jsx.map