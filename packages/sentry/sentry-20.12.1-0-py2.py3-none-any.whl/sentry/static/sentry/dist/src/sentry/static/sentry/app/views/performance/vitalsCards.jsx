import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Card from 'app/components/card';
import Link from 'app/components/links/link';
import QuestionTooltip from 'app/components/questionTooltip';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { decodeList } from 'app/utils/queryString';
import VitalsCardsDiscoverQuery from 'app/views/performance/vitalDetail/vitalsCardsDiscoverQuery';
import ColorBar from './vitalDetail/colorBar';
import { vitalAbbreviations, vitalDescription, vitalDetailRouteWithQuery, vitalMap, vitalsBaseFields, vitalsMehFields, vitalsP75Fields, vitalsPoorFields, VitalState, vitalStateColors, } from './vitalDetail/utils';
import VitalPercents from './vitalDetail/vitalPercents';
import { HeaderTitle } from './styles';
export default function VitalsCards(props) {
    var eventView = props.eventView, organization = props.organization, location = props.location;
    var vitalsView = eventView.clone();
    var shownVitals = [WebVital.FCP, WebVital.LCP, WebVital.FID, WebVital.CLS];
    return (<VitalsCardsDiscoverQuery eventView={vitalsView} orgSlug={organization.slug} location={location}>
      {function (_a) {
        var isLoading = _a.isLoading, tableData = _a.tableData;
        return (<VitalsContainer>
          {props.hasCondensedVitals ? (<CondensedVitalsCard tableData={tableData} isLoading={isLoading} {...props} condensedVitals={shownVitals}/>) : (shownVitals.map(function (vitalName) { return (<LinkedVitalsCard key={vitalName} vitalName={vitalName} tableData={tableData} isLoading={isLoading} {...props}/>); }))}
        </VitalsContainer>);
    }}
    </VitalsCardsDiscoverQuery>);
}
var VitalsContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
var NonPanel = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var VitalCard = styled(Card)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  min-height: 150px;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  min-height: 150px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.textColor; }, space(2), space(3), space(2));
export function LinkedVitalsCard(props) {
    var vitalName = props.vitalName;
    return (<VitalLink {...props} vitalName={vitalName}>
      <VitalsCard {...props}/>
    </VitalLink>);
}
function getCounts(result, vitalName) {
    var base = result[getAggregateAlias(vitalsBaseFields[vitalName])];
    var poorCount = parseFloat(result[getAggregateAlias(vitalsPoorFields[vitalName])]) || 0;
    var mehTotal = parseFloat(result[getAggregateAlias(vitalsMehFields[vitalName])]) || 0;
    var mehCount = mehTotal - poorCount;
    var baseCount = parseFloat(base) || Number.MIN_VALUE;
    var goodCount = baseCount - mehCount - poorCount;
    return {
        poorCount: poorCount,
        mehCount: mehCount,
        goodCount: goodCount,
        baseCount: baseCount,
    };
}
function getPercentsFromCounts(_a) {
    var poorCount = _a.poorCount, mehCount = _a.mehCount, goodCount = _a.goodCount, baseCount = _a.baseCount;
    var poorPercent = poorCount / baseCount;
    var mehPercent = mehCount / baseCount;
    var goodPercent = goodCount / baseCount;
    var percents = [
        {
            vitalState: VitalState.GOOD,
            percent: goodPercent,
        },
        {
            vitalState: VitalState.MEH,
            percent: mehPercent,
        },
        {
            vitalState: VitalState.POOR,
            percent: poorPercent,
        },
    ];
    return percents;
}
function getColorStopsFromPercents(percents) {
    return percents.map(function (_a) {
        var percent = _a.percent, vitalState = _a.vitalState;
        return ({
            percent: percent,
            color: vitalStateColors[vitalState],
        });
    });
}
export function VitalsCard(props) {
    var isLoading = props.isLoading, tableData = props.tableData, vitalName = props.vitalName, noBorder = props.noBorder, hideBar = props.hideBar;
    var measurement = vitalMap[vitalName];
    if (isLoading || !tableData || !tableData.data || !tableData.data[0]) {
        return <BlankCard noBorder={noBorder} measurement={measurement}/>;
    }
    var result = tableData.data[0];
    var base = result[getAggregateAlias(vitalsBaseFields[vitalName])];
    if (!base) {
        return <BlankCard noBorder={noBorder} measurement={measurement}/>;
    }
    var percents = getPercentsFromCounts(getCounts(result, vitalName));
    var p75 = parseFloat(result[getAggregateAlias(vitalsP75Fields[vitalName])]) || 0;
    var value = vitalName === WebVital.CLS ? p75.toFixed(2) : p75.toFixed(0);
    return (<VitalsCardContent percents={percents} showVitalPercentNames={props.showVitalPercentNames} showDurationDetail={props.showDurationDetail} title={measurement} titleDescription={vitalName ? vitalDescription[vitalName] || '' : ''} value={"" + value + (vitalName === WebVital.CLS ? '' : t('ms'))} noBorder={noBorder} hideBar={hideBar}/>);
}
/**
 * To aggregate and visualize all vital counts in returned data.
 */
function CondensedVitalsCard(props) {
    var isLoading = props.isLoading, tableData = props.tableData;
    if (isLoading || !tableData || !tableData.data || !tableData.data[0]) {
        return <BlankCard noBorder/>;
    }
    var result = tableData.data[0];
    var vitals = props.condensedVitals;
    var allCounts = {
        poorCount: 0,
        mehCount: 0,
        goodCount: 0,
        baseCount: 0,
    };
    vitals.forEach(function (vitalName) {
        var counts = getCounts(result, vitalName);
        Object.keys(counts).forEach(function (countKey) { return (allCounts[countKey] += counts[countKey]); });
    });
    if (!allCounts.baseCount) {
        return <BlankCard noBorder/>;
    }
    var percents = getPercentsFromCounts(allCounts);
    return (<VitalsCardContent noBorder percents={percents} showVitalPercentNames={props.showVitalPercentNames} showDurationDetail={props.showDurationDetail}/>);
}
function VitalsCardContent(props) {
    var percents = props.percents, noBorder = props.noBorder, title = props.title, titleDescription = props.titleDescription, value = props.value, showVitalPercentNames = props.showVitalPercentNames, showDurationDetail = props.showDurationDetail, hideBar = props.hideBar;
    var Container = noBorder ? NonPanel : VitalCard;
    var colorStops = getColorStopsFromPercents(percents);
    return (<Container interactive>
      {noBorder || (<HeaderTitle>
          <OverflowEllipsis>{t("" + title)}</OverflowEllipsis>
          <QuestionTooltip size="sm" position="top" title={titleDescription}/>
        </HeaderTitle>)}
      {noBorder || <CardValue>{value}</CardValue>}
      {!hideBar && <ColorBar colorStops={colorStops}/>}
      <BarDetail>
        {showDurationDetail && (<div>
            {t('The p75 for all transactions is ')}
            <strong>{value}</strong>
          </div>)}
        <VitalPercents percents={percents} showVitalPercentNames={showVitalPercentNames}/>
      </BarDetail>
    </Container>);
}
var BlankCard = function (props) {
    var Container = props.noBorder ? NonPanel : VitalCard;
    return (<Container interactive>
      {props.noBorder || (<HeaderTitle>
          <OverflowEllipsis>{t("" + props.measurement)}</OverflowEllipsis>
        </HeaderTitle>)}
      <CardValue>{'\u2014'}</CardValue>
    </Container>);
};
var VitalLink = function (props) {
    var organization = props.organization, eventView = props.eventView, vitalName = props.vitalName, children = props.children, location = props.location;
    var view = eventView.clone();
    var target = vitalDetailRouteWithQuery({
        orgSlug: organization.slug,
        query: view.generateQueryStringObject(),
        vitalName: vitalName,
        projectID: decodeList(location.query.project),
    });
    return (<Link to={target} data-test-id={"vitals-linked-card-" + vitalAbbreviations[vitalName]}>
      {children}
    </Link>);
};
var BarDetail = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"], ["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; });
var CardValue = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 32px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: 32px;\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(1), space(1.5));
var OverflowEllipsis = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=vitalsCards.jsx.map