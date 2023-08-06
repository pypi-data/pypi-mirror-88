import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import { getMeta } from 'app/components/events/meta/metaProxy';
import TextOverflow from 'app/components/textOverflow';
import { t } from 'app/locale';
import space from 'app/styles/space';
import ContextSummaryNoSummary from './contextSummaryNoSummary';
import generateClassName from './generateClassName';
import Item from './item';
var ContextSummaryGPU = function (_a) {
    var data = _a.data;
    if (Object.keys(data).length === 0 || !data.name) {
        return <ContextSummaryNoSummary title={t('Unknown GPU')}/>;
    }
    var renderName = function () {
        var meta = getMeta(data, 'name');
        return <AnnotatedText value={data.name} meta={meta}/>;
    };
    var className = generateClassName(data.name);
    var getVersionElement = function () {
        if (data.vendor_name) {
            className = generateClassName(data.vendor_name);
            return {
                subject: t('Vendor:'),
                value: data.vendor_name,
                meta: getMeta(data, 'vendor_name'),
            };
        }
        return {
            subject: t('Vendor:'),
            value: t('Unknown'),
        };
    };
    var versionElement = getVersionElement();
    return (<Item className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      <TextOverflow isParagraph>
        <Subject>{versionElement.subject}</Subject>
        <AnnotatedText value={versionElement.value} meta={versionElement.meta}/>
      </TextOverflow>
    </Item>);
};
ContextSummaryGPU.propTypes = {
    data: PropTypes.object.isRequired,
};
export default ContextSummaryGPU;
var Subject = styled('strong')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1;
//# sourceMappingURL=contextSummaryGPU.jsx.map