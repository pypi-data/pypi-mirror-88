import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import { t } from 'app/locale';
import { getIntegrationIcon, trackIntegrationEvent } from 'app/utils/integrationUtil';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { OpenInContainer, OpenInLink, OpenInName } from './openInContextLine';
import StacktraceLinkModal from './stacktraceLinkModal';
var StacktraceLink = /** @class */ (function (_super) {
    __extends(StacktraceLink, _super);
    function StacktraceLink() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(StacktraceLink.prototype, "project", {
        get: function () {
            // we can't use the withProject HoC on an the issue page
            // so we ge around that by using the withProjects HoC
            // and look up the project from the list
            var _a = this.props, projects = _a.projects, event = _a.event;
            return projects.find(function (project) { return project.id === event.projectID; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "match", {
        get: function () {
            return this.state.match;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "config", {
        get: function () {
            return this.match.config;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "integrations", {
        get: function () {
            return this.match.integrations;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "errorText", {
        get: function () {
            var error = this.match.error;
            switch (error) {
                case 'stack_root_mismatch':
                    return t('Error matching your configuration, check your stack trace root.');
                case 'file_not_found':
                    return t('Could not find source file, check your repository and source code root.');
                default:
                    return t('There was an error encountered with the code mapping for this project');
            }
        },
        enumerable: false,
        configurable: true
    });
    StacktraceLink.prototype.getEndpoints = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, frame = _c.frame, event = _c.event;
        var project = this.project;
        if (!project) {
            throw new Error('Unable to find project');
        }
        var commitId = (_b = (_a = event.release) === null || _a === void 0 ? void 0 : _a.lastCommit) === null || _b === void 0 ? void 0 : _b.id;
        var platform = event.platform;
        return [
            [
                'match',
                "/projects/" + organization.slug + "/" + project.slug + "/stacktrace-link/",
                { query: { file: frame.filename, platform: platform, commitId: commitId } },
            ],
        ];
    };
    StacktraceLink.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { showModal: false, sourceCodeInput: '', match: { integrations: [] } });
    };
    StacktraceLink.prototype.onOpenLink = function () {
        var _a;
        var provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        if (provider) {
            trackIntegrationEvent({
                eventKey: 'integrations.stacktrace_link_clicked',
                eventName: 'Integrations: Stacktrace Link Clicked',
                view: 'stacktrace_issue_details',
                provider: provider.key,
            }, this.props.organization, { startSession: true });
        }
    };
    StacktraceLink.prototype.onReconfigureMapping = function () {
        var _a;
        var provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        var error = this.match.error;
        if (provider) {
            trackIntegrationEvent({
                eventKey: 'integrations.reconfigure_stacktrace_setup',
                eventName: 'Integrations: Reconfigure Stacktrace Setup',
                view: 'stacktrace_issue_details',
                provider: provider.key,
                error_reason: error,
            }, this.props.organization, { startSession: true });
        }
    };
    StacktraceLink.prototype.handleSubmit = function () {
        this.reloadData();
    };
    // let the ErrorBoundary handle errors by raising it
    StacktraceLink.prototype.renderError = function () {
        throw new Error('Error loading endpoints');
    };
    StacktraceLink.prototype.renderLoading = function () {
        //TODO: Add loading
        return null;
    };
    StacktraceLink.prototype.renderNoMatch = function () {
        var _this = this;
        var organization = this.props.organization;
        var filename = this.props.frame.filename;
        var platform = this.props.event.platform;
        if (this.project && this.integrations.length > 0 && filename) {
            return (<CodeMappingButtonContainer columnQuantity={2}>
          {t('Enable source code stack trace linking by setting up a code mapping.')}
          <Button onClick={function () {
                trackIntegrationEvent({
                    eventKey: 'integrations.stacktrace_start_setup',
                    eventName: 'Integrations: Stacktrace Start Setup',
                    view: 'stacktrace_issue_details',
                    platform: platform,
                }, _this.props.organization, { startSession: true });
                openModal(function (deps) {
                    return _this.project && (<StacktraceLinkModal onSubmit={function () { return _this.handleSubmit(); }} filename={filename} project={_this.project} organization={organization} integrations={_this.integrations} {...deps}/>);
                });
            }} size="xsmall">
            {t('Setup Stack Trace Linking')}
          </Button>
        </CodeMappingButtonContainer>);
        }
        return null;
    };
    StacktraceLink.prototype.renderMatchNoUrl = function () {
        var _this = this;
        var config = this.match.config;
        var organization = this.props.organization;
        var text = this.errorText;
        var url = "/settings/" + organization.slug + "/integrations/" + (config === null || config === void 0 ? void 0 : config.provider.key) + "/" + (config === null || config === void 0 ? void 0 : config.integrationId) + "/?tab=codeMappings";
        return (<CodeMappingButtonContainer columnQuantity={2}>
        {text}
        <Button onClick={function () { return _this.onReconfigureMapping(); }} to={url} size="xsmall">
          {t('Configure Stack Trace Linking')}
        </Button>
      </CodeMappingButtonContainer>);
    };
    StacktraceLink.prototype.renderMatchWithUrl = function (config, url) {
        var _this = this;
        url = url + "#L" + this.props.frame.lineNo;
        return (<OpenInContainer columnQuantity={2}>
        <div>{t('Open this line in')}</div>
        <OpenInLink onClick={function () { return _this.onOpenLink(); }} href={url} openInNewTab>
          {getIntegrationIcon(config.provider.key)}
          <OpenInName>{config.provider.name}</OpenInName>
        </OpenInLink>
      </OpenInContainer>);
    };
    StacktraceLink.prototype.renderBody = function () {
        var _a = this.match || {}, config = _a.config, sourceUrl = _a.sourceUrl;
        if (config && sourceUrl) {
            return this.renderMatchWithUrl(config, sourceUrl);
        }
        if (config) {
            return this.renderMatchNoUrl();
        }
        return this.renderNoMatch();
    };
    return StacktraceLink;
}(AsyncComponent));
export default withProjects(withOrganization(StacktraceLink));
export { StacktraceLink };
export var CodeMappingButtonContainer = styled(OpenInContainer)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: space-between;\n"], ["\n  justify-content: space-between;\n"])));
var templateObject_1;
//# sourceMappingURL=stacktraceLink.jsx.map