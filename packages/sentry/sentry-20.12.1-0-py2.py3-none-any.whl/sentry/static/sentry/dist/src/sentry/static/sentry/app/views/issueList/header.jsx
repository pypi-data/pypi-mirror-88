import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import * as Layout from 'app/components/layouts/thirds';
import QueryCount from 'app/components/queryCount';
import { IconPause, IconPlay } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var queries = [
    ['is:needs_review is:unresolved', t('Needs Review')],
    ['is:unresolved', t('Unresolved')],
    ['is:ignored', t('Ignored')],
];
function IssueListHeader(_a) {
    var query = _a.query, queryCount = _a.queryCount, queryMaxCount = _a.queryMaxCount, realtimeActive = _a.realtimeActive, onTabChange = _a.onTabChange, onRealtimeChange = _a.onRealtimeChange;
    var count = <StyledQueryCount count={queryCount} max={queryMaxCount}/>;
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{t('Issues')}</StyledLayoutTitle>
        </StyledHeaderContent>
        <Layout.HeaderActions>
          <Button size="small" title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))} onClick={function () { return onRealtimeChange(!realtimeActive); }}>
            {realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}
          </Button>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          {queries.map(function (_a) {
        var _b = __read(_a, 2), tabQuery = _b[0], queryName = _b[1];
        return (<li key={tabQuery} className={query === tabQuery ? 'active' : ''}>
              <a onClick={function () { return onTabChange(tabQuery); }}>
                {queryName} {query === tabQuery && count}
              </a>
            </li>);
    })}
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
}
export default IssueListHeader;
var StyledLayoutTitle = styled(Layout.Title)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var BorderlessHeader = styled(Layout.Header)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var TabLayoutHeader = styled(Layout.Header)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"], ["\n  padding-top: 0;\n\n  @media (max-width: ", ") {\n    padding-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledQueryCount = styled(QueryCount)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map