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
var ProjectExpectCtReports = /** @class */ (function (_super) {
    __extends(ProjectExpectCtReports, _super);
    function ProjectExpectCtReports() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectExpectCtReports.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectExpectCtReports.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Certificate Transparency (Expect-CT)'), projectId, false);
    };
    ProjectExpectCtReports.prototype.getInstructions = function (keyList) {
        return "Expect-CT: report-uri=\"" + getSecurityDsn(keyList) + "\"";
    };
    ProjectExpectCtReports.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (!keyList) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={t('Certificate Transparency')}/>

        <PreviewFeature />

        <ReportUri keyList={keyList} orgId={params.orgId} projectId={params.orgId}/>

        <Panel>
          <PanelHeader>{'About'}</PanelHeader>
          <PanelBody withPadding>
            <p>
              {tct("[link:Certificate Transparency]\n      (CT) is a security standard which helps track and identify valid certificates, allowing identification of maliciously issued certificates", {
            link: (<ExternalLink href="https://en.wikipedia.org/wiki/Certificate_Transparency"/>),
        })}
            </p>
            <p>
              {tct("To configure reports in Sentry, you'll need to configure the [header] a header from your server:", {
            header: <code>Expect-CT</code>,
        })}
            </p>

            <pre>{this.getInstructions(keyList)}</pre>

            <p>
              {tct('For more information, see [link:the article on MDN].', {
            link: (<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Expect-CT"/>),
        })}
            </p>
          </PanelBody>
        </Panel>
      </div>);
    };
    return ProjectExpectCtReports;
}(AsyncView));
export default ProjectExpectCtReports;
//# sourceMappingURL=expectCt.jsx.map