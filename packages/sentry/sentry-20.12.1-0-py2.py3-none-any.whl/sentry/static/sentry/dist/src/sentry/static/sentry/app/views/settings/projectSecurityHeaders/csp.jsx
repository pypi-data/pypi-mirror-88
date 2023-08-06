import { __extends } from "tslib";
import React from 'react';
import Access from 'app/components/acl/access';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import PreviewFeature from 'app/components/previewFeature';
import formGroups from 'app/data/forms/cspReports';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ReportUri, { getSecurityDsn, } from 'app/views/settings/projectSecurityHeaders/reportUri';
var ProjectCspReports = /** @class */ (function (_super) {
    __extends(ProjectCspReports, _super);
    function ProjectCspReports() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectCspReports.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [
            ['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"],
            ['project', "/projects/" + orgId + "/" + projectId + "/"],
        ];
    };
    ProjectCspReports.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Content Security Policy (CSP)'), projectId, false);
    };
    ProjectCspReports.prototype.getInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Content-Security-Policy'] = \\\n" +
            '        "default-src *; " \\\n' +
            "        \"script-src 'self' 'unsafe-eval' 'unsafe-inline' cdn.example.com cdn.ravenjs.com; \" \\\n" +
            "        \"style-src 'self' 'unsafe-inline' cdn.example.com; \" \\\n" +
            '        "img-src * data:; " \\\n' +
            '        "report-uri ' +
            getSecurityDsn(keyList) +
            '"\n' +
            '    return response\n');
    };
    ProjectCspReports.prototype.getReportOnlyInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Content-Security-Policy-Report-Only'] = \\\n" +
            '        "default-src \'self\'; " \\\n' +
            '        "report-uri ' +
            getSecurityDsn(keyList) +
            '"\n' +
            '    return response\n');
    };
    ProjectCspReports.prototype.renderBody = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var _b = this.state, project = _b.project, keyList = _b.keyList;
        if (!keyList || !project) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={t('Content Security Policy')}/>

        <PreviewFeature />

        <ReportUri keyList={keyList} orgId={orgId} projectId={projectId}/>

        <Form saveOnBlur apiMethod="PUT" initialData={project.options} apiEndpoint={"/projects/" + orgId + "/" + projectId + "/"}>
          <Access access={['project:write']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return <JsonForm disabled={!hasAccess} forms={formGroups}/>;
        }}
          </Access>
        </Form>

        <Panel>
          <PanelHeader>{t('About')}</PanelHeader>

          <PanelBody withPadding>
            <p>
              {tct("[link:Content Security Policy]\n            (CSP) is a security standard which helps prevent cross-site scripting (XSS),\n            clickjacking and other code injection attacks resulting from execution of\n            malicious content in the trusted web page context. It's enforced by browser\n            vendors, and Sentry supports capturing CSP violations using the standard\n            reporting hooks.", {
            link: (<ExternalLink href="https://en.wikipedia.org/wiki/Content_Security_Policy"/>),
        })}
            </p>

            <p>
              {tct("To configure [csp:CSP] reports\n              in Sentry, you'll need to send a header from your server describing your\n              policy, as well specifying the authenticated Sentry endpoint.", {
            csp: <abbr title="Content Security Policy"/>,
        })}
            </p>

            <p>
              {t('For example, in Python you might achieve this via a simple web middleware')}
            </p>
            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {t("Alternatively you can setup CSP reports to simply send reports rather than\n              actually enforcing the policy")}
            </p>
            <pre>{this.getReportOnlyInstructions(keyList)}</pre>

            <p>
              {tct("We recommend setting this up to only run on a percentage of requests, as\n              otherwise you may find that you've quickly exhausted your quota. For more\n              information, take a look at [link:the article on html5rocks.com].", {
            link: (<a href="http://www.html5rocks.com/en/tutorials/security/content-security-policy/"/>),
        })}
            </p>
          </PanelBody>
        </Panel>
      </div>);
    };
    return ProjectCspReports;
}(AsyncView));
export default ProjectCspReports;
//# sourceMappingURL=csp.jsx.map