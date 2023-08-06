import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
var ProjectTeamAccess = /** @class */ (function (_super) {
    __extends(ProjectTeamAccess, _super);
    function ProjectTeamAccess() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: true,
        };
        _this.onCollapseToggle = function () {
            _this.setState(function (prevState) { return ({
                collapsed: !prevState.collapsed,
            }); });
        };
        return _this;
    }
    ProjectTeamAccess.prototype.renderInnerBody = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        if (!project) {
            return <Placeholder height="23px"/>;
        }
        if (project.teams.length === 0) {
            var hasPermission = organization.access.includes('project:write');
            return (<Button to={"/settings/" + organization.slug + "/projects/" + project.slug + "/teams/"} disabled={!hasPermission} title={hasPermission ? undefined : t('You do not have permission to do this')} priority="primary" size="small">
          {t('Assign Team')}
        </Button>);
        }
        var teams = project.teams;
        var collapsed = this.state.collapsed;
        var canExpand = teams.length > ProjectTeamAccess.MAX_WHEN_COLLAPSED;
        var teamsToRender = collapsed && canExpand
            ? teams.slice(0, ProjectTeamAccess.MAX_WHEN_COLLAPSED)
            : teams;
        var numberOfCollapsedTeams = teams.length - teamsToRender.length;
        return (<React.Fragment>
        {teamsToRender.map(function (team) { return (<StyledLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"} key={team.slug}>
            <IdBadge team={team} hideAvatar/>
          </StyledLink>); })}
        {numberOfCollapsedTeams > 0 && (<CollapseToggle priority="link" onClick={this.onCollapseToggle}>
            {tn('Show %s collapsed team', 'Show %s collapsed teams', numberOfCollapsedTeams)}
          </CollapseToggle>)}
        {numberOfCollapsedTeams === 0 && canExpand && (<CollapseToggle priority="link" onClick={this.onCollapseToggle}>
            {t('Collapse')}
          </CollapseToggle>)}
      </React.Fragment>);
    };
    ProjectTeamAccess.prototype.render = function () {
        return (<Section>
        <SectionHeading>{t('Team Access')}</SectionHeading>

        <div>{this.renderInnerBody()}</div>
      </Section>);
    };
    ProjectTeamAccess.MAX_WHEN_COLLAPSED = 5;
    return ProjectTeamAccess;
}(React.Component));
var Section = styled('section')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin-bottom: ", ";\n"], ["\n  display: block;\n  margin-bottom: ", ";\n"])), space(0.5));
var CollapseToggle = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default ProjectTeamAccess;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectTeamAccess.jsx.map