import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon, trackIntegrationEvent } from 'app/utils/integrationUtil';
import InputField from 'app/views/settings/components/forms/inputField';
var StacktraceLinkModal = /** @class */ (function (_super) {
    __extends(StacktraceLinkModal, _super);
    function StacktraceLinkModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function () { return __awaiter(_this, void 0, void 0, function () {
            var sourceCodeInput, _a, organization, filename, project, parsingEndpoint, configData, configEndpoint, err_1, errors, apiErrors;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        sourceCodeInput = this.state.sourceCodeInput;
                        _a = this.props, organization = _a.organization, filename = _a.filename, project = _a.project;
                        trackIntegrationEvent({
                            eventKey: 'integrations.stacktrace_automatic_setup',
                            eventName: 'Integrations: Stacktrace Automatic Setup',
                            view: 'stacktrace_issue_details',
                        }, this.props.organization, { startSession: true });
                        parsingEndpoint = "/projects/" + organization.slug + "/" + project.slug + "/repo-path-parsing/";
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 4, , 5]);
                        return [4 /*yield*/, this.api.requestPromise(parsingEndpoint, {
                                method: 'POST',
                                data: {
                                    sourceUrl: sourceCodeInput,
                                    stackPath: filename,
                                },
                            })];
                    case 2:
                        configData = _b.sent();
                        configEndpoint = "/organizations/" + organization.slug + "/integrations/" + configData.integrationId + "/repo-project-path-configs/";
                        return [4 /*yield*/, this.api.requestPromise(configEndpoint, {
                                method: 'POST',
                                data: __assign(__assign({}, configData), { projectId: project.id }),
                            })];
                    case 3:
                        _b.sent();
                        addSuccessMessage(t('Stack trace configuration saved.'));
                        this.props.closeModal();
                        this.props.onSubmit();
                        return [3 /*break*/, 5];
                    case 4:
                        err_1 = _b.sent();
                        errors = (err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) ? Array.isArray(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            ? err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON : Object.values(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            : [];
                        apiErrors = errors.length > 0 ? ": " + errors.join(', ') : '';
                        addErrorMessage(t('Something went wrong%s', apiErrors));
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    StacktraceLinkModal.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { sourceCodeInput: '' });
    };
    StacktraceLinkModal.prototype.onHandleChange = function (sourceCodeInput) {
        this.setState({
            sourceCodeInput: sourceCodeInput,
        });
    };
    StacktraceLinkModal.prototype.onManualSetup = function (provider) {
        trackIntegrationEvent({
            eventKey: 'integrations.stacktrace_manual_setup',
            eventName: 'Integrations: Stacktrace Manual Setup',
            view: 'stacktrace_issue_details',
            provider: provider,
        }, this.props.organization, { startSession: true });
    };
    StacktraceLinkModal.prototype.renderBody = function () {
        var _this = this;
        var sourceCodeInput = this.state.sourceCodeInput;
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, filename = _a.filename, integrations = _a.integrations, organization = _a.organization;
        var baseUrl = "/settings/" + organization.slug + "/integrations";
        return (<React.Fragment>
        <Header closeButton>{t('Link Stack Trace To Source Code')}</Header>
        <Body>
          <ModalContainer>
            <div>
              <h6>{t('Automatic Setup')}</h6>
              {tct('Enter the source code URL corresponding to stack trace filename [filename] so we can automatically set up stack trace linking for this project.', {
            filename: <code>{filename}</code>,
        })}
            </div>
            <SourceCodeInput>
              <StyledInputField inline={false} flexibleControlStateSize stacked name="source-code-input" type="text" value={sourceCodeInput} onChange={function (val) { return _this.onHandleChange(val); }} placeholder={t("https://github.com/helloworld/Hello-World/blob/master/" + filename)}/>
              <ButtonBar>
                <Button data-test-id="quick-setup-button" type="button" onClick={function () { return _this.handleSubmit(); }}>
                  {t('Submit')}
                </Button>
              </ButtonBar>
            </SourceCodeInput>
            <div>
              <h6>{t('Manual Setup')}</h6>
              <Alert type="warning">
                {t('We recommend this for more complicated configurations, like projects with multiple repositories.')}
              </Alert>
              {t("To manually configure stack trace linking, select the integration you'd like to use for mapping:")}
            </div>
            <ManualSetup>
              {integrations.map(function (integration) { return (<Button key={integration.id} type="button" onClick={function () { return _this.onManualSetup(integration.provider.key); }} to={baseUrl + "/" + integration.provider.key + "/" + integration.id + "/?tab=codeMappings"}>
                  {getIntegrationIcon(integration.provider.key)}
                  <IntegrationName>{integration.name}</IntegrationName>
                </Button>); })}
            </ManualSetup>
          </ModalContainer>
        </Body>
        <Footer>
          <Alert type="info" icon={<IconInfo />}>
            {tct('Stack trace linking is in Beta. Got feedback? Email [email:ecosystem-feedback@sentry.io].', { email: <a href="mailto:ecosystem-feedback@sentry.io"/> })}
          </Alert>
        </Footer>
      </React.Fragment>);
    };
    return StacktraceLinkModal;
}(AsyncComponent));
export default StacktraceLinkModal;
var SourceCodeInput = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"])), space(1));
var ManualSetup = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"])), space(1));
var ModalContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"])), space(3));
var StyledInputField = styled(InputField)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 0px;\n"], ["\n  padding: 0px;\n"])));
var IntegrationName = styled('p')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-left: 10px;\n"], ["\n  padding-left: 10px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=stacktraceLinkModal.jsx.map