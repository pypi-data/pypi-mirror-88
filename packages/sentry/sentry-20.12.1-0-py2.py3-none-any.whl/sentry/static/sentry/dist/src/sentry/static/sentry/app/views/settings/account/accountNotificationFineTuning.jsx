import { __assign, __extends, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { fields } from 'app/data/forms/accountNotificationSettings';
import { t } from 'app/locale';
import withOrganizations from 'app/utils/withOrganizations';
import AsyncView from 'app/views/asyncView';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SelectField from 'app/views/settings/components/forms/selectField';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var ACCOUNT_NOTIFICATION_FIELDS = {
    alerts: {
        title: 'Project Alerts',
        description: t('Control alerts that you receive per project.'),
        type: 'select',
        choices: [
            [-1, t('Default')],
            [1, t('On')],
            [0, t('Off')],
        ],
        defaultValue: -1,
        defaultFieldName: 'subscribeByDefault',
    },
    workflow: {
        title: 'Workflow Notifications',
        description: t('Control workflow notifications, e.g. changes in issue assignment, resolution status, and comments.'),
        type: 'select',
        choices: [
            [-1, t('Default')],
            [0, t('Always')],
            [1, t('Only on issues I subscribe to')],
            [2, t('Never')],
        ],
        defaultValue: -1,
        defaultFieldName: 'workflowNotifications',
    },
    deploy: {
        title: t('Deploy Notifications'),
        description: t('Control deploy notifications that include release, environment, and commit overviews.'),
        type: 'select',
        choices: [
            [-1, t('Default')],
            [2, t('Always')],
            [3, t('Only on deploys with my commits')],
            [4, t('Never')],
        ],
        defaultValue: -1,
        defaultFieldName: 'deployNotifications',
    },
    reports: {
        title: t('Weekly Reports'),
        description: t("Reports contain a summary of what's happened within the organization."),
        type: 'select',
        // API only saves organizations that have this disabled, so we should default to "On"
        defaultValue: 1,
        choices: [
            [1, t('On')],
            [0, t('Off')],
        ],
        defaultFieldName: 'weeklyReports',
    },
    email: {
        title: t('Email Routing'),
        description: t('On a per project basis, route emails to an alternative email address.'),
        type: 'select',
    },
};
var PanelBodyLineItem = styled(PanelBody)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; });
// Which fine tuning parts are grouped by project
var isGroupedByProject = function (type) {
    return ['alerts', 'workflow', 'email'].indexOf(type) > -1;
};
function groupByOrganization(projects) {
    return projects.reduce(function (acc, project) {
        var orgSlug = project.organization.slug;
        if (acc.hasOwnProperty(orgSlug)) {
            acc[orgSlug].projects.push(project);
        }
        else {
            acc[orgSlug] = {
                organization: project.organization,
                projects: [project],
            };
        }
        return acc;
    }, {});
}
var AccountNotificationsByProject = function (_a) {
    var projects = _a.projects, field = _a.field;
    var projectsByOrg = groupByOrganization(projects);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = __rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = Object.values(projectsByOrg).map(function (org) { return ({
        name: org.organization.name,
        projects: org.projects.map(function (project) { return (__assign(__assign({}, fieldConfig), { 
            // `name` key refers to field name
            // we use project.id because slugs are not unique across orgs
            name: project.id, label: project.slug })); }),
    }); });
    return (<React.Fragment>
      {data.map(function (_a) {
        var name = _a.name, projectFields = _a.projects;
        return (<div key={name}>
          <PanelHeader>{name}</PanelHeader>
          {projectFields.map(function (f) { return (<PanelBodyLineItem key={f.name}>
              <SelectField deprecatedSelectControl defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
            </PanelBodyLineItem>); })}
        </div>);
    })}
    </React.Fragment>);
};
var AccountNotificationsByOrganization = function (_a) {
    var organizations = _a.organizations, field = _a.field;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = __rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = organizations.map(function (org) { return (__assign(__assign({}, fieldConfig), { 
        // `name` key refers to field name
        // we use org.id to remain consistent project.id use (which is required because slugs are not unique across orgs)
        name: org.id, label: org.slug })); });
    return (<React.Fragment>
      {data.map(function (f) { return (<PanelBodyLineItem key={f.name}>
          <SelectField deprecatedSelectControl defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
        </PanelBodyLineItem>); })}
    </React.Fragment>);
};
var AccountNotificationsByOrganizationContainer = withOrganizations(AccountNotificationsByOrganization);
var AccountNotificationFineTuning = /** @class */ (function (_super) {
    __extends(AccountNotificationFineTuning, _super);
    function AccountNotificationFineTuning() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountNotificationFineTuning.prototype.getEndpoints = function () {
        var fineTuneType = this.props.params.fineTuneType;
        var endpoints = [
            ['notifications', '/users/me/notifications/'],
            ['fineTuneData', "/users/me/notifications/" + fineTuneType + "/"],
        ];
        if (isGroupedByProject(fineTuneType)) {
            endpoints.push(['projects', '/projects/']);
        }
        endpoints.push(['emails', '/users/me/emails/']);
        if (fineTuneType === 'email') {
            endpoints.push(['emails', '/users/me/emails/']);
        }
        return endpoints;
    };
    Object.defineProperty(AccountNotificationFineTuning.prototype, "emailChoices", {
        // Return a sorted list of user's verified emails
        get: function () {
            var _a, _b, _c;
            return ((_c = (_b = (_a = this.state.emails) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                var isVerified = _a.isVerified;
                return isVerified;
            })) === null || _b === void 0 ? void 0 : _b.sort(function (a, b) {
                // Sort by primary -> email
                if (a.isPrimary) {
                    return -1;
                }
                else if (b.isPrimary) {
                    return 1;
                }
                return a.email < b.email ? -1 : 1;
            })) !== null && _c !== void 0 ? _c : []);
        },
        enumerable: false,
        configurable: true
    });
    AccountNotificationFineTuning.prototype.renderBody = function () {
        var fineTuneType = this.props.params.fineTuneType;
        var _a = this.state, notifications = _a.notifications, projects = _a.projects, fineTuneData = _a.fineTuneData, projectsPageLinks = _a.projectsPageLinks;
        var isProject = isGroupedByProject(fineTuneType);
        var field = ACCOUNT_NOTIFICATION_FIELDS[fineTuneType];
        var title = field.title, description = field.description;
        var _b = __read(isProject ? this.getEndpoints()[2] : [], 2), stateKey = _b[0], url = _b[1];
        var hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length);
        if (fineTuneType === 'email') {
            // Fetch verified email addresses
            field.choices = this.emailChoices.map(function (_a) {
                var email = _a.email;
                return [email, email];
            });
        }
        if (!notifications || !fineTuneData) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={title}/>
        {description && <TextBlock>{description}</TextBlock>}

        {field &&
            field.defaultFieldName &&
            // not implemented yet
            field.defaultFieldName !== 'weeklyReports' && (<Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/" initialData={notifications}>
              <JsonForm title={"Default " + title} fields={[fields[field.defaultFieldName]]}/>
            </Form>)}
        <Panel>
          <PanelBody>
            <PanelHeader hasButtons={isProject}>
              <Heading>{isProject ? t('Projects') : t('Organizations')}</Heading>
              <div>
                {isProject &&
            this.renderSearchInput({
                placeholder: t('Search Projects'),
                url: url,
                stateKey: stateKey,
            })}
              </div>
            </PanelHeader>

            <Form saveOnBlur apiMethod="PUT" apiEndpoint={"/users/me/notifications/" + fineTuneType + "/"} initialData={fineTuneData}>
              {isProject && hasProjects && (<AccountNotificationsByProject projects={projects} field={field}/>)}

              {isProject && !hasProjects && (<EmptyMessage>{t('No projects found')}</EmptyMessage>)}

              {!isProject && (<AccountNotificationsByOrganizationContainer field={field}/>)}
            </Form>
          </PanelBody>
        </Panel>

        {projects && <Pagination pageLinks={projectsPageLinks} {...this.props}/>}
      </div>);
    };
    return AccountNotificationFineTuning;
}(AsyncView));
export default AccountNotificationFineTuning;
var Heading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=accountNotificationFineTuning.jsx.map