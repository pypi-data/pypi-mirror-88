import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { Link, withRouter } from 'react-router';
import styled from '@emotion/styled';
import * as qs from 'query-string';
import Button from 'app/components/button';
import FeatureBadge from 'app/components/featureBadge';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelItem } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import { PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { decodeScalar } from 'app/utils/queryString';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import MonitorIcon from './monitorIcon';
var Monitors = /** @class */ (function (_super) {
    __extends(Monitors, _super);
    function Monitors() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var router = _this.context.router;
            router.push({
                pathname: location.pathname,
                query: getParams(__assign(__assign({}, (location.query || {})), { query: query })),
            });
        };
        return _this;
    }
    Monitors.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [
            [
                'monitorList',
                "/organizations/" + params.orgId + "/monitors/",
                {
                    query: location.query,
                },
            ],
        ];
    };
    Monitors.prototype.getTitle = function () {
        return "Monitors - " + this.props.params.orgId;
    };
    Monitors.prototype.renderBody = function () {
        var _a, _b;
        var _c = this.state, monitorList = _c.monitorList, monitorListPageLinks = _c.monitorListPageLinks;
        var organization = this.props.organization;
        return (<React.Fragment>
        <PageHeader>
          <HeaderTitle>
            <div>
              {t('Monitors')} <FeatureBadge type="beta"/>
            </div>
            <NewMonitorButton to={"/organizations/" + organization.slug + "/monitors/create/"} priority="primary" size="xsmall">
              {t('New Monitor')}
            </NewMonitorButton>
          </HeaderTitle>
          <StyledSearchBar query={(_b = decodeScalar((_a = qs.parse(location.search)) === null || _a === void 0 ? void 0 : _a.query)) !== null && _b !== void 0 ? _b : ''} placeholder={t('Search for monitors.')} onSearch={this.handleSearch}/>
        </PageHeader>
        <Panel>
          <PanelBody>
            {monitorList === null || monitorList === void 0 ? void 0 : monitorList.map(function (monitor) { return (<PanelItemCentered key={monitor.id}>
                <MonitorIcon status={monitor.status} size={16}/>
                <StyledLink to={"/organizations/" + organization.slug + "/monitors/" + monitor.id + "/"}>
                  {monitor.name}
                </StyledLink>
                {monitor.nextCheckIn ? (<TimeSince date={monitor.lastCheckIn}/>) : (t('n/a'))}
              </PanelItemCentered>); })}
          </PanelBody>
        </Panel>
        {monitorListPageLinks && (<Pagination pageLinks={monitorListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return Monitors;
}(AsyncView));
var HeaderTitle = styled(PageHeading)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex: 1;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  flex: 1;\n"])));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var NewMonitorButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(2));
var PanelItemCentered = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-items: center;\n  padding: 0;\n  padding-left: ", ";\n  padding-right: ", ";\n"], ["\n  align-items: center;\n  padding: 0;\n  padding-left: ", ";\n  padding-right: ", ";\n"])), space(2), space(2));
var StyledLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space(2));
export default withRouter(withOrganization(Monitors));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=monitors.jsx.map