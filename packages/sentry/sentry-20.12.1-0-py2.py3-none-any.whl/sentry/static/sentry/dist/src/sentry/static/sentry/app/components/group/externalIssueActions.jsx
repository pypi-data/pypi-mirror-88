import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import ExternalIssueForm from './externalIssueForm';
var ExternalIssueActions = function (_a) {
    var configurations = _a.configurations, group = _a.group, onChange = _a.onChange, api = _a.api;
    var _b = configurations
        .sort(function (a, b) { return a.name.toLowerCase().localeCompare(b.name.toLowerCase()); })
        .reduce(function (acc, curr) {
        if (curr.externalIssues.length) {
            acc.linked.push(curr);
        }
        else {
            acc.unlinked.push(curr);
        }
        return acc;
    }, { linked: [], unlinked: [] }), linked = _b.linked, unlinked = _b.unlinked;
    var deleteIssue = function (integration) {
        var externalIssues = integration.externalIssues;
        // Currently we do not support a case where there is multiple external issues.
        // For example, we shouldn't have more than 1 jira ticket created for an issue for each jira configuration.
        var issue = externalIssues[0];
        var id = issue.id;
        var endpoint = "/groups/" + group.id + "/integrations/" + integration.id + "/?externalIssue=" + id;
        api.request(endpoint, {
            method: 'DELETE',
            success: function () {
                onChange(function () { return addSuccessMessage(t('Successfully unlinked issue.')); }, function () { return addErrorMessage(t('Unable to unlink issue.')); });
            },
            error: function () {
                addErrorMessage(t('Unable to unlink issue.'));
            },
        });
    };
    var doOpenModal = function (integration) {
        return openModal(function (deps) { return (<ExternalIssueForm {...deps} {...{ group: group, onChange: onChange, integration: integration }}/>); });
    };
    return (<React.Fragment>
      {linked.map(function (config) {
        var provider = config.provider, externalIssues = config.externalIssues;
        var issue = externalIssues[0];
        return (<IssueSyncListElement key={issue.id} externalIssueLink={issue.url} externalIssueId={issue.id} externalIssueKey={issue.key} externalIssueDisplayName={issue.displayName} onClose={function () { return deleteIssue(config); }} integrationType={provider.key} hoverCardHeader={t('Linked %s Integration', provider.name)} hoverCardBody={<div>
                <IssueTitle>{issue.title}</IssueTitle>
                {issue.description && (<IssueDescription>{issue.description}</IssueDescription>)}
              </div>}/>);
    })}

      {unlinked.length > 0 && (<IssueSyncListElement integrationType={unlinked[0].provider.key} hoverCardHeader={t('Linked %s Integration', unlinked[0].provider.name)} hoverCardBody={<Container>
              {unlinked.map(function (config) { return (<Wrapper onClick={function () { return doOpenModal(config); }} key={config.id}>
                  <IntegrationItem integration={config}/>
                </Wrapper>); })}
            </Container>} onOpen={unlinked.length === 1 ? function () { return doOpenModal(unlinked[0]); } : undefined}/>)}
    </React.Fragment>);
};
var IssueTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"], ["\n  font-size: 1.1em;\n  font-weight: 600;\n  ", ";\n"])), overflowEllipsis);
var IssueDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  ", ";\n"], ["\n  margin-top: ", ";\n  ", ";\n"])), space(1), overflowEllipsis);
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  cursor: pointer;\n"], ["\n  margin-bottom: ", ";\n  cursor: pointer;\n"])), space(2));
var Container = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"], ["\n  & > div:last-child {\n    margin-bottom: ", ";\n  }\n"])), space(1));
export default withApi(ExternalIssueActions);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=externalIssueActions.jsx.map