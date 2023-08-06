import { __awaiter, __extends, __generator, __makeTemplateObject, __values } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import isEqual from 'lodash/isEqual';
import uniqWith from 'lodash/uniqWith';
import Button from 'app/components/button';
import EventErrorItem from 'app/components/events/errorItem';
import { IconWarning } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { BannerContainer, BannerSummary } from './styles';
var MAX_ERRORS = 100;
var EventErrors = /** @class */ (function (_super) {
    __extends(EventErrors, _super);
    function EventErrors() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.toggle = function () {
            _this.setState(function (state) { return ({ isOpen: !state.isOpen }); });
        };
        _this.uniqueErrors = function (errors) { return uniqWith(errors, isEqual); };
        return _this;
    }
    EventErrors.prototype.componentDidMount = function () {
        this.checkSourceCodeErrors();
    };
    EventErrors.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (this.state.isOpen !== nextState.isOpen) {
            return true;
        }
        return this.props.event.id !== nextProps.event.id;
    };
    EventErrors.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.event.id !== prevProps.event.id) {
            this.checkSourceCodeErrors();
        }
    };
    EventErrors.prototype.checkSourceCodeErrors = function () {
        var e_1, _a;
        var event = this.props.event;
        var errors = event.errors;
        var sourceCodeErrors = errors.filter(function (error) { return error.type === 'js_no_source' && error.data.url; });
        if (!sourceCodeErrors.length) {
            return;
        }
        var pathNames = [];
        try {
            for (var sourceCodeErrors_1 = __values(sourceCodeErrors), sourceCodeErrors_1_1 = sourceCodeErrors_1.next(); !sourceCodeErrors_1_1.done; sourceCodeErrors_1_1 = sourceCodeErrors_1.next()) {
                var sourceCodeError = sourceCodeErrors_1_1.value;
                var url = sourceCodeError.data.url;
                if (url) {
                    var pathName = this.getURLPathname(url);
                    if (pathName) {
                        pathNames.push(encodeURIComponent(pathName));
                    }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (sourceCodeErrors_1_1 && !sourceCodeErrors_1_1.done && (_a = sourceCodeErrors_1.return)) _a.call(sourceCodeErrors_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.fetchReleaseArtifacts(pathNames.join('&query='));
    };
    EventErrors.prototype.getURLPathname = function (url) {
        try {
            return new URL(url).pathname;
        }
        catch (_a) {
            return undefined;
        }
    };
    EventErrors.prototype.fetchReleaseArtifacts = function (query) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, orgSlug, event, projectSlug, release, releaseVersion, releaseArtifacts, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgSlug = _a.orgSlug, event = _a.event, projectSlug = _a.projectSlug;
                        release = event.release;
                        releaseVersion = release === null || release === void 0 ? void 0 : release.version;
                        if (!releaseVersion || !query) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/files/?query=" + query, {
                                method: 'GET',
                            })];
                    case 2:
                        releaseArtifacts = _b.sent();
                        this.setState({ releaseArtifacts: releaseArtifacts });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    EventErrors.prototype.render = function () {
        var _this = this;
        var event = this.props.event;
        var _a = this.state, isOpen = _a.isOpen, releaseArtifacts = _a.releaseArtifacts;
        var dist = event.dist;
        // XXX: uniqueErrors is not performant with large datasets
        var errors = event.errors.length > MAX_ERRORS ? event.errors : this.uniqueErrors(event.errors);
        return (<StyledBanner priority="danger">
        <BannerSummary>
          <StyledIconWarning />
          <span>
            {tn('There was %s error encountered while processing this event', 'There were %s errors encountered while processing this event', errors.length)}
          </span>
          <StyledButton data-test-id="event-error-toggle" priority="link" onClick={this.toggle}>
            {isOpen ? t('Hide') : t('Show')}
          </StyledButton>
        </BannerSummary>
        {isOpen && (<ErrorList data-test-id="event-error-details">
            {errors.map(function (error, errorIdx) {
            if (error.type === 'js_no_source' &&
                error.data.url &&
                !!(releaseArtifacts === null || releaseArtifacts === void 0 ? void 0 : releaseArtifacts.length)) {
                var releaseArtifact = releaseArtifacts.find(function (releaseArt) {
                    var pathname = _this.getURLPathname(error.data.url);
                    if (pathname) {
                        return releaseArt.name.includes(pathname);
                    }
                    return false;
                });
                if (releaseArtifact && !releaseArtifact.dist) {
                    error.message = t('Source code was not found because the distribution did not match');
                    error.data['expected-distribution'] = dist;
                    error.data['current-distribution'] = t('none');
                }
            }
            return <EventErrorItem key={errorIdx} error={error}/>;
        })}
          </ErrorList>)}
      </StyledBanner>);
    };
    return EventErrors;
}(React.Component));
var linkStyle = function (_a) {
    var theme = _a.theme;
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  font-weight: bold;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), theme.subText, theme.textColor);
};
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), linkStyle);
var StyledBanner = styled(BannerContainer)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"], ["\n  margin-top: -1px;\n  a {\n    ", "\n  }\n"])), linkStyle);
var StyledIconWarning = styled(IconWarning)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.red300; });
// TODO(theme) don't use a custom pink
var customPink = '#e7c0bc';
var ErrorList = styled('ul')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin: 0 ", " 0 ", ";\n  padding: ", " 0 ", " ", ";\n\n  li {\n    margin-bottom: ", ";\n    word-break: break-word;\n  }\n\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  margin: 0 ", " 0 ", ";\n  padding: ", " 0 ", " ", ";\n\n  li {\n    margin-bottom: ", ";\n    word-break: break-word;\n  }\n\n  pre {\n    background: #f9eded;\n    color: #381618;\n    margin: ", " 0 0;\n  }\n"])), customPink, space(3), space(4), space(1), space(0.5), space(4), space(0.75), space(0.5));
export default withApi(EventErrors);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=errors.jsx.map