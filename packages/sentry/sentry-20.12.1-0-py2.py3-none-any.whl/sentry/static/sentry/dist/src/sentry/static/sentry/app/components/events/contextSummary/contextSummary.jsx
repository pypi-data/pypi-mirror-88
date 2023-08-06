import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { objectIsEmpty } from 'app/utils';
import ContextSummaryDevice from './contextSummaryDevice';
import ContextSummaryGeneric from './contextSummaryGeneric';
import ContextSummaryGPU from './contextSummaryGPU';
import ContextSummaryOS from './contextSummaryOS';
import ContextSummaryUser from './contextSummaryUser';
import filterContexts from './filterContexts';
var MIN_CONTEXTS = 3;
var MAX_CONTEXTS = 4;
var KNOWN_CONTEXTS = [
    { keys: ['user'], Component: ContextSummaryUser },
    {
        keys: ['browser'],
        Component: ContextSummaryGeneric,
        unknownTitle: t('Unknown Browser'),
    },
    {
        keys: ['runtime'],
        Component: ContextSummaryGeneric,
        unknownTitle: t('Unknown Runtime'),
    },
    { keys: ['client_os', 'os'], Component: ContextSummaryOS },
    { keys: ['device'], Component: ContextSummaryDevice },
    { keys: ['gpu'], Component: ContextSummaryGPU },
];
var ContextSummary = /** @class */ (function (_super) {
    __extends(ContextSummary, _super);
    function ContextSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ContextSummary.prototype.render = function () {
        var event = this.props.event;
        var contextCount = 0;
        // Add defined contexts in the declared order, until we reach the limit
        // defined by MAX_CONTEXTS.
        var contexts = KNOWN_CONTEXTS.filter(function (context) { return filterContexts(event, context); }).map(function (_a) {
            var keys = _a.keys, Component = _a.Component, unknownTitle = _a.unknownTitle;
            if (contextCount >= MAX_CONTEXTS) {
                return null;
            }
            var _b = __read(keys
                .map(function (k) { return [k, event.contexts[k] || event[k]]; })
                .find(function (_a) {
                var _b = __read(_a, 2), _k = _b[0], d = _b[1];
                return !objectIsEmpty(d);
            }) || [null, null], 2), key = _b[0], data = _b[1];
            if (!key) {
                return null;
            }
            contextCount += 1;
            return <Component key={key} data={data} unknownTitle={unknownTitle}/>;
        });
        // Bail out if all contexts are empty or only the user context is set
        if (contextCount === 0 || (contextCount === 1 && contexts[0])) {
            return null;
        }
        if (contextCount < MIN_CONTEXTS) {
            // Add contents in the declared order until we have at least MIN_CONTEXTS
            // contexts in our list.
            contexts = KNOWN_CONTEXTS.filter(function (context) { return filterContexts(event, context); }).map(function (_a, index) {
                var keys = _a.keys, Component = _a.Component, unknownTitle = _a.unknownTitle;
                if (contexts[index]) {
                    return contexts[index];
                }
                if (contextCount >= MIN_CONTEXTS) {
                    return null;
                }
                contextCount += 1;
                return <Component key={keys[0]} data={{}} unknownTitle={unknownTitle}/>;
            });
        }
        return <Wrapper className="context-summary">{contexts}</Wrapper>;
    };
    return ContextSummary;
}(React.Component));
export default ContextSummary;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-auto-flow: column;\n    grid-auto-columns: minmax(0, auto);\n    grid-gap: ", ";\n    padding: 25px ", " 25px 40px;\n  }\n"], ["\n  border-top: 1px solid ", ";\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-auto-flow: column;\n    grid-auto-columns: minmax(0, auto);\n    grid-gap: ", ";\n    padding: 25px ", " 25px 40px;\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.breakpoints[0]; }, space(4), space(4));
var templateObject_1;
//# sourceMappingURL=contextSummary.jsx.map