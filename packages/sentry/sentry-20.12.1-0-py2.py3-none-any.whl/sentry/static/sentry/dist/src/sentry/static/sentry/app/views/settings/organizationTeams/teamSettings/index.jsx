import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { removeTeam, updateTeamSuccess } from 'app/actionCreators/teams';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { Panel, PanelHeader } from 'app/components/panels';
import teamSettingsFields from 'app/data/forms/teamSettingsFields';
import { IconDelete } from 'app/icons';
import { t, tct } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import AsyncView from 'app/views/asyncView';
import Field from 'app/views/settings/components/forms/field';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import TeamModel from './model';
var TeamSettings = /** @class */ (function (_super) {
    __extends(TeamSettings, _super);
    function TeamSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new TeamModel(_this.props.params.orgId, _this.props.params.teamId);
        _this.handleSubmitSuccess = function (resp, model, id) {
            updateTeamSuccess(resp.slug, resp);
            if (id === 'slug') {
                addSuccessMessage(t('Team name changed'));
                _this.props.router.replace("/settings/" + _this.props.params.orgId + "/teams/" + model.getValue(id) + "/settings/");
                _this.setState({ loading: true });
            }
        };
        _this.handleRemoveTeam = function () { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, removeTeam(this.api, this.props.params)];
                    case 1:
                        _a.sent();
                        this.props.router.replace("/settings/" + this.props.params.orgId + "/teams/");
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    TeamSettings.prototype.getTitle = function () {
        return 'Team Settings';
    };
    TeamSettings.prototype.getEndpoints = function () {
        return [];
    };
    TeamSettings.prototype.renderBody = function () {
        var _a = this.context, location = _a.location, organization = _a.organization;
        var team = this.props.team;
        var access = new Set(organization.access);
        return (<React.Fragment>
        <Form model={this.model} apiMethod="PUT" saveOnBlur allowUndo onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={function () { return addErrorMessage(t('Unable to save change')); }} initialData={{
            name: team.name,
            slug: team.slug,
        }}>
          <JsonForm access={access} location={location} forms={teamSettingsFields}/>
        </Form>

        <Panel>
          <PanelHeader>{t('Remove Team')}</PanelHeader>
          <Field help={t("This may affect team members' access to projects and associated alert delivery.")}>
            <div>
              <Confirm disabled={!access.has('team:admin')} onConfirm={this.handleRemoveTeam} priority="danger" message={tct('Are you sure you want to remove the team [team]?', {
            team: "#" + team.slug,
        })}>
                <Button icon={<IconDelete />} priority="danger" disabled={!access.has('team:admin')}>
                  {t('Remove Team')}
                </Button>
              </Confirm>
            </div>
          </Field>
        </Panel>
      </React.Fragment>);
    };
    TeamSettings.contextTypes = {
        router: PropTypes.object,
        location: PropTypes.object,
        organization: SentryTypes.Organization,
    };
    return TeamSettings;
}(AsyncView));
export default TeamSettings;
//# sourceMappingURL=index.jsx.map