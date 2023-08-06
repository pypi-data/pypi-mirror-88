import { __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { API_ACCESS_SCOPES } from 'app/constants';
import { t } from 'app/locale';
import recreateRoute from 'app/utils/recreateRoute';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import ApiForm from 'app/views/settings/components/forms/apiForm';
import MultipleCheckbox from 'app/views/settings/components/forms/controls/multipleCheckbox';
import FormField from 'app/views/settings/components/forms/formField';
import TextareaField from 'app/views/settings/components/forms/textareaField';
import TextField from 'app/views/settings/components/forms/textField';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
var API_CHOICES = API_ACCESS_SCOPES.map(function (s) { return [s, s]; });
var OrganizationApiKeyDetails = /** @class */ (function (_super) {
    __extends(OrganizationApiKeyDetails, _super);
    function OrganizationApiKeyDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            addSuccessMessage('Saved changes');
            // Go back to API list
            browserHistory.push(recreateRoute('', {
                stepBack: -1,
                routes: _this.props.routes,
                params: _this.props.params,
            }));
        };
        _this.handleSubmitError = function () {
            addErrorMessage('Unable to save changes. Please try again.');
        };
        return _this;
    }
    OrganizationApiKeyDetails.prototype.getEndpoints = function () {
        return [
            [
                'apiKey',
                "/organizations/" + this.props.params.orgId + "/api-keys/" + this.props.params.apiKey + "/",
            ],
        ];
    };
    OrganizationApiKeyDetails.prototype.getTitle = function () {
        return routeTitleGen(t('Edit API Key'), this.props.organization.slug, false);
    };
    OrganizationApiKeyDetails.prototype.renderBody = function () {
        var _this = this;
        return (<div>
        <SettingsPageHeader title={t('Edit Api Key')}/>

        <Panel>
          <PanelHeader>{t('API Key')}</PanelHeader>
          <ApiForm apiMethod="PUT" apiEndpoint={"/organizations/" + this.props.params.orgId + "/api-keys/" + this.props.params.apiKey + "/"} initialData={this.state.apiKey} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onCancel={function () {
            return browserHistory.push(recreateRoute('', {
                stepBack: -1,
                routes: _this.props.routes,
                params: _this.props.params,
            }));
        }}>
            <PanelBody>
              <TextField label={t('Label')} name="label"/>
              <TextField label={t('API Key')} name="key" disabled/>

              <FormField name="scope_list" label={t('Scopes')} inline={false} required>
                {function (_a) {
            var value = _a.value, onChange = _a.onChange;
            return (<MultipleCheckbox value={value} onChange={onChange} choices={API_CHOICES}/>);
        }}
              </FormField>

              <TextareaField label={t('Allowed Domains')} name="allowed_origins" placeholder="e.g. example.com or https://example.com" help="Separate multiple entries with a newline"/>
            </PanelBody>
          </ApiForm>
        </Panel>
      </div>);
    };
    return OrganizationApiKeyDetails;
}(AsyncView));
export default withOrganization(OrganizationApiKeyDetails);
//# sourceMappingURL=organizationApiKeyDetails.jsx.map