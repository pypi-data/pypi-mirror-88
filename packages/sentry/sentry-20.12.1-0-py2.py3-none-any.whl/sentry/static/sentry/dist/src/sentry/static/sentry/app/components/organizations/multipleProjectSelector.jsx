import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import { Link } from 'react-router';
import { ClassNames } from '@emotion/core';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import Button from 'app/components/button';
import HeaderItem from 'app/components/organizations/headerItem';
import PlatformList from 'app/components/platformList';
import Tooltip from 'app/components/tooltip';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { IconProject } from 'app/icons';
import { t, tct } from 'app/locale';
import { growIn } from 'app/styles/animations';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import ProjectSelector from './projectSelector';
var MultipleProjectSelector = /** @class */ (function (_super) {
    __extends(MultipleProjectSelector, _super);
    function MultipleProjectSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hasChanges: false,
        };
        // Reset "hasChanges" state and call `onUpdate` callback
        _this.doUpdate = function () {
            _this.setState({ hasChanges: false }, _this.props.onUpdate);
        };
        /**
         * Handler for when an explicit update call should be made.
         * e.g. an "Update" button
         *
         * Should perform an "update" callback
         */
        _this.handleUpdate = function (actions) {
            actions.close();
            _this.doUpdate();
        };
        /**
         * Handler for when a dropdown item was selected directly (and not via multi select)
         *
         * Should perform an "update" callback
         */
        _this.handleQuickSelect = function (selected) {
            analytics('projectselector.direct_selection', {
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            var value = selected.id === null ? [] : [parseInt(selected.id, 10)];
            _this.props.onChange(value);
            _this.doUpdate();
        };
        /**
         * Handler for when dropdown menu closes
         *
         * Should perform an "update" callback
         */
        _this.handleClose = function () {
            // Only update if there are changes
            if (!_this.state.hasChanges) {
                return;
            }
            var _a = _this.props, value = _a.value, multi = _a.multi;
            analytics('projectselector.update', {
                count: value.length,
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
                multi: multi,
            });
            _this.doUpdate();
        };
        /**
         * Handler for clearing the current value
         *
         * Should perform an "update" callback
         */
        _this.handleClear = function () {
            analytics('projectselector.clear', {
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.props.onChange([]);
            // Update on clear
            _this.doUpdate();
        };
        /**
         * Handler for selecting multiple items, should NOT call update
         */
        _this.handleMultiSelect = function (selected) {
            var _a = _this.props, onChange = _a.onChange, value = _a.value;
            analytics('projectselector.toggle', {
                action: selected.length > value.length ? 'added' : 'removed',
                path: getRouteStringFromRoutes(_this.context.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            var selectedList = selected.map(function (_a) {
                var id = _a.id;
                return parseInt(id, 10);
            }).filter(function (i) { return i; });
            onChange(selectedList);
            _this.setState({ hasChanges: true });
        };
        return _this;
    }
    MultipleProjectSelector.prototype.renderProjectName = function () {
        var location = this.context.router.location;
        var _a = this.props, forceProject = _a.forceProject, multi = _a.multi, organization = _a.organization, showIssueStreamLink = _a.showIssueStreamLink;
        if (showIssueStreamLink && forceProject && multi) {
            return (<Tooltip title={t('Issues Stream')} position="bottom">
          <StyledLink to={{
                pathname: "/organizations/" + organization.slug + "/issues/",
                query: __assign(__assign({}, location.query), { project: forceProject.id }),
            }}>
            {forceProject.slug}
          </StyledLink>
        </Tooltip>);
        }
        if (forceProject) {
            return forceProject.slug;
        }
        return '';
    };
    MultipleProjectSelector.prototype.getLockedMessage = function () {
        var _a = this.props, forceProject = _a.forceProject, lockedMessageSubject = _a.lockedMessageSubject;
        if (forceProject) {
            return tct('This [subject] is unique to the [projectSlug] project', {
                subject: lockedMessageSubject,
                projectSlug: forceProject.slug,
            });
        }
        return tct('This [subject] is unique to a project', { subject: lockedMessageSubject });
    };
    MultipleProjectSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, value = _a.value, projects = _a.projects, isGlobalSelectionReady = _a.isGlobalSelectionReady, nonMemberProjects = _a.nonMemberProjects, multi = _a.multi, organization = _a.organization, shouldForceProject = _a.shouldForceProject, forceProject = _a.forceProject, showProjectSettingsLink = _a.showProjectSettingsLink, footerMessage = _a.footerMessage;
        var selectedProjectIds = new Set(value);
        var allProjects = __spread(projects, nonMemberProjects);
        var selected = allProjects.filter(function (project) {
            return selectedProjectIds.has(parseInt(project.id, 10));
        });
        // `forceProject` can be undefined if it is loading the project
        // We are intentionally using an empty string as its "loading" state
        return shouldForceProject ? (<StyledHeaderItem data-test-id="global-header-project-selector" icon={forceProject && (<PlatformList platforms={forceProject.platform ? [forceProject.platform] : []} max={1}/>)} locked lockedMessage={this.getLockedMessage()} settingsLink={(forceProject &&
            showProjectSettingsLink &&
            "/settings/" + organization.slug + "/projects/" + forceProject.slug + "/") ||
            undefined}>
        {this.renderProjectName()}
      </StyledHeaderItem>) : !isGlobalSelectionReady ? (<StyledHeaderItem data-test-id="global-header-project-selector-loading" icon={<IconProject />} loading>
        {t('Loading\u2026')}
      </StyledHeaderItem>) : (<ClassNames>
        {function (_a) {
            var css = _a.css;
            return (<StyledProjectSelector {..._this.props} multi={!!multi} selectedProjects={selected} multiProjects={projects} onSelect={_this.handleQuickSelect} onClose={_this.handleClose} onMultiSelect={_this.handleMultiSelect} rootClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n              display: flex;\n            "], ["\n              display: flex;\n            "])))} menuFooter={function (_a) {
                var actions = _a.actions;
                return (<SelectorFooterControls selected={selectedProjectIds} multi={multi} organization={organization} hasChanges={_this.state.hasChanges} onApply={function () { return _this.handleUpdate(actions); }} onShowAllProjects={function () {
                    _this.handleQuickSelect({ id: ALL_ACCESS_PROJECTS.toString() });
                    actions.close();
                }} onShowMyProjects={function () {
                    _this.handleClear();
                    actions.close();
                }} message={footerMessage}/>);
            }}>
            {function (_a) {
                var _b;
                var getActorProps = _a.getActorProps, selectedProjects = _a.selectedProjects, isOpen = _a.isOpen;
                var hasSelected = !!selectedProjects.length;
                var title = hasSelected
                    ? selectedProjects.map(function (_a) {
                        var slug = _a.slug;
                        return slug;
                    }).join(', ')
                    : selectedProjectIds.has(ALL_ACCESS_PROJECTS)
                        ? t('All Projects')
                        : t('My Projects');
                var icon = hasSelected ? (<PlatformList platforms={selectedProjects.map(function (p) { var _a; return (_a = p.platform) !== null && _a !== void 0 ? _a : 'other'; }).reverse()} max={5}/>) : (<IconProject />);
                return (<StyledHeaderItem data-test-id="global-header-project-selector" icon={icon} hasSelected={hasSelected} hasChanges={_this.state.hasChanges} isOpen={isOpen} onClear={_this.handleClear} allowClear={multi} settingsLink={selectedProjects.length === 1
                    ? "/settings/" + organization.slug + "/projects/" + ((_b = selected[0]) === null || _b === void 0 ? void 0 : _b.slug) + "/"
                    : ''} {...getActorProps()}>
                  {title}
                </StyledHeaderItem>);
            }}
          </StyledProjectSelector>);
        }}
      </ClassNames>);
    };
    MultipleProjectSelector.contextTypes = {
        router: PropTypes.object,
    };
    MultipleProjectSelector.defaultProps = {
        multi: true,
        lockedMessageSubject: t('page'),
    };
    return MultipleProjectSelector;
}(React.PureComponent));
export default MultipleProjectSelector;
var SelectorFooterControls = function (_a) {
    var selected = _a.selected, multi = _a.multi, hasChanges = _a.hasChanges, onApply = _a.onApply, onShowAllProjects = _a.onShowAllProjects, onShowMyProjects = _a.onShowMyProjects, organization = _a.organization, message = _a.message;
    var showMyProjects = false;
    var showAllProjects = false;
    if (multi) {
        showMyProjects = true;
        var hasGlobalRole = organization.role === 'owner' || organization.role === 'manager';
        var hasOpenMembership = organization.features.includes('open-membership');
        var allSelected = selected && selected.has(ALL_ACCESS_PROJECTS);
        if ((hasGlobalRole || hasOpenMembership) && !allSelected) {
            showAllProjects = true;
            showMyProjects = false;
        }
    }
    // Nothing to show.
    if (!(showAllProjects || showMyProjects || hasChanges || message)) {
        return null;
    }
    return (<FooterContainer>
      {message && <FooterMessage>{message}</FooterMessage>}

      <FooterActions>
        {showAllProjects && (<Button onClick={onShowAllProjects} priority="default" size="xsmall">
            {t('View All Projects')}
          </Button>)}
        {showMyProjects && (<Button onClick={onShowMyProjects} priority="default" size="xsmall">
            {t('View My Projects')}
          </Button>)}
        {hasChanges && (<SubmitButton onClick={onApply} size="xsmall" priority="primary">
            {t('Apply Filter')}
          </SubmitButton>)}
      </FooterActions>
    </FooterContainer>);
};
var FooterContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " 0;\n"], ["\n  padding: ", " 0;\n"])), space(1));
var FooterActions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  & > * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  & > * {\n    margin-left: ", ";\n  }\n"])), space(0.5));
var SubmitButton = styled(Button)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  animation: 0.1s ", " ease-in;\n"], ["\n  animation: 0.1s ", " ease-in;\n"])), growIn);
var FooterMessage = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  padding: 0 ", ";\n"], ["\n  font-size: ", ";\n  padding: 0 ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(0.5));
var StyledProjectSelector = styled(ProjectSelector)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background-color: ", ";\n  color: ", ";\n  margin: 1px 0 0 -1px;\n  border-radius: ", ";\n  width: 100%;\n"], ["\n  background-color: ", ";\n  color: ", ";\n  margin: 1px 0 0 -1px;\n  border-radius: ", ";\n  width: 100%;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.borderRadiusBottom; });
var StyledHeaderItem = styled(HeaderItem)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  height: 100%;\n  width: 100%;\n  ", ";\n"], ["\n  height: 100%;\n  width: 100%;\n  ", ";\n"])), function (p) { return p.locked && 'cursor: default'; });
var StyledLink = styled(Link)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=multipleProjectSelector.jsx.map