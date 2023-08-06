import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import ProjectActions from 'app/actions/projectActions';
import Button from 'app/components/button';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconFlag, IconSubtract } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { sortProjects } from 'app/utils';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ProjectListItem from 'app/views/settings/components/settingsProjectItem';
var TeamProjects = /** @class */ (function (_super) {
    __extends(TeamProjects, _super);
    function TeamProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            loading: true,
            pageLinks: null,
            unlinkedProjects: [],
            linkedProjects: [],
        };
        _this.fetchAll = function () {
            _this.fetchTeamProjects();
            _this.fetchUnlinkedProjects();
        };
        _this.handleLinkProject = function (project, action) {
            var _a = _this.props.params, orgId = _a.orgId, teamId = _a.teamId;
            _this.props.api.request("/projects/" + orgId + "/" + project.slug + "/teams/" + teamId + "/", {
                method: action === 'add' ? 'POST' : 'DELETE',
                success: function (resp) {
                    _this.fetchAll();
                    ProjectActions.updateSuccess(resp);
                    addSuccessMessage(action === 'add'
                        ? t('Successfully added project to team.')
                        : t('Successfully removed project from team'));
                },
                error: function () {
                    addErrorMessage(t("Wasn't able to change project association."));
                },
            });
        };
        _this.handleProjectSelected = function (selection) {
            var project = _this.state.unlinkedProjects.find(function (p) { return p.id === selection.value; });
            if (project) {
                _this.handleLinkProject(project, 'add');
            }
        };
        _this.handleQueryUpdate = function (evt) {
            _this.fetchUnlinkedProjects(evt.target.value);
        };
        return _this;
    }
    TeamProjects.prototype.componentDidMount = function () {
        this.fetchAll();
    };
    TeamProjects.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.teamId !== this.props.params.teamId) {
            this.fetchAll();
        }
        if (prevProps.location !== this.props.location) {
            this.fetchTeamProjects();
        }
    };
    TeamProjects.prototype.fetchTeamProjects = function () {
        var _this = this;
        var _a = this.props, location = _a.location, _b = _a.params, orgId = _b.orgId, teamId = _b.teamId;
        this.setState({ loading: true });
        this.props.api
            .requestPromise("/organizations/" + orgId + "/projects/", {
            query: {
                query: "team:" + teamId,
                cursor: location.query.cursor || '',
            },
            includeAllArgs: true,
        })
            .then(function (_a) {
            var _b;
            var _c = __read(_a, 3), linkedProjects = _c[0], _ = _c[1], jqXHR = _c[2];
            _this.setState({
                loading: false,
                error: false,
                linkedProjects: linkedProjects,
                pageLinks: (_b = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _b !== void 0 ? _b : null,
            });
        })
            .catch(function () {
            _this.setState({ loading: false, error: true });
        });
    };
    TeamProjects.prototype.fetchUnlinkedProjects = function (query) {
        var _this = this;
        if (query === void 0) { query = ''; }
        var _a = this.props.params, orgId = _a.orgId, teamId = _a.teamId;
        this.props.api
            .requestPromise("/organizations/" + orgId + "/projects/", {
            query: {
                query: query ? "!team:" + teamId + " " + query : "!team:" + teamId,
            },
        })
            .then(function (unlinkedProjects) {
            _this.setState({ unlinkedProjects: unlinkedProjects });
        });
    };
    TeamProjects.prototype.projectPanelContents = function (projects) {
        var _this = this;
        var organization = this.props.organization;
        var access = new Set(organization.access);
        var canWrite = access.has('org:write');
        return projects.length ? (sortProjects(projects).map(function (project) { return (<StyledPanelItem key={project.id}>
          <ProjectListItem project={project} organization={organization}/>
          <Tooltip disabled={canWrite} title={t('You do not have enough permission to change project association.')}>
            <Button size="small" disabled={!canWrite} icon={<IconSubtract isCircled size="xs"/>} onClick={function () {
            _this.handleLinkProject(project, 'remove');
        }}>
              {t('Remove')}
            </Button>
          </Tooltip>
        </StyledPanelItem>); })) : (<EmptyMessage size="large" icon={<IconFlag size="xl"/>}>
        {t("This team doesn't have access to any projects.")}
      </EmptyMessage>);
    };
    TeamProjects.prototype.render = function () {
        var _this = this;
        var _a = this.state, linkedProjects = _a.linkedProjects, unlinkedProjects = _a.unlinkedProjects, error = _a.error, loading = _a.loading;
        if (error) {
            return <LoadingError onRetry={function () { return _this.fetchAll(); }}/>;
        }
        if (loading) {
            return <LoadingIndicator />;
        }
        var access = new Set(this.props.organization.access);
        var otherProjects = unlinkedProjects.map(function (p) { return ({
            value: p.id,
            searchKey: p.slug,
            label: <ProjectListElement>{p.slug}</ProjectListElement>,
        }); });
        return (<React.Fragment>
        <Panel>
          <PanelHeader hasButtons>
            <div>{t('Projects')}</div>
            <div style={{ textTransform: 'none' }}>
              {!access.has('org:write') ? (<DropdownButton disabled title={t('You do not have enough permission to associate a project.')} size="xsmall">
                  {t('Add Project')}
                </DropdownButton>) : (<DropdownAutoComplete items={otherProjects} onChange={this.handleQueryUpdate} onSelect={this.handleProjectSelected} emptyMessage={t('No projects')} alignMenu="right">
                  {function (_a) {
            var isOpen = _a.isOpen;
            return (<DropdownButton isOpen={isOpen} size="xsmall">
                      {t('Add Project')}
                    </DropdownButton>);
        }}
                </DropdownAutoComplete>)}
            </div>
          </PanelHeader>
          <PanelBody>{this.projectPanelContents(linkedProjects)}</PanelBody>
        </Panel>
        <Pagination pageLinks={this.state.pageLinks} {...this.props}/>
      </React.Fragment>);
    };
    return TeamProjects;
}(React.Component));
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  padding: ", ";\n"])), space(2));
var ProjectListElement = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " 0;\n"], ["\n  padding: ", " 0;\n"])), space(0.25));
export { TeamProjects };
export default withApi(withOrganization(TeamProjects));
var templateObject_1, templateObject_2;
//# sourceMappingURL=teamProjects.jsx.map