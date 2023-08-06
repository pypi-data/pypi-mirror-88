import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import moment from 'moment-timezone';
import DateTime from 'app/components/dateTime';
import FileSize from 'app/components/fileSize';
import ExternalLink from 'app/components/links/externalLink';
import NavigationButtonGroup from 'app/components/navigationButtonGroup';
import Tooltip from 'app/components/tooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
var formatDateDelta = function (reference, observed) {
    var duration = moment.duration(Math.abs(+observed - +reference));
    var hours = Math.floor(+duration / (60 * 60 * 1000));
    var minutes = duration.minutes();
    var results = [];
    if (hours) {
        results.push(hours + " hour" + (hours !== 1 ? 's' : ''));
    }
    if (minutes) {
        results.push(minutes + " minute" + (minutes !== 1 ? 's' : ''));
    }
    if (results.length === 0) {
        results.push('a few seconds');
    }
    return results.join(', ');
};
var GroupEventToolbar = /** @class */ (function (_super) {
    __extends(GroupEventToolbar, _super);
    function GroupEventToolbar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GroupEventToolbar.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event.id !== nextProps.event.id;
    };
    GroupEventToolbar.prototype.getDateTooltip = function () {
        var _a;
        var evt = this.props.event;
        var user = ConfigStore.get('user');
        var options = (_a = user === null || user === void 0 ? void 0 : user.options) !== null && _a !== void 0 ? _a : {};
        var format = options.clock24Hours ? 'HH:mm:ss z' : 'LTS z';
        var dateCreated = moment(evt.dateCreated);
        var dateReceived = evt.dateReceived ? moment(evt.dateReceived) : null;
        return (<DescriptionList className="flat">
        <dt>Occurred</dt>
        <dd>
          {dateCreated.format('ll')}
          <br />
          {dateCreated.format(format)}
        </dd>
        {dateReceived && (<React.Fragment>
            <dt>Received</dt>
            <dd>
              {dateReceived.format('ll')}
              <br />
              {dateReceived.format(format)}
            </dd>
            <dt>Latency</dt>
            <dd>{formatDateDelta(dateCreated, dateReceived)}</dd>
          </React.Fragment>)}
      </DescriptionList>);
    };
    GroupEventToolbar.prototype.render = function () {
        var evt = this.props.event;
        var _a = this.props, orgId = _a.orgId, location = _a.location;
        var groupId = this.props.group.id;
        var baseEventsPath = "/organizations/" + orgId + "/issues/" + groupId + "/events/";
        // TODO: possible to define this as a route in react-router, but without a corresponding
        //       React component?
        var jsonUrl = "/organizations/" + orgId + "/issues/" + groupId + "/events/" + evt.id + "/json/";
        var latencyThreshold = 30 * 60 * 1000; // 30 minutes
        var isOverLatencyThreshold = evt.dateReceived &&
            Math.abs(+moment(evt.dateReceived) - +moment(evt.dateCreated)) > latencyThreshold;
        return (<Wrapper>
        <StyledNavigationButtonGroup location={location} hasPrevious={!!evt.previousEventID} hasNext={!!evt.nextEventID} urls={[
            baseEventsPath + "oldest/",
            "" + baseEventsPath + evt.previousEventID + "/",
            "" + baseEventsPath + evt.nextEventID + "/",
            baseEventsPath + "latest/",
        ]}/>
        <Heading>
          {t('Event')}{' '}
          <EventIdLink to={"" + baseEventsPath + evt.id + "/"}>{evt.eventID}</EventIdLink>
        </Heading>
        <Tooltip title={this.getDateTooltip()} disableForVisualTest>
          <StyledDateTime date={getDynamicText({ value: evt.dateCreated, fixed: 'Dummy timestamp' })}/>
          {isOverLatencyThreshold && <StyledIconWarning color="yellow300"/>}
        </Tooltip>
        <JsonLink href={jsonUrl}>
          {'JSON'} (<FileSize bytes={evt.size}/>)
        </JsonLink>
      </Wrapper>);
    };
    return GroupEventToolbar;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  margin-bottom: -5px;\n  /* z-index seems unnecessary, but increasing (instead of removing) just in case(billy) */\n  /* Fixes tooltips in toolbar having lower z-index than .btn-group .btn.active */\n  z-index: 3;\n  padding: 20px 30px 20px 40px;\n\n  @media (max-width: 767px) {\n    display: none;\n  }\n"], ["\n  position: relative;\n  margin-bottom: -5px;\n  /* z-index seems unnecessary, but increasing (instead of removing) just in case(billy) */\n  /* Fixes tooltips in toolbar having lower z-index than .btn-group .btn.active */\n  z-index: 3;\n  padding: 20px 30px 20px 40px;\n\n  @media (max-width: 767px) {\n    display: none;\n  }\n"])));
var EventIdLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: normal;\n"], ["\n  font-weight: normal;\n"])));
var Heading = styled('h4')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  line-height: 1.3;\n  margin: 0;\n  font-size: ", ";\n"], ["\n  line-height: 1.3;\n  margin: 0;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledNavigationButtonGroup = styled(NavigationButtonGroup)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  float: right;\n"], ["\n  float: right;\n"])));
var StyledIconWarning = styled(IconWarning)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  position: relative;\n  top: ", ";\n"], ["\n  margin-left: ", ";\n  position: relative;\n  top: ", ";\n"])), space(0.5), space(0.25));
var StyledDateTime = styled(DateTime)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  border-bottom: 1px dotted #dfe3ea;\n  color: ", ";\n"], ["\n  border-bottom: 1px dotted #dfe3ea;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var JsonLink = styled(ExternalLink)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"])), space(1), space(1), function (p) { return p.theme.border; });
var DescriptionList = styled('dl')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  text-align: left;\n  margin: 0;\n  min-width: 200px;\n  max-width: 250px;\n"], ["\n  text-align: left;\n  margin: 0;\n  min-width: 200px;\n  max-width: 250px;\n"])));
export default GroupEventToolbar;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=eventToolbar.jsx.map