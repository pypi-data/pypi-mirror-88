import React from 'react';
import VitalsCardDiscoverQuery from 'app/views/performance/vitalDetail/vitalsCardsDiscoverQuery';
import { VitalsCard } from '../vitalsCards';
export default function vitalInfo(props) {
    var vitalName = props.vitalName, eventView = props.eventView, organization = props.organization, location = props.location, hideVitalPercentNames = props.hideVitalPercentNames, hideDurationDetail = props.hideDurationDetail;
    return (<VitalsCardDiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} onlyVital={vitalName}>
      {function (_a) {
        var isLoading = _a.isLoading, tableData = _a.tableData;
        return (<React.Fragment>
          <VitalsCard tableData={tableData} isLoading={isLoading} {...props} noBorder showVitalPercentNames={!hideVitalPercentNames} showDurationDetail={!hideDurationDetail}/>
        </React.Fragment>);
    }}
    </VitalsCardDiscoverQuery>);
}
//# sourceMappingURL=vitalInfo.jsx.map