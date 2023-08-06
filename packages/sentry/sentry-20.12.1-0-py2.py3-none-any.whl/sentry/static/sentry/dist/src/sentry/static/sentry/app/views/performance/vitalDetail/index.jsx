import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import { WebVital } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { generatePerformanceVitalDetailView } from '../data';
import { addRoutePerformanceContext, getTransactionName } from '../utils';
import VitalDetailContent from './vitalDetailContent';
var VitalDetail = /** @class */ (function (_super) {
    __extends(VitalDetail, _super);
    function VitalDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generatePerformanceVitalDetailView(_this.props.organization, _this.props.location),
        };
        return _this;
    }
    VitalDetail.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generatePerformanceVitalDetailView(nextProps.organization, nextProps.location) });
    };
    VitalDetail.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
    };
    VitalDetail.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    VitalDetail.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Performance')].join(' - ');
        }
        return [t('Vital Detail'), t('Performance')].join(' - ');
    };
    VitalDetail.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, router = _a.router;
        var eventView = this.state.eventView;
        if (!eventView) {
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var vitalNameQuery = decodeScalar(location.query.vitalName);
        var vitalName = Object.values(WebVital).indexOf(vitalNameQuery) === -1
            ? undefined
            : vitalNameQuery;
        return (<SentryDocumentTitle title={this.getDocumentTitle()} objSlug={organization.slug}>
        <GlobalSelectionHeader>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <VitalDetailContent location={location} organization={organization} eventView={eventView} router={router} vitalName={vitalName || WebVital.LCP}/>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return VitalDetail;
}(React.Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
export default withApi(withGlobalSelection(withProjects(withOrganization(VitalDetail))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map