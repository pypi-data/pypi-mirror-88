import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { SectionHeading } from 'app/components/charts/styles';
import Link from 'app/components/links/link';
import QuestionTooltip from 'app/components/questionTooltip';
import UserMisery from 'app/components/userMisery';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { getTermHelp } from 'app/views/performance/data';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, WEB_VITAL_DETAILS, } from 'app/views/performance/transactionVitals/constants';
import { vitalsRouteWithQuery } from 'app/views/performance/transactionVitals/utils';
import VitalsCards from '../vitalsCards';
function UserStats(_a) {
    var _b;
    var eventView = _a.eventView, totals = _a.totals, location = _a.location, organization = _a.organization, transactionName = _a.transactionName;
    var userMisery = <StatNumber>{'\u2014'}</StatNumber>;
    var threshold = organization.apdexThreshold;
    var apdex = <StatNumber>{'\u2014'}</StatNumber>;
    var vitalsPassRate = null;
    if (totals) {
        var miserableUsers = Number(totals["user_misery_" + threshold]);
        var totalUsers = Number(totals.count_unique_user);
        if (!isNaN(miserableUsers) && !isNaN(totalUsers)) {
            userMisery = (<UserMisery bars={40} barHeight={30} miseryLimit={threshold} totalUsers={totalUsers} miserableUsers={miserableUsers}/>);
        }
        var apdexKey = "apdex_" + threshold;
        var formatter = getFieldRenderer(apdexKey, (_b = {}, _b[apdexKey] = 'number', _b));
        apdex = formatter(totals, { organization: organization, location: location });
        var _c = __read(VITAL_GROUPS.map(function (_a) {
            var vs = _a.vitals;
            return vs;
        }).reduce(function (_a, vs) {
            var _b = __read(_a, 2), passed = _b[0], total = _b[1];
            vs.forEach(function (vital) {
                var alias = getAggregateAlias("percentile(" + vital + ", " + VITAL_PERCENTILE + ")");
                if (Number.isFinite(totals[alias])) {
                    total += 1;
                    if (totals[alias] < WEB_VITAL_DETAILS[vital].failureThreshold) {
                        passed += 1;
                    }
                }
            });
            return [passed, total];
        }, [0, 0]), 2), vitalsPassed = _c[0], vitalsTotal = _c[1];
        if (vitalsTotal > 0) {
            vitalsPassRate = <StatNumber>{vitalsPassed + "/" + vitalsTotal}</StatNumber>;
        }
    }
    var webVitalsTarget = vitalsRouteWithQuery({
        orgSlug: organization.slug,
        transaction: transactionName,
        projectID: decodeScalar(location.query.project),
        query: location.query,
    });
    return (<div>
      <SidebarWrapper>
        <SectionHeading>
          {t('Apdex Score')}
          <QuestionTooltip position="top" title={t('Apdex is the ratio of both satisfactory and tolerable response time to all response times.')} size="sm"/>
        </SectionHeading>
        <StatNumber>{apdex}</StatNumber>
        <Link to={"/settings/" + organization.slug + "/performance/"}>
          <SectionValue>
            {threshold}ms {t('threshold')}
          </SectionValue>
        </Link>
      </SidebarWrapper>
      <Feature features={['organizations:performance-vitals-overview']}>
        {function (_a) {
        var hasFeature = _a.hasFeature;
        if (hasFeature) {
            return (<SidebarWrapper>
                <VitalsHeading>
                  <SectionHeading>
                    {t('Web Vitals')}
                    <QuestionTooltip position="top" title={t('Web Vitals with p75 better than the "poor" threshold, as defined by Google Web Vitals.')} size="sm"/>
                  </SectionHeading>
                  <Link to={webVitalsTarget}>
                    <IconOpen />
                  </Link>
                </VitalsHeading>
                <VitalsCards eventView={eventView} organization={organization} location={location} hasCondensedVitals/>
              </SidebarWrapper>);
        }
        else {
            return (vitalsPassRate !== null && (<div>
                  <SectionHeading>
                    {t('Web Vitals')}
                    <QuestionTooltip position="top" title={t('Web Vitals with p75 better than the "poor" threshold, as defined by Google Web Vitals.')} size="sm"/>
                  </SectionHeading>
                  <StatNumber>{vitalsPassRate}</StatNumber>
                  <Link to={webVitalsTarget}>
                    <SectionValue>{t('Passed')}</SectionValue>
                  </Link>
                </div>));
        }
    }}
      </Feature>
      <UserMiseryContainer>
        <SectionHeading>
          {t('User Misery')}
          <QuestionTooltip position="top" title={getTermHelp(organization, 'userMisery')} size="sm"/>
        </SectionHeading>
        {userMisery}
      </UserMiseryContainer>
    </div>);
}
var SidebarWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var VitalsHeading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var UserMiseryContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var StatNumber = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: 32px;\n  margin-bottom: ", ";\n  color: ", ";\n\n  > div {\n    text-align: left;\n  }\n"], ["\n  font-size: 32px;\n  margin-bottom: ", ";\n  color: ", ";\n\n  > div {\n    text-align: left;\n  }\n"])), space(0.5), function (p) { return p.theme.textColor; });
var SectionValue = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
export default UserStats;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=userStats.jsx.map