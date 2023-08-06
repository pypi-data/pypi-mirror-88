import { __assign, __extends, __values } from "tslib";
import React from 'react';
import getDisplayName from 'app/utils/getDisplayName';
import { clamp, rectOfContent, setBodyUserSelect, toPercent, } from './utils';
var ScrollbarManagerContext = React.createContext({
    generateScrollableSpanBarRef: function () { return function () { return undefined; }; },
    generateContentSpanBarRef: function () { return function () { return undefined; }; },
    virtualScrollbarRef: React.createRef(),
    onDragStart: function () { },
    updateScrollState: function () { },
});
var selectRefs = function (refs, transform) {
    if (!(refs instanceof Set)) {
        if (refs.current) {
            transform(refs.current);
        }
        return;
    }
    refs.forEach(function (element) {
        if (document.body.contains(element)) {
            transform(element);
        }
    });
};
// simple linear interpolation between start and end such that needle is between [0, 1]
var lerp = function (start, end, needle) {
    return start + needle * (end - start);
};
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            maxContentWidth: undefined,
        };
        _this.scrollableSpanBar = new Set();
        _this.contentSpanBar = new Set();
        _this.virtualScrollbar = React.createRef();
        _this.isDragging = false;
        _this.previousUserSelect = null;
        _this.initializeScrollState = function () {
            if (_this.scrollableSpanBar.size === 0 || _this.contentSpanBar.size === 0) {
                return;
            }
            // set initial scroll state for all scrollable spanbars
            selectRefs(_this.scrollableSpanBar, function (spanBarDOM) {
                spanBarDOM.scrollLeft = 0;
            });
            // reset all span bar content containers to their natural widths
            selectRefs(_this.contentSpanBar, function (spanBarDOM) {
                spanBarDOM.style.removeProperty('width');
                spanBarDOM.style.removeProperty('max-width');
                spanBarDOM.style.removeProperty('overflow');
            });
            // Find the maximum content width. We set each content spanbar to be this maximum width,
            // such that all content spanbar widths are uniform.
            var maxContentWidth = Array.from(_this.scrollableSpanBar).reduce(function (currentMaxWidth, currentSpanBar) {
                var isHidden = currentSpanBar.offsetParent === null;
                if (!document.body.contains(currentSpanBar) || isHidden) {
                    return currentMaxWidth;
                }
                var maybeMaxWidth = currentSpanBar.scrollWidth;
                if (maybeMaxWidth > currentMaxWidth) {
                    return maybeMaxWidth;
                }
                return currentMaxWidth;
            }, 0);
            selectRefs(_this.contentSpanBar, function (spanBarDOM) {
                spanBarDOM.style.width = maxContentWidth + "px";
                spanBarDOM.style.maxWidth = maxContentWidth + "px";
                spanBarDOM.style.overflow = 'hidden';
            });
            _this.scrollableSpanBar.forEach(function (currentSpanBarRef) {
                _this.unregisterEventListeners(currentSpanBarRef);
            });
            var spanBarDOM = _this.getReferenceSpanBar();
            if (spanBarDOM) {
                _this.syncVirtualScrollbar(spanBarDOM);
            }
            _this.scrollableSpanBar.forEach(function (currentSpanBarRef) {
                _this.registerEventListeners(currentSpanBarRef);
            });
        };
        _this.registerEventListeners = function (spanbar) {
            spanbar.onscroll = _this.handleScroll.bind(_this, spanbar);
        };
        _this.unregisterEventListeners = function (spanbar) {
            spanbar.onscroll = null;
        };
        _this.handleScroll = function (spanbar) {
            window.requestAnimationFrame(function () {
                _this.syncScrollPositions(spanbar);
            });
        };
        _this.syncScrollPositions = function (scrolledSpanBar) {
            // Sync scroll positions of all span bars with respect to scrolledSpanBar's
            // scroll position
            selectRefs(_this.scrollableSpanBar, function (spanBarDOM) {
                if (scrolledSpanBar === spanBarDOM) {
                    // Don't sync scrolledSpanBar's scroll position with itself
                    return;
                }
                _this.unregisterEventListeners(spanBarDOM);
                _this.syncScrollPosition(scrolledSpanBar, spanBarDOM);
                _this.syncVirtualScrollbar(scrolledSpanBar);
                window.requestAnimationFrame(function () {
                    _this.registerEventListeners(spanBarDOM);
                });
            });
        };
        _this.syncScrollPosition = function (scrolledSpanBar, spanBarDOM) {
            // sync spanBarDOM's scroll position with respect to scrolledSpanBar's
            // scroll position
            var scrollLeft = scrolledSpanBar.scrollLeft, scrollWidth = scrolledSpanBar.scrollWidth, clientWidth = scrolledSpanBar.clientWidth;
            var scrollLeftOffset = scrollWidth - clientWidth;
            if (scrollLeftOffset > 0) {
                spanBarDOM.scrollLeft = scrollLeft;
            }
        };
        _this.syncVirtualScrollbar = function (scrolledSpanBar) {
            // sync the virtual scrollbar's scroll position with respect to scrolledSpanBar's
            // scroll position
            if (!_this.virtualScrollbar.current || !_this.hasInteractiveLayer()) {
                return;
            }
            var virtualScrollbarDOM = _this.virtualScrollbar.current;
            var maxContentWidth = scrolledSpanBar.scrollWidth;
            if (maxContentWidth === undefined || maxContentWidth <= 0) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            var visibleWidth = scrolledSpanBar.getBoundingClientRect().width;
            // This is the scroll width of the content not visible on the screen due to overflow.
            var maxScrollDistance = scrolledSpanBar.scrollWidth - scrolledSpanBar.clientWidth;
            var virtualScrollbarWidth = visibleWidth / (visibleWidth + maxScrollDistance);
            if (virtualScrollbarWidth >= 1) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            virtualScrollbarDOM.style.width = "max(50px, " + toPercent(virtualScrollbarWidth) + ")";
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            var virtualScrollBarRect = rectOfContent(virtualScrollbarDOM);
            var maxVirtualScrollableArea = 1 - virtualScrollBarRect.width / rect.width;
            // Assume scrollbarLeftOffset = lerp(0, maxScrollDistance, virtualScrollPercentage).
            // Then solve for virtualScrollPercentage.
            var virtualScrollPercentage = clamp(scrolledSpanBar.scrollLeft / maxScrollDistance, 0, 1);
            var virtualScrollbarPosition = virtualScrollPercentage * maxVirtualScrollableArea;
            virtualScrollbarDOM.style.left = "clamp(0%, calc(" + toPercent(virtualScrollbarPosition) + "), calc(100% - max(50px, " + toPercent(virtualScrollbarWidth) + ")))";
        };
        _this.generateScrollableSpanBarRef = function () {
            var previousInstance = null;
            var addScrollableSpanBarRef = function (instance) {
                if (previousInstance) {
                    _this.scrollableSpanBar.delete(previousInstance);
                    previousInstance = null;
                }
                if (instance) {
                    _this.scrollableSpanBar.add(instance);
                    previousInstance = instance;
                }
            };
            return addScrollableSpanBarRef;
        };
        _this.generateContentSpanBarRef = function () {
            var previousInstance = null;
            var addContentSpanBarRef = function (instance) {
                if (previousInstance) {
                    _this.contentSpanBar.delete(previousInstance);
                    previousInstance = null;
                }
                if (instance) {
                    _this.contentSpanBar.add(instance);
                    previousInstance = instance;
                }
            };
            return addContentSpanBarRef;
        };
        _this.hasInteractiveLayer = function () { return !!_this.props.interactiveLayerRef.current; };
        _this.initialMouseClickX = undefined;
        _this.onDragStart = function (event) {
            if (_this.isDragging ||
                event.type !== 'mousedown' ||
                !_this.hasInteractiveLayer() ||
                !_this.virtualScrollbar.current) {
                return;
            }
            event.stopPropagation();
            var virtualScrollbarRect = rectOfContent(_this.virtualScrollbar.current);
            // get intitial x-coordinate of the mouse click on the virtual scrollbar
            _this.initialMouseClickX = Math.abs(event.clientX - virtualScrollbarRect.x);
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor inside the minimap
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor does not select text during a drag
            window.addEventListener('mousemove', _this.onDragMove);
            window.addEventListener('mouseup', _this.onDragEnd);
            // indicate drag has begun
            _this.isDragging = true;
            selectRefs(_this.virtualScrollbar, function (dividerDOM) {
                dividerDOM.classList.add('dragging');
            });
        };
        _this.onDragMove = function (event) {
            if (!_this.isDragging ||
                event.type !== 'mousemove' ||
                !_this.hasInteractiveLayer() ||
                !_this.virtualScrollbar.current ||
                _this.initialMouseClickX === undefined) {
                return;
            }
            var virtualScrollbarDOM = _this.virtualScrollbar.current;
            var rect = rectOfContent(_this.props.interactiveLayerRef.current);
            var virtualScrollBarRect = rectOfContent(virtualScrollbarDOM);
            // Mouse x-coordinate relative to the interactive layer's left side
            var localDragX = event.pageX - rect.x;
            // The drag movement with respect to the interactive layer's width.
            var rawMouseX = (localDragX - _this.initialMouseClickX) / rect.width;
            var maxVirtualScrollableArea = 1 - virtualScrollBarRect.width / rect.width;
            // clamp rawMouseX to be within [0, 1]
            var virtualScrollbarPosition = clamp(rawMouseX, 0, 1);
            virtualScrollbarDOM.style.left = "clamp(0%, calc(" + toPercent(virtualScrollbarPosition) + "), " + toPercent(maxVirtualScrollableArea) + ")";
            var virtualScrollPercentage = clamp(rawMouseX / maxVirtualScrollableArea, 0, 1);
            // Update scroll positions of all the span bars
            selectRefs(_this.scrollableSpanBar, function (spanBarDOM) {
                _this.unregisterEventListeners(spanBarDOM);
                var maxScrollDistance = spanBarDOM.scrollWidth - spanBarDOM.clientWidth;
                spanBarDOM.scrollLeft = lerp(0, maxScrollDistance, virtualScrollPercentage);
                window.requestAnimationFrame(function () {
                    _this.registerEventListeners(spanBarDOM);
                });
            });
        };
        _this.onDragEnd = function (event) {
            if (!_this.isDragging || event.type !== 'mouseup' || !_this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onDragStart
            _this.cleanUpListeners();
            // restore body styles
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // indicate drag has ended
            _this.isDragging = false;
            selectRefs(_this.virtualScrollbar, function (dividerDOM) {
                dividerDOM.classList.remove('dragging');
            });
        };
        _this.cleanUpListeners = function () {
            if (_this.isDragging) {
                // we only remove listeners during a drag
                window.removeEventListener('mousemove', _this.onDragMove);
                window.removeEventListener('mouseup', _this.onDragEnd);
            }
        };
        return _this;
    }
    Provider.prototype.componentDidMount = function () {
        // React will guarantee that refs are set before componentDidMount() is called;
        // but only for DOM elements that actually got rendered
        this.initializeScrollState();
    };
    Provider.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.dividerPosition !== prevProps.dividerPosition) {
            // Find any span bar and adjust the virtual scroll bar's scroll position
            // with respect to this span bar.
            if (this.scrollableSpanBar.size === 0) {
                return;
            }
            var spanBarDOM = this.getReferenceSpanBar();
            if (spanBarDOM) {
                this.syncVirtualScrollbar(spanBarDOM);
            }
            return;
        }
        // If the window was selected via the minimap, then re-initialize the scroll state.
        var viewWindowChanged = prevProps.dragProps.viewWindowStart !== this.props.dragProps.viewWindowStart ||
            prevProps.dragProps.viewWindowEnd !== this.props.dragProps.viewWindowEnd;
        if (viewWindowChanged) {
            this.initializeScrollState();
        }
    };
    Provider.prototype.componentWillUnmount = function () {
        this.cleanUpListeners();
    };
    Provider.prototype.getReferenceSpanBar = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.scrollableSpanBar), _c = _b.next(); !_c.done; _c = _b.next()) {
                var currentSpanBar = _c.value;
                var isHidden = currentSpanBar.offsetParent === null;
                if (!document.body.contains(currentSpanBar) || isHidden) {
                    continue;
                }
                return currentSpanBar;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return undefined;
    };
    Provider.prototype.render = function () {
        var childrenProps = {
            generateScrollableSpanBarRef: this.generateScrollableSpanBarRef,
            generateContentSpanBarRef: this.generateContentSpanBarRef,
            onDragStart: this.onDragStart,
            virtualScrollbarRef: this.virtualScrollbar,
            updateScrollState: this.initializeScrollState,
        };
        return (<ScrollbarManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </ScrollbarManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = ScrollbarManagerContext.Consumer;
export var withScrollbarManager = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _this = this;
            return (<ScrollbarManagerContext.Consumer>
          {function (context) {
                var props = __assign(__assign({}, _this.props), context);
                return <WrappedComponent {...props}/>;
            }}
        </ScrollbarManagerContext.Consumer>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withScrollbarManager(" + getDisplayName(WrappedComponent) + ")",
    _a; };
//# sourceMappingURL=scrollbarManager.jsx.map