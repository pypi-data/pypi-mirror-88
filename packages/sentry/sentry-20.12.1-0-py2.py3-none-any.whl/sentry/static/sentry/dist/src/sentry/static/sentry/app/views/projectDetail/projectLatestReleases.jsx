import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import AsyncComponent from 'app/components/asyncComponent';
import { SectionHeading } from 'app/components/charts/styles';
import DateTime from 'app/components/dateTime';
import Placeholder from 'app/components/placeholder';
import TextOverflow from 'app/components/textOverflow';
import Version from 'app/components/version';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import { RELEASES_TOUR_STEPS } from 'app/views/releases/list/releaseLanding';
import MissingReleasesButtons from './missingFeatureButtons/missingReleasesButtons';
var ProjectLatestReleases = /** @class */ (function (_super) {
    __extends(ProjectLatestReleases, _super);
    function ProjectLatestReleases() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTourAdvance = function (index) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            analytics('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: projectId && parseInt(projectId, 10),
                step_id: index,
                step_title: RELEASES_TOUR_STEPS[index].title,
            });
        };
        _this.renderReleaseRow = function (release) {
            var projectId = _this.props.projectId;
            var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated;
            return (<React.Fragment key={release.version}>
        <DateTime date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated} seconds={false}/>
        <TextOverflow>
          <StyledVersion version={release.version} tooltipRawVersion projectId={projectId}/>
        </TextOverflow>
      </React.Fragment>);
        };
        return _this;
    }
    ProjectLatestReleases.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (this.state !== nextState ||
            !isEqual(pick(this.props.location.query, Object.values(URL_PARAM)), pick(nextProps.location.query, Object.values(URL_PARAM)))) {
            return true;
        }
        return false;
    };
    ProjectLatestReleases.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, projectSlug = _a.projectSlug;
        var query = __assign(__assign({}, pick(location.query, Object.values(URL_PARAM))), { per_page: 5 });
        // TODO(project-detail): this does not filter releases for the given time
        return [
            ['releases', "/projects/" + organization.slug + "/" + projectSlug + "/releases/", { query: query }],
        ];
    };
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    ProjectLatestReleases.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var releases, _a, organization, projectSlug, oldReleases;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        releases = this.state.releases;
                        _a = this.props, organization = _a.organization, projectSlug = _a.projectSlug;
                        if ((releases !== null && releases !== void 0 ? releases : []).length !== 0) {
                            this.setState({ hasOlderReleases: true });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/releases/", {
                                method: 'GET',
                                query: {
                                    statsPeriod: '90d',
                                    per_page: 1,
                                },
                            })];
                    case 1:
                        oldReleases = _b.sent();
                        this.setState({ hasOlderReleases: oldReleases.length > 0, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    ProjectLatestReleases.prototype.renderInnerBody = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        var _b = this.state, loading = _b.loading, releases = _b.releases, hasOlderReleases = _b.hasOlderReleases;
        var checkingForOlderReleases = !(releases !== null && releases !== void 0 ? releases : []).length && hasOlderReleases === undefined;
        var showLoadingIndicator = loading || checkingForOlderReleases;
        if (showLoadingIndicator) {
            return <Placeholder height="160px"/>;
        }
        if (!hasOlderReleases) {
            return <MissingReleasesButtons organization={organization} projectId={projectId}/>;
        }
        if (!releases || releases.length === 0) {
            return t('No releases match the filter.');
        }
        return <ReleasesTable>{releases.map(this.renderReleaseRow)}</ReleasesTable>;
    };
    ProjectLatestReleases.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectLatestReleases.prototype.renderBody = function () {
        return (<Section>
        <SectionHeading>{t('Latest Releases')}</SectionHeading>
        <div>{this.renderInnerBody()}</div>
      </Section>);
    };
    return ProjectLatestReleases;
}(AsyncComponent));
var Section = styled('section')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var ReleasesTable = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  font-size: ", ";\n  white-space: nowrap;\n  grid-template-columns: 1fr auto;\n  margin-bottom: ", ";\n\n  & > * {\n    padding: ", " ", ";\n    height: 32px;\n  }\n\n  & > *:nth-child(2n + 2) {\n    text-align: right;\n  }\n\n  & > *:nth-child(4n + 1),\n  & > *:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"], ["\n  display: grid;\n  font-size: ", ";\n  white-space: nowrap;\n  grid-template-columns: 1fr auto;\n  margin-bottom: ", ";\n\n  & > * {\n    padding: ", " ", ";\n    height: 32px;\n  }\n\n  & > *:nth-child(2n + 2) {\n    text-align: right;\n  }\n\n  & > *:nth-child(4n + 1),\n  & > *:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, space(2), space(0.5), space(1), function (p) { return p.theme.rowBackground; });
var StyledVersion = styled(Version)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
export default ProjectLatestReleases;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectLatestReleases.jsx.map