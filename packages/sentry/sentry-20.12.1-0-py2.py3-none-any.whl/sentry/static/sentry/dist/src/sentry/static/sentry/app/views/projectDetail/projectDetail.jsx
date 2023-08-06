import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import IdBadge from 'app/components/idBadge';
import * as Layout from 'app/components/layouts/thirds';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import TextOverflow from 'app/components/textOverflow';
import { IconSettings } from 'app/icons';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import ProjectCharts from './projectCharts';
import ProjectIssues from './projectIssues';
import ProjectLatestAlerts from './projectLatestAlerts';
import ProjectLatestReleases from './projectLatestReleases';
import ProjectQuickLinks from './projectQuickLinks';
import ProjectScoreCards from './projectScoreCards';
import ProjectTeamAccess from './projectTeamAccess';
var ProjectDetail = /** @class */ (function (_super) {
    __extends(ProjectDetail, _super);
    function ProjectDetail() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectDetail.prototype.getTitle = function () {
        var params = this.props.params;
        return routeTitleGen(t('Project %s', params.projectId), params.orgId, false);
    };
    ProjectDetail.prototype.getEndpoints = function () {
        var _a;
        var params = this.props.params;
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.project) {
            return [];
        }
        return [['project', "/projects/" + params.orgId + "/" + params.projectId + "/"]];
    };
    ProjectDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, router = _a.router;
        var project = this.state.project;
        return (<GlobalSelectionHeader shouldForceProject forceProject={project}>
        <LightWeightNoProjectMessage organization={organization}>
          <StyledPageContent>
            <Layout.Header>
              <Layout.HeaderContent>
                <Breadcrumbs crumbs={[
            {
                to: "/organizations/" + params.orgId + "/projects/",
                label: t('Projects'),
            },
            { label: t('Project Details') },
        ]}/>
                <Layout.Title>
                  <TextOverflow>
                    {project && (<IdBadge project={project} avatarSize={28} displayName={params.projectId}/>)}
                  </TextOverflow>
                </Layout.Title>
              </Layout.HeaderContent>

              <Layout.HeaderActions>
                <ButtonBar gap={1}>
                  <Button to={"/organizations/" + params.orgId + "/issues/?project=" + params.projectId}>
                    {t('View All Issues')}
                  </Button>
                  <CreateAlertButton organization={organization} projectSlug={params.projectId}/>
                  <Button icon={<IconSettings />} label={t('Settings')} to={"/settings/" + params.orgId + "/projects/" + params.projectId + "/"}/>
                </ButtonBar>
              </Layout.HeaderActions>
            </Layout.Header>

            <Layout.Body>
              <Layout.Main>
                <ProjectScoreCards organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id}/>
                {[0, 1].map(function (id) { return (<ProjectCharts location={location} organization={organization} router={router} key={"project-charts-" + id} index={id}/>); })}
                <ProjectIssues organization={organization} location={location}/>
              </Layout.Main>
              <Layout.Side>
                <ProjectTeamAccess organization={organization} project={project}/>
                <Feature features={['incidents']}>
                  <ProjectLatestAlerts organization={organization} projectSlug={params.projectId} location={location}/>
                </Feature>
                <ProjectLatestReleases organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id} location={location}/>
                <ProjectQuickLinks organization={organization} project={project} location={location}/>
              </Layout.Side>
            </Layout.Body>
          </StyledPageContent>
        </LightWeightNoProjectMessage>
      </GlobalSelectionHeader>);
    };
    return ProjectDetail;
}(AsyncView));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export default ProjectDetail;
var templateObject_1;
//# sourceMappingURL=projectDetail.jsx.map