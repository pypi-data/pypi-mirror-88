import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import ActionLink from 'app/components/actions/actionLink';
import ResolveActions from 'app/components/actions/resolve';
import DropdownLink from 'app/components/dropdownLink';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconEllipsis, IconIssues } from 'app/icons';
import { t } from 'app/locale';
import { ResolutionStatus } from 'app/types';
import Projects from 'app/utils/projects';
import withApi from 'app/utils/withApi';
var GroupRowActions = /** @class */ (function (_super) {
    __extends(GroupRowActions, _super);
    function GroupRowActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleUpdate = function (data) {
            var _a = _this.props, api = _a.api, group = _a.group, orgId = _a.orgId, query = _a.query, selection = _a.selection;
            addLoadingMessage(t('Saving changes\u2026'));
            api.bulkUpdate(__assign({ orgId: orgId, itemIds: [group.id], data: data,
                query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                complete: function () {
                    clearIndicators();
                },
            });
        };
        _this.handleDelete = function () {
            var _a = _this.props, api = _a.api, group = _a.group, orgId = _a.orgId, query = _a.query, selection = _a.selection;
            addLoadingMessage(t('Removing events\u2026'));
            api.bulkDelete(__assign({ orgId: orgId, itemIds: [group.id], query: query, project: selection.projects, environment: selection.environments }, selection.datetime), {
                complete: function () {
                    clearIndicators();
                },
            });
        };
        return _this;
    }
    GroupRowActions.prototype.render = function () {
        var _this = this;
        var _a = this.props, orgId = _a.orgId, group = _a.group;
        return (<Wrapper>
        <Tooltip title={t('Mark Reviewed')}>
          <ActionLink className="btn btn-default btn-sm" onAction={function () { return _this.handleUpdate({ inbox: false }); }} shouldConfirm={false} title={t('Mark Reviewed')}>
            <IconIssues size="sm" color="gray300"/>
          </ActionLink>
        </Tooltip>

        <StyledDropdownLink caret={false} className="btn btn-sm btn-default action-more" customTitle={<IconEllipsis size="sm" color="gray300"/>} title="" anchorRight>
          <MenuItem noAnchor>
            <ActionLink className="action-resolve" onAction={function () { return _this.handleUpdate({ status: ResolutionStatus.RESOLVED }); }} shouldConfirm={false} title={t('Resolve')}>
              {t('Resolve')}
            </ActionLink>
          </MenuItem>
          <MenuItem divider/>
          <MenuItem noAnchor>
            <Projects orgId={orgId} slugs={[group.project.slug]}>
              {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
            var project = projects[0];
            return (<ResolveActions hasRelease={project.hasOwnProperty('features')
                ? project.features.includes('releases')
                : false} latestRelease={project.hasOwnProperty('latestRelease')
                ? project.latestRelease
                : undefined} orgId={orgId} projectId={group.project.id} onUpdate={_this.handleUpdate} shouldConfirm={false} hasInbox disabled={!!fetchError} disableDropdown={!initiallyLoaded || !!fetchError} projectFetchError={!!fetchError}/>);
        }}
            </Projects>
          </MenuItem>
          <MenuItem divider/>
          <MenuItem noAnchor>
            <ActionLink className="action-delete" onAction={this.handleDelete} shouldConfirm={false} title={t('Delete')}>
              {t('Delete')}
            </ActionLink>
          </MenuItem>
        </StyledDropdownLink>
      </Wrapper>);
    };
    return GroupRowActions;
}(React.Component));
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  justify-content: space-between;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n"])));
export default withApi(GroupRowActions);
var templateObject_1, templateObject_2;
//# sourceMappingURL=groupRowActions.jsx.map