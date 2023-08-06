import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { fetchTeamDetails, joinTeam } from 'app/actionCreators/teams';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import IdBadge from 'app/components/idBadge';
import ListLink from 'app/components/links/listLink';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import NavTabs from 'app/components/navTabs';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t, tct } from 'app/locale';
import TeamStore from 'app/stores/teamStore';
import recreateRoute from 'app/utils/recreateRoute';
import withApi from 'app/utils/withApi';
import withTeams from 'app/utils/withTeams';
var TeamDetails = /** @class */ (function (_super) {
    __extends(TeamDetails, _super);
    function TeamDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRequestAccess = function () {
            var _a = _this.props, api = _a.api, params = _a.params;
            var team = _this.state.team;
            if (!team) {
                return;
            }
            _this.setState({
                requesting: true,
            });
            joinTeam(api, {
                orgId: params.orgId,
                teamId: team.slug,
            }, {
                success: function () {
                    addSuccessMessage(tct('You have requested access to [team]', {
                        team: "#" + team.slug,
                    }));
                    _this.setState({
                        requesting: false,
                    });
                },
                error: function () {
                    addErrorMessage(tct('Unable to request access to [team]', {
                        team: "#" + team.slug,
                    }));
                    _this.setState({
                        requesting: false,
                    });
                },
            });
        };
        _this.fetchData = function () {
            _this.setState({
                loading: true,
                error: false,
            });
            fetchTeamDetails(_this.props.api, _this.props.params);
        };
        _this.onTeamChange = function (data) {
            var team = _this.state.team;
            if (data.slug !== (team === null || team === void 0 ? void 0 : team.slug)) {
                var orgId = _this.props.params.orgId;
                browserHistory.replace("/organizations/" + orgId + "/teams/" + data.slug + "/settings/");
            }
            else {
                _this.setState({
                    team: __assign(__assign({}, team), data),
                });
            }
        };
        return _this;
    }
    TeamDetails.prototype.getInitialState = function () {
        var team = TeamStore.getBySlug(this.props.params.teamId);
        return {
            loading: !TeamStore.initialized,
            error: false,
            requesting: false,
            team: team,
        };
    };
    TeamDetails.prototype.componentDidUpdate = function (prevProps) {
        var params = this.props.params;
        if (prevProps.params.teamId !== params.teamId ||
            prevProps.params.orgId !== params.orgId) {
            this.fetchData();
        }
        if (!isEqual(this.props.teams, prevProps.teams)) {
            this.setActiveTeam();
        }
    };
    TeamDetails.prototype.setActiveTeam = function () {
        var _a, _b;
        var teamId = this.props.params.teamId;
        var team = (_b = (_a = this.props.teams) === null || _a === void 0 ? void 0 : _a.find(function (item) { return item.id === teamId; })) !== null && _b !== void 0 ? _b : null;
        var loading = !TeamStore.initialized;
        var error = !loading && !team;
        this.setState({ team: team, loading: loading, error: error });
    };
    TeamDetails.prototype.render = function () {
        var _a = this.props, params = _a.params, routes = _a.routes, children = _a.children;
        var _b = this.state, team = _b.team, loading = _b.loading, requesting = _b.requesting, error = _b.error;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (!team || !team.hasAccess) {
            return (<Alert type="warning">
          {team ? (<RequestAccessWrapper>
              {tct('You do not have access to the [teamSlug] team.', {
                teamSlug: <strong>{"#" + team.slug}</strong>,
            })}
              <Button disabled={requesting || team.isPending} size="small" onClick={this.handleRequestAccess}>
                {team.isPending ? t('Request Pending') : t('Request Access')}
              </Button>
            </RequestAccessWrapper>) : (<div>{t('You do not have access to this team.')}</div>)}
        </Alert>);
        }
        if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        var routePrefix = recreateRoute('', { routes: routes, params: params, stepBack: -1 }); //`/organizations/${orgId}/teams/${teamId}`;
        return (<div>
        <SentryDocumentTitle title={t('Team Details')} objSlug={params.orgId}/>
        <h3>
          <IdBadge hideAvatar team={team} avatarSize={36}/>
        </h3>

        <NavTabs underlined>
          <ListLink to={routePrefix + "members/"}>{t('Members')}</ListLink>
          <ListLink to={routePrefix + "projects/"}>{t('Projects')}</ListLink>
          <ListLink to={routePrefix + "settings/"}>{t('Settings')}</ListLink>
        </NavTabs>

        {React.isValidElement(children) &&
            React.cloneElement(children, {
                team: team,
                onTeamChange: this.onTeamChange,
            })}
      </div>);
    };
    return TeamDetails;
}(React.Component));
export default withApi(withTeams(TeamDetails));
var RequestAccessWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=teamDetails.jsx.map