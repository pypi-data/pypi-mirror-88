import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import FeatureTourModal, { TourImage, TourText, } from 'app/components/modals/featureTourModal';
import OnboardingPanel from 'app/components/onboardingPanel';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import AsyncView from 'app/views/asyncView';
import emptyStateImg from '../../../../images/spot/releases-empty-state.svg';
import commitImage from '../../../../images/spot/releases-tour-commits.svg';
import emailImage from '../../../../images/spot/releases-tour-email.svg';
import resolutionImage from '../../../../images/spot/releases-tour-resolution.svg';
import statsImage from '../../../../images/spot/releases-tour-stats.svg';
var releasesSetupUrl = 'https://docs.sentry.io/product/releases/';
var docsLink = (<Button external href={releasesSetupUrl}>
    {t('Setup')}
  </Button>);
export var RELEASES_TOUR_STEPS = [
    {
        title: t('Suspect Commits'),
        image: <TourImage src={commitImage}/>,
        body: (<TourText>
        {t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Release Stats'),
        image: <TourImage src={statsImage}/>,
        body: (<TourText>
        {t('Get an overview of the commits in each release, and which issues were introduced or fixed.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Easily Resolve'),
        image: <TourImage src={resolutionImage}/>,
        body: (<TourText>
        {t('Automatically resolve issues by including the issue number in your commit message.')}
      </TourText>),
        actions: docsLink,
    },
    {
        title: t('Deploy Emails'),
        image: <TourImage src={emailImage}/>,
        body: (<TourText>
        {t('Receive email notifications about when your code gets deployed. This can be customized in settings.')}
      </TourText>),
    },
];
var ReleaseLanding = /** @class */ (function (_super) {
    __extends(ReleaseLanding, _super);
    function ReleaseLanding() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // if there are no releases in the last 30 days, we want to show releases promo, otherwise empty message
    ReleaseLanding.prototype.getEndpoints = function () {
        var slug = this.props.organization.slug;
        var query = {
            per_page: 1,
            summaryStatsPeriod: '30d',
        };
        return [['releases', "/organizations/" + slug + "/releases/", { query: query }]];
    };
    ReleaseLanding.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        if (this.state.releases.length === 0) {
            return <Promo organization={organization} projectId={projectId}/>;
        }
        return <EmptyStateWarning small>{t('There are no releases.')}</EmptyStateWarning>;
    };
    return ReleaseLanding;
}(AsyncView));
var Promo = /** @class */ (function (_super) {
    __extends(Promo, _super);
    function Promo() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTourAdvance = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            trackAnalyticsEvent({
                eventKey: 'releases.tour.advance',
                eventName: 'Releases: Tour Advance',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        _this.handleClose = function (step, duration) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            trackAnalyticsEvent({
                eventKey: 'releases.tour.close',
                eventName: 'Releases: Tour Close',
                organization_id: parseInt(organization.id, 10),
                project_id: projectId,
                step: step,
                duration: duration,
            });
        };
        return _this;
    }
    Promo.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        trackAnalyticsEvent({
            eventKey: 'releases.landing_card_viewed',
            eventName: 'Releases: Landing Card Viewed',
            organization_id: parseInt(organization.id, 10),
            project_id: projectId,
        });
    };
    Promo.prototype.render = function () {
        return (<OnboardingPanel image={<img src={emptyStateImg}/>}>
        <h3>{t('Demystify Releases')}</h3>
        <p>
          {t('Did you know how many errors your latest release triggered? We do. And more, too.')}
        </p>
        <ButtonList gap={1}>
          <FeatureTourModal steps={RELEASES_TOUR_STEPS} onAdvance={this.handleTourAdvance} onCloseModal={this.handleClose} doneText={t('Start Setup')} doneUrl={releasesSetupUrl}>
            {function (_a) {
            var showModal = _a.showModal;
            return (<Button priority="default" onClick={showModal}>
                {t('Take a Tour')}
              </Button>);
        }}
          </FeatureTourModal>
          <Button priority="primary" href={releasesSetupUrl} external>
            {t('Start Setup')}
          </Button>
        </ButtonList>
      </OnboardingPanel>);
    };
    return Promo;
}(React.Component));
var ButtonList = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default ReleaseLanding;
var templateObject_1;
//# sourceMappingURL=releaseLanding.jsx.map