import { __extends } from "tslib";
import React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import CrashActions from 'app/components/events/interfaces/crashHeader/crashActions';
import CrashTitle from 'app/components/events/interfaces/crashHeader/crashTitle';
import { isStacktraceNewestFirst } from 'app/components/events/interfaces/stacktrace';
import { t } from 'app/locale';
import { STACK_TYPE, STACK_VIEW } from 'app/types/stacktrace';
import { defined } from 'app/utils';
import getThreadException from './threadSelector/getThreadException';
import getThreadStacktrace from './threadSelector/getThreadStacktrace';
import Content from './content';
import ThreadSelector from './threadSelector';
var defaultProps = {
    hideGuide: false,
};
function getIntendedStackView(thread, event) {
    var stacktrace = getThreadStacktrace(thread, event, false);
    return stacktrace && stacktrace.hasSystemFrames ? STACK_VIEW.APP : STACK_VIEW.FULL;
}
function findBestThread(threads) {
    // Search the entire threads list for a crashed thread with stack
    // trace.
    return (threads.find(function (thread) { return thread.crashed; }) ||
        threads.find(function (thread) { return thread.stacktrace; }) ||
        threads[0]);
}
var Threads = /** @class */ (function (_super) {
    __extends(Threads, _super);
    function Threads() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleSelectNewThread = function (thread) {
            _this.setState(function (prevState) { return ({
                activeThread: thread,
                stackView: prevState.stackView !== STACK_VIEW.RAW
                    ? getIntendedStackView(thread, _this.props.event)
                    : prevState.stackView,
                stackType: STACK_TYPE.ORIGINAL,
            }); });
        };
        _this.handleChangeNewestFirst = function (_a) {
            var newestFirst = _a.newestFirst;
            _this.setState({ newestFirst: newestFirst });
        };
        _this.handleChangeStackView = function (_a) {
            var stackView = _a.stackView, stackType = _a.stackType;
            _this.setState(function (prevState) { return ({
                stackView: stackView !== null && stackView !== void 0 ? stackView : prevState.stackView,
                stackType: stackType !== null && stackType !== void 0 ? stackType : prevState.stackType,
            }); });
        };
        return _this;
    }
    Threads.prototype.getInitialState = function () {
        var _a = this.props, data = _a.data, event = _a.event;
        var thread = defined(data.values) ? findBestThread(data.values) : undefined;
        return {
            activeThread: thread,
            stackView: thread ? getIntendedStackView(thread, event) : undefined,
            stackType: STACK_TYPE.ORIGINAL,
            newestFirst: isStacktraceNewestFirst(),
        };
    };
    Threads.prototype.render = function () {
        var _a = this.props, data = _a.data, event = _a.event, projectId = _a.projectId, hideGuide = _a.hideGuide, type = _a.type;
        if (!data.values) {
            return null;
        }
        var threads = data.values;
        var _b = this.state, stackView = _b.stackView, stackType = _b.stackType, newestFirst = _b.newestFirst, activeThread = _b.activeThread;
        var exception = getThreadException(activeThread, event);
        var stacktrace = getThreadStacktrace(activeThread, event, stackType !== STACK_TYPE.ORIGINAL);
        var hasMoreThanOneThread = threads.length > 1;
        return (<EventDataSection type={type} title={hasMoreThanOneThread ? (<CrashTitle title="" newestFirst={newestFirst} hideGuide={hideGuide} onChange={this.handleChangeNewestFirst} beforeTitle={<ThreadSelector threads={threads} activeThread={activeThread} event={event} onChange={this.handleSelectNewThread}/>}/>) : (<CrashTitle title={t('Stack Trace')} newestFirst={newestFirst} hideGuide={hideGuide} onChange={this.handleChangeNewestFirst}/>)} actions={<CrashActions stackView={stackView} platform={event.platform} stacktrace={stacktrace} stackType={stackType} thread={hasMoreThanOneThread ? activeThread : undefined} exception={hasMoreThanOneThread ? exception : undefined} onChange={this.handleChangeStackView}/>} showPermalink={!hasMoreThanOneThread} wrapTitle={false}>
        <Content data={activeThread} exception={exception} stackView={stackView} stackType={stackType} stacktrace={stacktrace} event={event} newestFirst={newestFirst} projectId={projectId}/>
      </EventDataSection>);
    };
    Threads.defaultProps = defaultProps;
    return Threads;
}(React.Component));
export default Threads;
//# sourceMappingURL=index.jsx.map