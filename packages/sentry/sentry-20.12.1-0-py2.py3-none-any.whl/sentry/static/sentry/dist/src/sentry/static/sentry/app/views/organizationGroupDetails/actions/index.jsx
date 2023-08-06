import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import GroupActions from 'app/actions/groupActions';
import IgnoreActions from 'app/components/actions/ignore';
import ResolveActions from 'app/components/actions/resolve';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Link from 'app/components/links/link';
import ShareIssue from 'app/components/shareIssue';
import Tooltip from 'app/components/tooltip';
import { IconRefresh, IconStar } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import EventView from 'app/utils/discover/eventView';
import { uniqueId } from 'app/utils/guid';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import ReprocessingDialogForm from 'app/views/organizationGroupDetails/reprocessingDialogForm';
import SubscribeAction from '../subscribeAction';
import DeleteAction from './deleteAction';
var Actions = /** @class */ (function (_super) {
    __extends(Actions, _super);
    function Actions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shareBusy: false,
        };
        _this.onDelete = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            addLoadingMessage(t('Delete event\u2026'));
            api.bulkDelete({
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
            }, {
                complete: function () {
                    clearIndicators();
                    browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
            });
        };
        _this.onUpdate = function (data) {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            addLoadingMessage(t('Saving changes\u2026'));
            api.bulkUpdate({
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
                data: data,
            }, {
                complete: clearIndicators,
            });
        };
        _this.onReprocess = function () {
            var _a = _this.props, group = _a.group, organization = _a.organization, project = _a.project;
            openModal(function (_a) {
                var closeModal = _a.closeModal, Header = _a.Header, Body = _a.Body;
                return (<ReprocessingDialogForm group={group} project={project} orgSlug={organization.slug} closeModal={closeModal} Header={Header} Body={Body}/>);
            });
        };
        _this.onToggleShare = function () {
            _this.onShare(!_this.props.group.isPublic);
        };
        _this.onToggleBookmark = function () {
            _this.onUpdate({ isBookmarked: !_this.props.group.isBookmarked });
        };
        _this.onToggleSubscribe = function () {
            _this.onUpdate({ isSubscribed: !_this.props.group.isSubscribed });
        };
        _this.onDiscard = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            var id = uniqueId();
            addLoadingMessage(t('Discarding event\u2026'));
            GroupActions.discard(id, group.id);
            api.request("/issues/" + group.id + "/", {
                method: 'PUT',
                data: { discard: true },
                success: function (response) {
                    GroupActions.discardSuccess(id, group.id, response);
                    browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
                error: function (error) {
                    GroupActions.discardError(id, group.id, error);
                },
                complete: clearIndicators,
            });
        };
        return _this;
    }
    Actions.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.state.shareBusy && nextProps.group.shareId !== this.props.group.shareId) {
            this.setState({ shareBusy: false });
        }
    };
    Actions.prototype.getShareUrl = function (shareId) {
        if (!shareId) {
            return '';
        }
        var path = "/share/issue/" + shareId + "/";
        var _a = window.location, host = _a.host, protocol = _a.protocol;
        return protocol + "//" + host + path;
    };
    Actions.prototype.getDiscoverUrl = function () {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization;
        var title = group.title, id = group.id, type = group.type;
        var discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user', 'timestamp'],
            orderby: '-timestamp',
            query: "issue.id:" + id,
            projects: [Number(project.id)],
            version: 2,
            range: '90d',
        };
        var discoverView = EventView.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    };
    Actions.prototype.onShare = function (shared) {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
        this.setState({ shareBusy: true });
        // not sure why this is a bulkUpdate
        api.bulkUpdate({
            orgId: organization.slug,
            projectId: project.slug,
            itemIds: [group.id],
            data: {
                isPublic: shared,
            },
        }, {
            error: function () {
                addErrorMessage(t('Error sharing'));
            },
            complete: function () {
                // shareBusy marked false in componentWillReceiveProps to sync
                // busy state update with shareId update
            },
        });
    };
    Actions.prototype.handleClick = function (disabled, onClick) {
        return function (event) {
            if (disabled) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            onClick(event);
        };
    };
    Actions.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, group = _b.group, project = _b.project, organization = _b.organization, disabled = _b.disabled;
        var status = group.status, isBookmarked = group.isBookmarked;
        var orgFeatures = new Set(organization.features);
        var projectFeatures = new Set(project.features);
        var buttonClassName = 'btn btn-default btn-sm';
        var bookmarkTitle = isBookmarked ? t('Remove bookmark') : t('Bookmark');
        var hasRelease = !!((_a = project.features) === null || _a === void 0 ? void 0 : _a.includes('releases'));
        var isResolved = status === 'resolved';
        var isIgnored = status === 'ignored';
        if (disabled) {
            buttonClassName = buttonClassName + " disabled";
        }
        return (<div className="group-actions">
        <GuideAnchor target="resolve" position="bottom" offset={space(3)}>
          <ResolveActions disabled={disabled} hasRelease={hasRelease} latestRelease={project.latestRelease} onUpdate={this.onUpdate} orgId={organization.slug} projectId={project.slug} isResolved={isResolved} isAutoResolved={isResolved && group.statusDetails.autoResolved}/>
        </GuideAnchor>
        <GuideAnchor target="ignore_delete_discard" position="bottom" offset={space(3)}>
          <IgnoreActions isIgnored={isIgnored} onUpdate={this.onUpdate} disabled={disabled}/>
        </GuideAnchor>
        <DeleteAction disabled={disabled} organization={organization} project={project} onDelete={this.onDelete} onDiscard={this.onDiscard}/>
        {orgFeatures.has('shared-issues') && (<div className="btn-group">
            <ShareIssue disabled={disabled} loading={this.state.shareBusy} isShared={group.isPublic} shareUrl={this.getShareUrl(group.shareId)} onToggle={this.onToggleShare} onReshare={function () { return _this.onShare(true); }}/>
          </div>)}
        {orgFeatures.has('discover-basic') && (<div className="btn-group">
            <Link className={buttonClassName} title={t('Open in Discover')} to={disabled ? '' : this.getDiscoverUrl()}>
              {t('Open in Discover')}
            </Link>
          </div>)}
        <div className="btn-group">
          <BookmarkButton className={buttonClassName} role="button" isActive={group.isBookmarked} title={bookmarkTitle} aria-label={bookmarkTitle} onClick={this.handleClick(disabled, this.onToggleBookmark)}>
            <IconWrapper>
              <IconStar isSolid size="xs"/>
            </IconWrapper>
          </BookmarkButton>
        </div>
        <SubscribeAction group={group} onClick={this.handleClick(disabled, this.onToggleSubscribe)} className={buttonClassName}/>
        {projectFeatures.has('reprocessing-v2') && (<div className="btn-group">
            <Tooltip title={t('Reprocess this issue')}>
              <div className={buttonClassName} onClick={this.handleClick(disabled, this.onReprocess)}>
                <IconWrapper>
                  <IconRefresh size="xs"/>
                </IconWrapper>
              </div>
            </Tooltip>
          </div>)}
      </div>);
    };
    return Actions;
}(React.Component));
var IconWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var BookmarkButton = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.isActive &&
        "\n    background: " + p.theme.yellow100 + ";\n    color: " + p.theme.yellow300 + ";\n    border-color: " + p.theme.yellow300 + ";\n    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.15);\n  ";
});
export { Actions };
export default withApi(withOrganization(Actions));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map