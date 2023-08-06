import { __extends } from "tslib";
import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import PreviewFeature from 'app/components/previewFeature';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ReportUri, { getSecurityDsn, } from 'app/views/settings/projectSecurityHeaders/reportUri';
var ProjectHpkpReports = /** @class */ (function (_super) {
    __extends(ProjectHpkpReports, _super);
    function ProjectHpkpReports() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectHpkpReports.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectHpkpReports.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('HTTP Public Key Pinning (HPKP)'), projectId, false);
    };
    ProjectHpkpReports.prototype.getInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            ("        'report-uri=\"" + getSecurityDsn(keyList) + "\"' \n") +
            '    return response\n');
    };
    ProjectHpkpReports.prototype.getReportOnlyInstructions = function (keyList) {
        return ('def middleware(request, response):\n' +
            "    response['Public-Key-Pins-Report-Only'] = \\\n" +
            '        \'pin-sha256="cUPcTAZWKaASuYWhhneDttWpY3oBAkE3h2+soZS7sWs="; \' \\\n' +
            '        \'pin-sha256="M8HztCzM3elUxkcjR2S5P4hhyBNf6lHkmjAHKhpGPWE="; \' \\\n' +
            "        'max-age=5184000; includeSubDomains; ' \\\n" +
            ("        'report-uri=\"" + getSecurityDsn(keyList) + "\"' \n") +
            '    return response\n');
    };
    ProjectHpkpReports.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (!keyList) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={t('HTTP Public Key Pinning')}/>

        <PreviewFeature />

        <ReportUri keyList={keyList} orgId={params.orgId} projectId={params.projectId}/>

        <Panel>
          <PanelHeader>{t('About')}</PanelHeader>

          <PanelBody withPadding>
            <p>
              {tct("[link:HTTP Public Key Pinning]\n              (HPKP) is a security feature that tells a web client to associate a specific\n              cryptographic public key with a certain web server to decrease the risk of MITM\n              attacks with forged certificates. It's enforced by browser vendors, and Sentry\n              supports capturing violations using the standard reporting hooks.", {
            link: (<ExternalLink href="https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning"/>),
        })}
            </p>

            <p>
              {t("To configure HPKP reports\n              in Sentry, you'll need to send a header from your server describing your\n              policy, as well specifying the authenticated Sentry endpoint.")}
            </p>

            <p>
              {t('For example, in Python you might achieve this via a simple web middleware')}
            </p>
            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {t("Alternatively you can setup HPKP reports to simply send reports rather than\n              actually enforcing the policy")}
            </p>
            <pre>{this.getReportOnlyInstructions(keyList)}</pre>

            <p>
              {tct("We recommend setting this up to only run on a percentage of requests, as\n              otherwise you may find that you've quickly exhausted your quota. For more\n              information, take a look at [link:the documentation on MDN].", {
            link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning"/>),
        })}
            </p>
          </PanelBody>
        </Panel>
      </div>);
    };
    return ProjectHpkpReports;
}(AsyncView));
export default ProjectHpkpReports;
//# sourceMappingURL=hpkp.jsx.map