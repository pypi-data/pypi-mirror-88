import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import Tooltip from 'app/components/tooltip';
import { IconLink } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { FilterViews } from 'app/views/performance/landing';
import { DEFAULT_MAX_DURATION } from 'app/views/performance/trends/utils';
import { getPerformanceLandingUrl } from 'app/views/performance/utils';
function ProjectQuickLinks(_a) {
    var organization = _a.organization, project = _a.project, location = _a.location;
    function getTrendsLink() {
        var queryString = decodeScalar(location.query.query);
        var conditions = tokenizeSearch(queryString || '');
        conditions.setTagValues('tpm()', ['>0.01']);
        conditions.setTagValues('transaction.duration', ['>0', "<" + DEFAULT_MAX_DURATION]);
        return {
            pathname: getPerformanceLandingUrl(organization),
            query: {
                project: project === null || project === void 0 ? void 0 : project.id,
                cursor: undefined,
                query: stringifyQueryObject(conditions),
                view: FilterViews.TRENDS,
            },
        };
    }
    var quickLinks = [
        {
            title: t('User Feedback'),
            to: {
                pathname: "/organizations/" + organization.slug + "/user-feedback/",
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
        },
        {
            title: t('Key Transactions'),
            to: {
                pathname: getPerformanceLandingUrl(organization),
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
            disabled: !organization.features.includes('performance-view'),
        },
        {
            title: t('Most Improved/Regressed Transactions'),
            to: getTrendsLink(),
            disabled: !organization.features.includes('performance-view'),
        },
    ];
    return (<Section>
      <SectionHeading>{t('Quick Links')}</SectionHeading>
      {quickLinks
        // push disabled links to the bottom
        .sort(function (link1, link2) { return Number(!!link1.disabled) - Number(!!link2.disabled); })
        .map(function (_a) {
        var title = _a.title, to = _a.to, disabled = _a.disabled;
        return (<div key={title}>
            <Tooltip title={t("You don't have access to this feature")} disabled={!disabled}>
              <QuickLink to={to} disabled={disabled}>
                <IconLink />
                <QuickLinkText>{title}</QuickLinkText>
              </QuickLink>
            </Tooltip>
          </div>);
    })}
    </Section>);
}
var Section = styled('section')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var QuickLink = styled(function (p) {
    return p.disabled ? (<span className={p.className}>{p.children}</span>) : (<GlobalSelectionLink {...p}/>);
})(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  display: grid;\n  align-items: center;\n  gap: ", ";\n  grid-template-columns: auto 1fr;\n\n  ", "\n"], ["\n  margin-bottom: ", ";\n  display: grid;\n  align-items: center;\n  gap: ", ";\n  grid-template-columns: auto 1fr;\n\n  ",
    "\n"])), space(1), space(1), function (p) {
    return p.disabled &&
        "\n    color: " + p.theme.gray200 + ";\n    cursor: not-allowed;\n  ";
});
var QuickLinkText = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
export default ProjectQuickLinks;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectQuickLinks.jsx.map