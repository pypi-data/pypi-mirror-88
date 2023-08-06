import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { joinTeam, leaveTeam } from 'app/actionCreators/teams';
import Button from 'app/components/button';
import IdBadge from 'app/components/idBadge';
import { PanelItem } from 'app/components/panels';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var AllTeamsRow = /** @class */ (function (_super) {
    __extends(AllTeamsRow, _super);
    function AllTeamsRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            error: false,
        };
        _this.handleRequestAccess = function () { return __awaiter(_this, void 0, void 0, function () {
            var team;
            return __generator(this, function (_a) {
                team = this.props.team;
                try {
                    this.joinTeam({
                        successMessage: tct('You have requested access to [team]', {
                            team: "#" + team.slug,
                        }),
                        errorMessage: tct('Unable to request access to [team]', {
                            team: "#" + team.slug,
                        }),
                    });
                    // TODO: Ideally we would update team so that `isPending` is true
                }
                catch (_err) {
                    // No need to do anything
                }
                return [2 /*return*/];
            });
        }); };
        _this.handleJoinTeam = function () {
            var team = _this.props.team;
            _this.joinTeam({
                successMessage: tct('You have joined [team]', {
                    team: "#" + team.slug,
                }),
                errorMessage: tct('Unable to join [team]', {
                    team: "#" + team.slug,
                }),
            });
        };
        _this.joinTeam = function (_a) {
            var successMessage = _a.successMessage, errorMessage = _a.errorMessage;
            var _b = _this.props, api = _b.api, organization = _b.organization, team = _b.team;
            _this.setState({
                loading: true,
            });
            return new Promise(function (resolve, reject) {
                return joinTeam(api, {
                    orgId: organization.slug,
                    teamId: team.slug,
                }, {
                    success: function () {
                        _this.setState({
                            loading: false,
                            error: false,
                        });
                        addSuccessMessage(successMessage);
                        resolve();
                    },
                    error: function () {
                        _this.setState({
                            loading: false,
                            error: true,
                        });
                        addErrorMessage(errorMessage);
                        reject(new Error('Unable to join team'));
                    },
                });
            });
        };
        _this.handleLeaveTeam = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, team = _a.team;
            _this.setState({
                loading: true,
            });
            leaveTeam(api, {
                orgId: organization.slug,
                teamId: team.slug,
            }, {
                success: function () {
                    _this.setState({
                        loading: false,
                        error: false,
                    });
                    addSuccessMessage(tct('You have left [team]', {
                        team: "#" + team.slug,
                    }));
                },
                error: function () {
                    _this.setState({
                        loading: false,
                        error: true,
                    });
                    addErrorMessage(tct('Unable to leave [team]', {
                        team: "#" + team.slug,
                    }));
                },
            });
        };
        return _this;
    }
    AllTeamsRow.prototype.render = function () {
        var _a = this.props, team = _a.team, urlPrefix = _a.urlPrefix, openMembership = _a.openMembership;
        var display = (<IdBadge team={team} avatarSize={36} description={tn('%s Member', '%s Members', team.memberCount)}/>);
        // You can only view team details if you have access to team -- this should account
        // for your role + org open membership
        var canViewTeam = team.hasAccess;
        return (<TeamPanelItem>
        <TeamNameWrapper>
          {canViewTeam ? (<TeamLink to={urlPrefix + "teams/" + team.slug + "/"}>{display}</TeamLink>) : (display)}
        </TeamNameWrapper>
        <Spacer>
          {this.state.loading ? (<Button size="small" disabled>
              ...
            </Button>) : team.isMember ? (<Button size="small" onClick={this.handleLeaveTeam}>
              {t('Leave Team')}
            </Button>) : team.isPending ? (<Button size="small" disabled>
              {t('Request Pending')}
            </Button>) : openMembership ? (<Button size="small" onClick={this.handleJoinTeam}>
              {t('Join Team')}
            </Button>) : (<Button size="small" onClick={this.handleRequestAccess}>
              {t('Request Access')}
            </Button>)}
        </Spacer>
      </TeamPanelItem>);
    };
    return AllTeamsRow;
}(React.Component));
var TeamLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n\n  &.focus-visible {\n    margin: -", ";\n    padding: ", ";\n    background: #f2eff5;\n    border-radius: 3px;\n    outline: none;\n  }\n"], ["\n  display: inline-block;\n\n  &.focus-visible {\n    margin: -", ";\n    padding: ", ";\n    background: #f2eff5;\n    border-radius: 3px;\n    outline: none;\n  }\n"])), space(1), space(1));
export { AllTeamsRow };
export default withApi(AllTeamsRow);
var TeamPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0;\n  align-items: center;\n"], ["\n  padding: 0;\n  align-items: center;\n"])));
var Spacer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(2));
var TeamNameWrapper = styled(Spacer)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=allTeamsRow.jsx.map