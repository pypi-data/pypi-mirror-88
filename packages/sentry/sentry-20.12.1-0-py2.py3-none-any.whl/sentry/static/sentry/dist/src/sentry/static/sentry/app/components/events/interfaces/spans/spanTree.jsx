import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t, tct } from 'app/locale';
import { DividerLine } from './spanBar';
import SpanGroup from './spanGroup';
import { SpanRowMessage } from './styles';
import { boundsGenerator, generateRootSpan, getSpanID, getSpanOperation, getSpanTraceID, isEventFromBrowserJavaScriptSDK, isGapSpan, isOrphanSpan, pickSpanBarColour, } from './utils';
var SpanTree = /** @class */ (function (_super) {
    __extends(SpanTree, _super);
    function SpanTree() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderSpan = function (_a) {
            var _b;
            var spanNumber = _a.spanNumber, isRoot = _a.isRoot, isLast = _a.isLast, treeDepth = _a.treeDepth, continuingTreeDepths = _a.continuingTreeDepths, numOfSpansOutOfViewAbove = _a.numOfSpansOutOfViewAbove, numOfFilteredSpansAbove = _a.numOfFilteredSpansAbove, childSpans = _a.childSpans, span = _a.span, generateBounds = _a.generateBounds, previousSiblingEndTimestamp = _a.previousSiblingEndTimestamp;
            var _c = _this.props, orgId = _c.orgId, event = _c.event, spansWithErrors = _c.spansWithErrors, organization = _c.organization;
            var spanBarColour = pickSpanBarColour(getSpanOperation(span));
            var spanChildren = (_b = childSpans === null || childSpans === void 0 ? void 0 : childSpans[getSpanID(span)]) !== null && _b !== void 0 ? _b : [];
            // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
            // For example if a span has a span_id that's identical to its parent_span_id.
            childSpans = __assign({}, childSpans);
            delete childSpans[getSpanID(span)];
            var bounds = generateBounds({
                startTimestamp: span.start_timestamp,
                endTimestamp: span.timestamp,
            });
            var isCurrentSpanHidden = !bounds.isSpanVisibleInView;
            var isCurrentSpanFilteredOut = isGapSpan(span)
                ? false
                : _this.isSpanFilteredOut(span);
            var isSpanDisplayed = !isCurrentSpanHidden && !isCurrentSpanFilteredOut;
            // hide gap spans (i.e. "missing instrumentation" spans) for browser js transactions,
            // since they're not useful to indicate
            var shouldIncludeGap = !isEventFromBrowserJavaScriptSDK(event);
            var isValidGap = typeof previousSiblingEndTimestamp === 'number' &&
                previousSiblingEndTimestamp < span.start_timestamp &&
                // gap is at least 100 ms
                span.start_timestamp - previousSiblingEndTimestamp >= 0.1 &&
                shouldIncludeGap;
            var spanGroupNumber = isValidGap && isSpanDisplayed ? spanNumber + 1 : spanNumber;
            var treeDepthEntry = isOrphanSpan(span)
                ? { type: 'orphan', depth: treeDepth }
                : treeDepth;
            var treeArr = isLast
                ? continuingTreeDepths
                : __spread(continuingTreeDepths, [treeDepthEntry]);
            var reduced = spanChildren.reduce(function (acc, spanChild, index) {
                var key = "" + getSpanTraceID(span) + getSpanID(spanChild);
                var results = _this.renderSpan({
                    spanNumber: acc.nextSpanNumber,
                    isLast: index + 1 === spanChildren.length,
                    continuingTreeDepths: treeArr,
                    treeDepth: treeDepth + 1,
                    numOfSpansOutOfViewAbove: acc.numOfSpansOutOfViewAbove,
                    numOfFilteredSpansAbove: acc.numOfFilteredSpansAbove,
                    span: spanChild,
                    childSpans: childSpans,
                    generateBounds: generateBounds,
                    previousSiblingEndTimestamp: acc.previousSiblingEndTimestamp,
                });
                acc.renderedSpanChildren.push(<React.Fragment key={key}>{results.spanTree}</React.Fragment>);
                acc.numOfSpansOutOfViewAbove = results.numOfSpansOutOfViewAbove;
                acc.numOfFilteredSpansAbove = results.numOfFilteredSpansAbove;
                acc.nextSpanNumber = results.nextSpanNumber;
                acc.previousSiblingEndTimestamp = spanChild.timestamp;
                return acc;
            }, {
                renderedSpanChildren: [],
                nextSpanNumber: spanGroupNumber + 1,
                numOfSpansOutOfViewAbove: isCurrentSpanHidden ? numOfSpansOutOfViewAbove + 1 : 0,
                numOfFilteredSpansAbove: isCurrentSpanFilteredOut
                    ? numOfFilteredSpansAbove + 1
                    : isCurrentSpanHidden
                        ? numOfFilteredSpansAbove
                        : 0,
                previousSiblingEndTimestamp: undefined,
            });
            var infoMessage = _this.generateInfoMessage({
                isCurrentSpanHidden: isCurrentSpanHidden,
                numOfSpansOutOfViewAbove: numOfSpansOutOfViewAbove,
                isCurrentSpanFilteredOut: isCurrentSpanFilteredOut,
                numOfFilteredSpansAbove: numOfFilteredSpansAbove,
            });
            var spanGap = {
                type: 'gap',
                start_timestamp: previousSiblingEndTimestamp || span.start_timestamp,
                timestamp: span.start_timestamp,
                description: t('Missing instrumentation'),
                isOrphan: isOrphanSpan(span),
            };
            var spanGapComponent = isValidGap && isSpanDisplayed ? (<SpanGroup orgId={orgId} organization={organization} event={event} spanNumber={spanNumber} isLast={false} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} span={spanGap} trace={_this.props.trace} generateBounds={generateBounds} treeDepth={treeDepth} numOfSpanChildren={0} renderedSpanChildren={[]} isCurrentSpanFilteredOut={isCurrentSpanFilteredOut} spansWithErrors={spansWithErrors} spanBarHatch/>) : null;
            return {
                numOfSpansOutOfViewAbove: reduced.numOfSpansOutOfViewAbove,
                numOfFilteredSpansAbove: reduced.numOfFilteredSpansAbove,
                nextSpanNumber: reduced.nextSpanNumber,
                spanTree: (<React.Fragment>
          {infoMessage}
          {spanGapComponent}
          <SpanGroup orgId={orgId} organization={organization} event={event} spanNumber={spanGroupNumber} isLast={isLast} continuingTreeDepths={continuingTreeDepths} isRoot={isRoot} span={span} trace={_this.props.trace} generateBounds={generateBounds} treeDepth={treeDepth} numOfSpanChildren={spanChildren.length} renderedSpanChildren={reduced.renderedSpanChildren} spanBarColour={spanBarColour} isCurrentSpanFilteredOut={isCurrentSpanFilteredOut} spanBarHatch={false} spansWithErrors={spansWithErrors}/>
        </React.Fragment>),
            };
        };
        _this.renderRootSpan = function () {
            var trace = _this.props.trace;
            var rootSpan = generateRootSpan(trace);
            var generateBounds = _this.generateBounds();
            return _this.renderSpan({
                isRoot: true,
                isLast: true,
                spanNumber: 1,
                treeDepth: 0,
                continuingTreeDepths: [],
                numOfSpansOutOfViewAbove: 0,
                numOfFilteredSpansAbove: 0,
                span: rootSpan,
                childSpans: trace.childSpans,
                generateBounds: generateBounds,
                previousSiblingEndTimestamp: undefined,
            });
        };
        return _this;
    }
    SpanTree.prototype.shouldComponentUpdate = function (nextProps) {
        if (nextProps.dragProps.isDragging || nextProps.dragProps.isWindowSelectionDragging) {
            return false;
        }
        return true;
    };
    SpanTree.prototype.generateInfoMessage = function (input) {
        var isCurrentSpanHidden = input.isCurrentSpanHidden, numOfSpansOutOfViewAbove = input.numOfSpansOutOfViewAbove, isCurrentSpanFilteredOut = input.isCurrentSpanFilteredOut, numOfFilteredSpansAbove = input.numOfFilteredSpansAbove;
        var messages = [];
        var showHiddenSpansMessage = !isCurrentSpanHidden && numOfSpansOutOfViewAbove > 0;
        if (showHiddenSpansMessage) {
            messages.push(<span key="spans-out-of-view">
          <strong>{numOfSpansOutOfViewAbove}</strong> {t('spans out of view')}
        </span>);
        }
        var showFilteredSpansMessage = !isCurrentSpanFilteredOut && numOfFilteredSpansAbove > 0;
        if (showFilteredSpansMessage) {
            if (!isCurrentSpanHidden) {
                if (numOfFilteredSpansAbove === 1) {
                    messages.push(<span key="spans-filtered">
              {tct('[numOfSpans] hidden span', {
                        numOfSpans: <strong>{numOfFilteredSpansAbove}</strong>,
                    })}
            </span>);
                }
                else {
                    messages.push(<span key="spans-filtered">
              {tct('[numOfSpans] hidden spans', {
                        numOfSpans: <strong>{numOfFilteredSpansAbove}</strong>,
                    })}
            </span>);
                }
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <SpanRowMessage>{messages}</SpanRowMessage>;
    };
    SpanTree.prototype.generateLimitExceededMessage = function () {
        var trace = this.props.trace;
        if (hasAllSpans(trace)) {
            return null;
        }
        return (<SpanRowMessage>
        {t('The next spans are unavailable. You may have exceeded the span limit or need to address missing instrumentation.')}
      </SpanRowMessage>);
    };
    SpanTree.prototype.isSpanFilteredOut = function (span) {
        var _a = this.props, filterSpans = _a.filterSpans, operationNameFilters = _a.operationNameFilters;
        if (operationNameFilters.type === 'active_filter') {
            var operationName = getSpanOperation(span);
            if (typeof operationName === 'string' &&
                !operationNameFilters.operationNames.has(operationName)) {
                return true;
            }
        }
        if (!filterSpans) {
            return false;
        }
        return !filterSpans.spanIDs.has(getSpanID(span));
    };
    SpanTree.prototype.generateBounds = function () {
        var _a = this.props, dragProps = _a.dragProps, trace = _a.trace;
        return boundsGenerator({
            traceStartTimestamp: trace.traceStartTimestamp,
            traceEndTimestamp: trace.traceEndTimestamp,
            viewStart: dragProps.viewWindowStart,
            viewEnd: dragProps.viewWindowEnd,
        });
    };
    SpanTree.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<DividerLine ref={addDividerLineRef()} style={{
            position: 'relative',
        }} onMouseEnter={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseLeave={function () {
            dividerHandlerChildrenProps.setHover(false);
        }} onMouseOver={function () {
            dividerHandlerChildrenProps.setHover(true);
        }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
            // we prevent the propagation of the clicks from this component to prevent
            // the span detail from being opened.
            event.stopPropagation();
        }}/>);
    };
    SpanTree.prototype.render = function () {
        var _a = this.renderRootSpan(), spanTree = _a.spanTree, numOfSpansOutOfViewAbove = _a.numOfSpansOutOfViewAbove, numOfFilteredSpansAbove = _a.numOfFilteredSpansAbove;
        var infoMessage = this.generateInfoMessage({
            isCurrentSpanHidden: false,
            numOfSpansOutOfViewAbove: numOfSpansOutOfViewAbove,
            isCurrentSpanFilteredOut: false,
            numOfFilteredSpansAbove: numOfFilteredSpansAbove,
        });
        var limitExceededMessage = this.generateLimitExceededMessage();
        return (<TraceViewContainer ref={this.props.traceViewRef}>
        {spanTree}
        {infoMessage}
        {limitExceededMessage}
      </TraceViewContainer>);
    };
    return SpanTree;
}(React.Component));
var TraceViewContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
/**
 * Checks if a trace contains all of its spans.
 *
 * The heuristic used here favors false negatives over false positives.
 * This is because showing a warning that the trace is not showing all
 * spans when it has them all is more misleading than not showing a
 * warning when it is missing some spans.
 *
 * A simple heuristic to determine when there are unrecorded spans
 *
 * 1. We assume if there are less than 999 spans, then we have all
 *    the spans for a transaction. 999 was chosen because most SDKs
 *    have a default limit of 1000 spans per transaction, but the
 *    python SDK is 999 for historic reasons.
 *
 * 2. We assume that if there are unrecorded spans, they should be
 *    at least 100ms in duration.
 *
 * While not perfect, this simple heuristic is unlikely to report
 * false positives.
 */
function hasAllSpans(trace) {
    var traceEndTimestamp = trace.traceEndTimestamp, spans = trace.spans;
    if (spans.length < 999) {
        return true;
    }
    var lastSpan = spans.reduce(function (latest, span) {
        return latest.timestamp > span.timestamp ? latest : span;
    });
    var missingDuration = traceEndTimestamp - lastSpan.timestamp;
    return missingDuration < 0.1;
}
export default SpanTree;
var templateObject_1;
//# sourceMappingURL=spanTree.jsx.map