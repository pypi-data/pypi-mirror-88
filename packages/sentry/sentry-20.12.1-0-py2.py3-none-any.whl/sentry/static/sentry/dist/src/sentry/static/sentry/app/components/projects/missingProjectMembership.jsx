import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { joinTeam } from 'app/actionCreators/teams';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import { Panel } from 'app/components/panels';
import { IconFlag } from 'app/icons';
import { t } from 'app/locale';
import TeamStore from 'app/stores/teamStore';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var MissingProjectMembership = /** @class */ (function (_super) {
    __extends(MissingProjectMembership, _super);
    function MissingProjectMembership(props) {
        var _this = _super.call(this, props) || this;
        _this.handleChangeTeam = function (teamObj) {
            var team = teamObj ? teamObj.value : null;
            _this.setState({ team: team });
        };
        _this.getPendingTeamOption = function (team) {
            return {
                value: team,
                label: <DisabledLabel>{t("#" + team)}</DisabledLabel>,
            };
        };
        var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
        var project = organization.projects.find(function (p) { return p.slug === projectId; });
        _this.state = {
            loading: false,
            error: false,
            project: project,
            team: '',
        };
        return _this;
    }
    MissingProjectMembership.prototype.joinTeam = function (teamSlug) {
        var _this = this;
        this.setState({
            loading: true,
        });
        joinTeam(this.props.api, {
            orgId: this.props.organization.slug,
            teamId: teamSlug,
        }, {
            success: function () {
                _this.setState({
                    loading: false,
                    error: false,
                });
                addSuccessMessage(t('Request to join team sent.'));
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
                addErrorMessage(t('There was an error while trying to request access.'));
            },
        });
    };
    MissingProjectMembership.prototype.renderJoinTeam = function (teamSlug, features) {
        var team = TeamStore.getBySlug(teamSlug);
        if (!team) {
            return null;
        }
        if (this.state.loading) {
            if (features.has('open-membership')) {
                return <Button busy>{t('Join Team')}</Button>;
            }
            return <Button busy>{t('Request Access')}</Button>;
        }
        else if (team === null || team === void 0 ? void 0 : team.isPending) {
            return <Button disabled>{t('Request Pending')}</Button>;
        }
        else if (features.has('open-membership')) {
            return (<Button priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
          {t('Join Team')}
        </Button>);
        }
        return (<Button priority="primary" type="button" onClick={this.joinTeam.bind(this, teamSlug)}>
        {t('Request Access')}
      </Button>);
    };
    MissingProjectMembership.prototype.getTeamsForAccess = function () {
        var _a, _b;
        var request = [];
        var pending = [];
        var teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        teams.forEach(function (_a) {
            var slug = _a.slug;
            var team = TeamStore.getBySlug(slug);
            if (!team) {
                return;
            }
            team.isPending ? pending.push(team.slug) : request.push(team.slug);
        });
        return [request, pending];
    };
    MissingProjectMembership.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var organization = this.props.organization;
        var teamSlug = this.state.team;
        var teams = (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.teams) !== null && _b !== void 0 ? _b : [];
        var features = new Set(organization.features);
        var teamAccess = [
            {
                label: t('Request Access'),
                options: this.getTeamsForAccess()[0].map(function (request) { return ({
                    value: request,
                    label: t("#" + request),
                }); }),
            },
            {
                label: t('Pending Requests'),
                options: this.getTeamsForAccess()[1].map(function (pending) {
                    return _this.getPendingTeamOption(pending);
                }),
            },
        ];
        return (<StyledPanel>
        {!teams.length ? (<EmptyMessage icon={<IconFlag size="xl"/>}>
            {t('No teams have access to this project yet. Ask an admin to add your team to this project.')}
          </EmptyMessage>) : (<EmptyMessage icon={<IconFlag size="xl"/>} title={t("You're not a member of this project.")} description={t("You'll need to join a team with access before you can view this data.")} action={<Field>
                <StyledSelectControl name="select" placeholder={t('Select a Team')} options={teamAccess} onChange={this.handleChangeTeam}/>
                {teamSlug ? (this.renderJoinTeam(teamSlug, features)) : (<Button disabled>{t('Select a Team')}</Button>)}
              </Field>}/>)}
      </StyledPanel>);
    };
    return MissingProjectMembership;
}(React.Component));
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(2));
var Field = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  text-align: left;\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  text-align: left;\n"])), space(2));
var StyledSelectControl = styled(SelectControl)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 250px;\n"], ["\n  width: 250px;\n"])));
var DisabledLabel = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden;\n"], ["\n  display: flex;\n  opacity: 0.5;\n  overflow: hidden;\n"])));
export { MissingProjectMembership };
export default withApi(MissingProjectMembership);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=missingProjectMembership.jsx.map