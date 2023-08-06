import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isArray from 'lodash/isArray';
import isNumber from 'lodash/isNumber';
import isString from 'lodash/isString';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import ExternalLink from 'app/components/links/externalLink';
import { IconAdd, IconOpen, IconSubtract } from 'app/icons';
import { isUrl } from 'app/utils';
function looksLikeObjectRepr(value) {
    var a = value[0];
    var z = value[value.length - 1];
    if (a === '<' && z === '>') {
        return true;
    }
    else if (a === '[' && z === ']') {
        return true;
    }
    else if (a === '(' && z === ')') {
        return true;
    }
    else if (z === ')' && value.match(/^[\w\d._-]+\(/)) {
        return true;
    }
    return false;
}
function looksLikeMultiLineString(value) {
    return !!value.match(/[\r\n]/);
}
function padNumbersInString(string) {
    return string.replace(/(\d+)/g, function (num) {
        var isNegative = false;
        var realNum = parseInt(num, 10);
        if (realNum < 0) {
            realNum *= -1;
            isNegative = true;
        }
        var s = '0000000000000' + realNum;
        s = s.substr(s.length - (isNegative ? 11 : 12));
        if (isNegative) {
            s = '-' + s;
        }
        return s;
    });
}
function naturalCaseInsensitiveSort(a, b) {
    a = padNumbersInString(a).toLowerCase();
    b = padNumbersInString(b).toLowerCase();
    return a === b ? 0 : a < b ? -1 : 1;
}
function analyzeStringForRepr(value) {
    var rv = {
        repr: value,
        isString: true,
        isMultiLine: false,
        isStripped: false,
    };
    // stripped for security reasons
    if (value.match(/^['"]?\*{8,}['"]?$/)) {
        rv.isStripped = true;
        return rv;
    }
    if (looksLikeObjectRepr(value)) {
        rv.isString = false;
    }
    else {
        rv.isMultiLine = looksLikeMultiLineString(value);
    }
    return rv;
}
var ToggleWrap = /** @class */ (function (_super) {
    __extends(ToggleWrap, _super);
    function ToggleWrap() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { toggled: false };
        return _this;
    }
    ToggleWrap.prototype.render = function () {
        var _this = this;
        if (React.Children.count(this.props.children) === 0) {
            return null;
        }
        var _a = this.props, wrapClassName = _a.wrapClassName, children = _a.children;
        var wrappedChildren = <span className={wrapClassName}>{children}</span>;
        if (this.props.highUp) {
            return wrappedChildren;
        }
        return (<span>
        <ToggleIcon isOpen={this.state.toggled} href="#" onClick={function (evt) {
            _this.setState(function (state) { return ({ toggled: !state.toggled }); });
            evt.preventDefault();
        }}>
          {this.state.toggled ? (<IconSubtract size="9px" color="white"/>) : (<IconAdd size="9px" color="white"/>)}
        </ToggleIcon>
        {this.state.toggled && wrappedChildren}
      </span>);
    };
    return ToggleWrap;
}(React.Component));
var ContextData = /** @class */ (function (_super) {
    __extends(ContextData, _super);
    function ContextData() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ContextData.prototype.renderValue = function (value) {
        var _a = this.props, preserveQuotes = _a.preserveQuotes, meta = _a.meta, withAnnotatedText = _a.withAnnotatedText, jsonConsts = _a.jsonConsts, maxDefaultDepth = _a.maxDefaultDepth;
        var maxDepth = maxDefaultDepth !== null && maxDefaultDepth !== void 0 ? maxDefaultDepth : 2;
        function getValueWithAnnotatedText(v, meta) {
            return <AnnotatedText value={v} meta={meta}/>;
        }
        /*eslint no-shadow:0*/
        function walk(value, depth) {
            var i = 0;
            var children = [];
            if (value === null) {
                return <span className="val-null">{jsonConsts ? 'null' : 'None'}</span>;
            }
            if (value === true || value === false) {
                return (<span className="val-bool">
            {jsonConsts ? (value ? 'true' : 'false') : value ? 'True' : 'False'}
          </span>);
            }
            if (isString(value)) {
                var valueInfo = analyzeStringForRepr(value);
                var valueToBeReturned = withAnnotatedText
                    ? getValueWithAnnotatedText(valueInfo.repr, meta)
                    : valueInfo.repr;
                var out = [
                    <span key="value" className={(valueInfo.isString ? 'val-string' : '') +
                        (valueInfo.isStripped ? ' val-stripped' : '') +
                        (valueInfo.isMultiLine ? ' val-string-multiline' : '')}>
            {preserveQuotes ? "\"" + valueToBeReturned + "\"" : valueToBeReturned}
          </span>,
                ];
                if (valueInfo.isString && isUrl(value)) {
                    out.push(<ExternalLink key="external" href={value} className="external-icon">
              <StyledIconOpen size="xs"/>
            </ExternalLink>);
                }
                return out;
            }
            if (isNumber(value)) {
                var valueToBeReturned = withAnnotatedText && meta ? getValueWithAnnotatedText(value, meta) : value;
                return <span>{valueToBeReturned}</span>;
            }
            if (isArray(value)) {
                for (i = 0; i < value.length; i++) {
                    children.push(<span className="val-array-item" key={i}>
              {walk(value[i], depth + 1)}
              {i < value.length - 1 ? (<span className="val-array-sep">{', '}</span>) : null}
            </span>);
                }
                return (<span className="val-array">
            <span className="val-array-marker">{'['}</span>
            <ToggleWrap highUp={depth <= maxDepth} wrapClassName="val-array-items">
              {children}
            </ToggleWrap>
            <span className="val-array-marker">{']'}</span>
          </span>);
            }
            if (React.isValidElement(value)) {
                return value;
            }
            var keys = Object.keys(value);
            keys.sort(naturalCaseInsensitiveSort);
            for (i = 0; i < keys.length; i++) {
                var key = keys[i];
                children.push(<span className="val-dict-pair" key={key}>
            <span className="val-dict-key">
              <span className="val-string">{preserveQuotes ? "\"" + key + "\"" : key}</span>
            </span>
            <span className="val-dict-col">{': '}</span>
            <span className="val-dict-value">
              {walk(value[key], depth + 1)}
              {i < keys.length - 1 ? <span className="val-dict-sep">{', '}</span> : null}
            </span>
          </span>);
            }
            return (<span className="val-dict">
          <span className="val-dict-marker">{'{'}</span>
          <ToggleWrap highUp={depth <= maxDepth - 1} wrapClassName="val-dict-items">
            {children}
          </ToggleWrap>
          <span className="val-dict-marker">{'}'}</span>
        </span>);
        }
        return walk(value, 0);
    };
    ContextData.prototype.render = function () {
        var _a = this.props, data = _a.data, _preserveQuotes = _a.preserveQuotes, _withAnnotatedText = _a.withAnnotatedText, _meta = _a.meta, children = _a.children, other = __rest(_a, ["data", "preserveQuotes", "withAnnotatedText", "meta", "children"]);
        return (<ContextValues {...other}>
        {this.renderValue(data)}
        {children}
      </ContextValues>);
    };
    ContextData.defaultProps = {
        data: null,
        withAnnotatedText: false,
    };
    return ContextData;
}(React.Component));
var StyledIconOpen = styled(IconOpen)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var ToggleIcon = styled('a')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  top: 1px;\n  height: 11px;\n  width: 11px;\n  line-height: 1;\n  padding-left: 1px;\n  margin-left: 1px;\n  border-radius: 2px;\n\n  background: ", ";\n  &:hover {\n    background: ", ";\n  }\n"], ["\n  display: inline-block;\n  position: relative;\n  top: 1px;\n  height: 11px;\n  width: 11px;\n  line-height: 1;\n  padding-left: 1px;\n  margin-left: 1px;\n  border-radius: 2px;\n\n  background: ", ";\n  &:hover {\n    background: ", ";\n  }\n"])), function (p) { return (p.isOpen ? p.theme.gray300 : p.theme.blue300); }, function (p) { return (p.isOpen ? p.theme.gray400 : p.theme.blue200); });
var ContextValues = styled('pre')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Not using theme to be consistent with less files */\n  color: #4e3fb4;\n"], ["\n  /* Not using theme to be consistent with less files */\n  color: #4e3fb4;\n"])));
export default ContextData;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=contextData.jsx.map