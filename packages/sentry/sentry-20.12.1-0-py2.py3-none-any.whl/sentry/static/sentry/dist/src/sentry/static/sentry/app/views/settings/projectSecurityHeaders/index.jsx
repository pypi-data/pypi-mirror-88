import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import recreateRoute from 'app/utils/recreateRoute';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import ReportUri from 'app/views/settings/projectSecurityHeaders/reportUri';
var ProjectSecurityHeaders = /** @class */ (function (_super) {
    __extends(ProjectSecurityHeaders, _super);
    function ProjectSecurityHeaders() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectSecurityHeaders.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['keyList', "/projects/" + orgId + "/" + projectId + "/keys/"]];
    };
    ProjectSecurityHeaders.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Security Headers'), projectId, false);
    };
    ProjectSecurityHeaders.prototype.getReports = function () {
        return [
            {
                name: 'Content Security Policy (CSP)',
                url: recreateRoute('csp/', this.props),
            },
            {
                name: 'Certificate Transparency (Expect-CT)',
                url: recreateRoute('expect-ct/', this.props),
            },
            {
                name: 'HTTP Public Key Pinning (HPKP)',
                url: recreateRoute('hpkp/', this.props),
            },
        ];
    };
    ProjectSecurityHeaders.prototype.renderBody = function () {
        var params = this.props.params;
        var keyList = this.state.keyList;
        if (keyList === null) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={t('Security Header Reports')}/>

        <ReportUri keyList={keyList} projectId={params.projectId} orgId={params.orgId}/>

        <Panel>
          <PanelHeader>{t('Additional Configuration')}</PanelHeader>
          <PanelBody withPadding>
            <TextBlock style={{ marginBottom: 20 }}>
              {tct('In addition to the [key_param] parameter, you may also pass the following within the querystring for the report URI:', {
            key_param: <code>sentry_key</code>,
        })}
            </TextBlock>
            <table className="table" style={{ marginBottom: 0 }}>
              <tbody>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_environment</th>
                  <td style={{ padding: '8px 5px' }}>
                    {t('The environment name (e.g. production)')}.
                  </td>
                </tr>
                <tr>
                  <th style={{ padding: '8px 5px' }}>sentry_release</th>
                  <td style={{ padding: '8px 5px' }}>
                    {t('The version of the application.')}
                  </td>
                </tr>
              </tbody>
            </table>
          </PanelBody>
        </Panel>

        <Panel>
          <PanelHeader>{t('Supported Formats')}</PanelHeader>
          <PanelBody>
            {this.getReports().map(function (_a) {
            var name = _a.name, url = _a.url;
            return (<ReportItem key={url}>
                <HeaderName>{name}</HeaderName>
                <Button to={url} priority="primary">
                  {t('Instructions')}
                </Button>
              </ReportItem>);
        })}
          </PanelBody>
        </Panel>
      </div>);
    };
    return ProjectSecurityHeaders;
}(AsyncView));
export default ProjectSecurityHeaders;
var ReportItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
var HeaderName = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 1.2em;\n"], ["\n  font-size: 1.2em;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map