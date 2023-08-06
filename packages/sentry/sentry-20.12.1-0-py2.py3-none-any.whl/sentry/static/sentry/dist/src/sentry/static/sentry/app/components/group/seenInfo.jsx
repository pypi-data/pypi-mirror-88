import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import DateTime from 'app/components/dateTime';
import { Body, Header, Hovercard } from 'app/components/hovercard';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import VersionHoverCard from 'app/components/versionHoverCard';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined, toTitleCase } from 'app/utils';
import theme from 'app/utils/theme';
var SeenInfo = /** @class */ (function (_super) {
    __extends(SeenInfo, _super);
    function SeenInfo() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SeenInfo.prototype.shouldComponentUpdate = function (nextProps) {
        var _a;
        var _b = this.props, date = _b.date, release = _b.release;
        return (release === null || release === void 0 ? void 0 : release.version) !== ((_a = nextProps.release) === null || _a === void 0 ? void 0 : _a.version) || date !== nextProps.date;
    };
    SeenInfo.prototype.getReleaseTrackingUrl = function () {
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
        return "/settings/" + orgSlug + "/projects/" + projectSlug + "/release-tracking/";
    };
    SeenInfo.prototype.render = function () {
        var _a = this.props, date = _a.date, dateGlobal = _a.dateGlobal, environment = _a.environment, release = _a.release, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, projectId = _a.projectId;
        return (<HovercardWrapper>
        <StyledHovercard header={<div>
              <TimeSinceWrapper>
                {t('Any Environment')}
                <TimeSince date={dateGlobal} disabledAbsoluteTooltip/>
              </TimeSinceWrapper>
              {environment && (<TimeSinceWrapper>
                  {toTitleCase(environment)}
                  <TimeSince date={date} disabledAbsoluteTooltip/>
                </TimeSinceWrapper>)}
            </div>} body={<StyledDateTime date={date}/>} position="top" tipColor={theme.gray500}>
          <DateWrapper>
            {date ? (<TooltipWrapper>
                <StyledTimeSince date={date} disabledAbsoluteTooltip/>
              </TooltipWrapper>) : dateGlobal && environment === '' ? (<React.Fragment>
                <TimeSince date={dateGlobal} disabledAbsoluteTooltip/>
                <StyledTimeSince date={dateGlobal} disabledAbsoluteTooltip/>
              </React.Fragment>) : (<React.Fragment>{t('n/a')} </React.Fragment>)}
          </DateWrapper>
        </StyledHovercard>
        <DateWrapper>
          {defined(release) ? (<React.Fragment>
              {t('in release ')}
              <VersionHoverCard orgSlug={orgSlug} projectSlug={projectSlug} releaseVersion={release.version}>
                <span>
                  <Version version={release.version} projectId={projectId}/>
                </span>
              </VersionHoverCard>
            </React.Fragment>) : null}
        </DateWrapper>
      </HovercardWrapper>);
    };
    SeenInfo.propTypes = {
        orgSlug: PropTypes.string.isRequired,
        projectSlug: PropTypes.string.isRequired,
        projectId: PropTypes.string.isRequired,
        date: PropTypes.any,
        dateGlobal: PropTypes.any,
        release: PropTypes.shape({
            version: PropTypes.string.isRequired,
        }),
        environment: PropTypes.string,
    };
    SeenInfo.contextTypes = {
        organization: PropTypes.object,
    };
    return SeenInfo;
}(React.Component));
var HovercardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var DateWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  margin-bottom: ", ";\n  ", ";\n"])), space(2), overflowEllipsis);
var StyledDateTime = styled(DateTime)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  display: flex;\n  justify-content: center;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  display: flex;\n  justify-content: center;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var TooltipWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n"], ["\n  margin-right: ", ";\n  svg {\n    margin-right: ", ";\n    position: relative;\n    top: 1px;\n  }\n"])), space(0.25), space(0.5));
var TimeSinceWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n  display: flex;\n  justify-content: space-between;\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n  display: flex;\n  justify-content: space-between;\n"])), function (p) { return p.theme.fontSizeSmall; }, space(0.5));
var StyledTimeSince = styled(TimeSince)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledHovercard = styled(Hovercard)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: 250px;\n  font-weight: normal;\n  border: 1px solid ", ";\n  background: ", ";\n  ", " {\n    font-weight: normal;\n    color: ", ";\n    background: ", ";\n    border-bottom: 1px solid ", ";\n  }\n  ", " {\n    padding: ", ";\n  }\n"], ["\n  width: 250px;\n  font-weight: normal;\n  border: 1px solid ", ";\n  background: ", ";\n  ", " {\n    font-weight: normal;\n    color: ", ";\n    background: ", ";\n    border-bottom: 1px solid ", ";\n  }\n  ", " {\n    padding: ", ";\n  }\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray500; }, Header, function (p) { return p.theme.white; }, function (p) { return p.theme.gray500; }, function (p) { return p.theme.gray400; }, Body, space(1.5));
export default SeenInfo;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=seenInfo.jsx.map