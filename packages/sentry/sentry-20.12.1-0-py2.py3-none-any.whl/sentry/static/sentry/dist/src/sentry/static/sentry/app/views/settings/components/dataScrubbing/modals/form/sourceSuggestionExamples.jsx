import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Hovercard from 'app/components/hovercard';
import { IconQuestion } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var SourceSuggestionExamples = function (_a) {
    var examples = _a.examples, sourceName = _a.sourceName;
    return (<Wrapper>
    <ExampleCard position="right" header={t('Examples for %s in current event', <code>{sourceName}</code>)} body={examples.map(function (example) { return (<pre key={example}>{example}</pre>); })}>
      <Content>
        {t('See Example')} <IconQuestion size="xs"/>
      </Content>
    </ExampleCard>
  </Wrapper>);
};
export default SourceSuggestionExamples;
var ExampleCard = styled(Hovercard)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 400px;\n\n  pre:last-child {\n    margin: 0;\n  }\n"], ["\n  width: 400px;\n\n  pre:last-child {\n    margin: 0;\n  }\n"])));
var Content = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  text-decoration: underline;\n  text-decoration-style: dotted;\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n  text-decoration: underline;\n  text-decoration-style: dotted;\n"])), space(0.5), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeSmall; });
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 3/3;\n"], ["\n  grid-column: 3/3;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sourceSuggestionExamples.jsx.map