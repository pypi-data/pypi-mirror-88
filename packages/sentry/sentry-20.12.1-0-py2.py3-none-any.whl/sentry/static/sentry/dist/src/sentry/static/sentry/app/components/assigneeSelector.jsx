import { __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import PropTypes from 'prop-types';
import Reflux from 'reflux';
import { assignToActor, assignToUser, clearAssignment } from 'app/actionCreators/group';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import SuggestedAvatarStack from 'app/components/avatar/suggestedAvatarStack';
import TeamAvatar from 'app/components/avatar/teamAvatar';
import UserAvatar from 'app/components/avatar/userAvatar';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownBubble from 'app/components/dropdownBubble';
import Highlight from 'app/components/highlight';
import Link from 'app/components/links/link';
import LoadingIndicator from 'app/components/loadingIndicator';
import TextOverflow from 'app/components/textOverflow';
import { IconAdd, IconChevron, IconClose, IconUser } from 'app/icons';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import ConfigStore from 'app/stores/configStore';
import GroupStore from 'app/stores/groupStore';
import MemberListStore from 'app/stores/memberListStore';
import ProjectsStore from 'app/stores/projectsStore';
import space from 'app/styles/space';
import { buildTeamId, buildUserId, valueIsEqual } from 'app/utils';
var AssigneeSelectorComponent = createReactClass({
    displayName: 'AssigneeSelector',
    propTypes: {
        id: PropTypes.string.isRequired,
        size: PropTypes.number,
        // Either a list of users, or null. If null, members will
        // be read from the MemberListStore. The prop is useful when the
        // store contains more/different users than you need to show
        // in an individual component, eg. Org Issue list
        memberList: PropTypes.array,
        disabled: PropTypes.bool,
    },
    contextTypes: {
        organization: SentryTypes.Organization,
    },
    mixins: [
        Reflux.listenTo(GroupStore, 'onGroupChange'),
        Reflux.connect(MemberListStore, 'memberList'),
    ],
    getDefaultProps: function () {
        return {
            id: null,
            size: 20,
            memberList: undefined,
        };
    },
    getInitialState: function () {
        var group = GroupStore.get(this.props.id);
        var memberList = MemberListStore.loaded ? MemberListStore.getAll() : undefined;
        var loading = GroupStore.hasStatus(this.props.id, 'assignTo');
        var suggestedOwners = group && group.owners;
        return {
            assignedTo: group && group.assignedTo,
            memberList: memberList,
            loading: loading,
            suggestedOwners: suggestedOwners,
        };
    },
    componentWillReceiveProps: function (nextProps) {
        var loading = nextProps.id && GroupStore.hasStatus(nextProps.id, 'assignTo');
        if (nextProps.id !== this.props.id || loading !== this.state.loading) {
            var group = GroupStore.get(this.props.id);
            this.setState({
                loading: loading,
                assignedTo: group && group.assignedTo,
                suggestedOwners: group && group.owners,
            });
        }
    },
    shouldComponentUpdate: function (nextProps, nextState) {
        if (nextState.loading !== this.state.loading) {
            return true;
        }
        // If the memberList in props has changed, re-render as
        // props have updated, and we won't use internal state anyways.
        if (nextProps.memberList &&
            !valueIsEqual(this.props.memberList, nextProps.memberList)) {
            return true;
        }
        var currentMembers = this.memberList();
        // XXX(billyvg): this means that once `memberList` is not-null, this component will never update due to `memberList` changes
        // Note: this allows us to show a "loading" state for memberList, but only before `MemberListStore.loadInitialData`
        // is called
        if (currentMembers === undefined && nextState.memberList !== currentMembers) {
            return true;
        }
        return !valueIsEqual(nextState.assignedTo, this.state.assignedTo, true);
    },
    memberList: function () {
        return this.props.memberList ? this.props.memberList : this.state.memberList;
    },
    assignableTeams: function () {
        if (!this.props.id) {
            return [];
        }
        var group = GroupStore.get(this.props.id);
        if (!group) {
            return [];
        }
        return ((group && ProjectsStore.getBySlug(group.project.slug)) || {
            teams: [],
        }).teams
            .sort(function (a, b) { return a.slug.localeCompare(b.slug); })
            .map(function (team) { return ({
            id: buildTeamId(team.id),
            display: "#" + team.slug,
            email: team.id,
            team: team,
        }); });
    },
    onGroupChange: function (itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        var group = GroupStore.get(this.props.id);
        this.setState({
            assignedTo: group && group.assignedTo,
            suggestedOwners: group && group.owners,
            loading: this.props.id && GroupStore.hasStatus(this.props.id, 'assignTo'),
        });
    },
    assignToUser: function (user) {
        assignToUser({ id: this.props.id, user: user });
        this.setState({ loading: true });
    },
    assignToTeam: function (team) {
        assignToActor({ actor: { id: team.id, type: 'team' }, id: this.props.id });
        this.setState({ loading: true });
    },
    handleAssign: function (_a, _state, e) {
        var _b = _a.value, type = _b.type, assignee = _b.assignee;
        if (type === 'member') {
            this.assignToUser(assignee);
        }
        if (type === 'team') {
            this.assignToTeam(assignee);
        }
        e.stopPropagation();
    },
    clearAssignTo: function (e) {
        // clears assignment
        clearAssignment(this.props.id);
        this.setState({ loading: true });
        e.stopPropagation();
    },
    renderMemberNode: function (member, suggestedReason) {
        var _this = this;
        var size = this.props.size;
        return {
            value: { type: 'member', assignee: member },
            searchKey: member.email + " " + member.name,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<MenuItemWrapper data-test-id="assignee-option" key={buildUserId(member.id)} onSelect={_this.assignToUser.bind(_this, member)}>
          <IconContainer>
            <UserAvatar user={member} size={size}/>
          </IconContainer>
          <Label>
            <Highlight text={inputValue}>{member.name || member.email}</Highlight>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>);
            },
        };
    },
    renderNewMemberNodes: function () {
        var _this = this;
        var members = putSessionUserFirst(this.memberList());
        return members.map(function (member) { return _this.renderMemberNode(member); });
    },
    renderTeamNode: function (assignableTeam, suggestedReason) {
        var _this = this;
        var size = this.props.size;
        var id = assignableTeam.id, display = assignableTeam.display, team = assignableTeam.team;
        return {
            value: { type: 'team', assignee: team },
            searchKey: team.slug,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<MenuItemWrapper data-test-id="assignee-option" key={id} onSelect={_this.assignToTeam.bind(_this, team)}>
          <IconContainer>
            <TeamAvatar team={team} size={size}/>
          </IconContainer>
          <Label>
            <Highlight text={inputValue}>{display}</Highlight>
            {suggestedReason && <SuggestedReason>{suggestedReason}</SuggestedReason>}
          </Label>
        </MenuItemWrapper>);
            },
        };
    },
    renderNewTeamNodes: function () {
        var _this = this;
        return this.assignableTeams().map(function (team) { return _this.renderTeamNode(team); });
    },
    renderSuggestedAssigneeNodes: function () {
        var _this = this;
        var _a;
        return (_a = this.getSuggestedAssignees()) === null || _a === void 0 ? void 0 : _a.map(function (_a) {
            var type = _a.type, suggestedReason = _a.suggestedReason, assignee = _a.assignee;
            var reason = suggestedReason === 'suspectCommit' ? t('(Suspect Commit)') : t('(Issue Owner)');
            if (type === 'user') {
                return _this.renderMemberNode(assignee, reason);
            }
            else if (type === 'team') {
                return _this.renderTeamNode(assignee, reason);
            }
            return null;
        });
    },
    renderDropdownGroupLabel: function (label) {
        return <GroupHeader>{label}</GroupHeader>;
    },
    renderNewDropdownItems: function () {
        var _a;
        var teams = this.renderNewTeamNodes();
        var members = this.renderNewMemberNodes();
        var dropdownItems = [
            { label: this.renderDropdownGroupLabel(t('Teams')), id: 'team-header', items: teams },
            {
                label: this.renderDropdownGroupLabel(t('People')),
                id: 'members-header',
                items: members,
            },
        ];
        var suggestedAssignees = (_a = this.renderSuggestedAssigneeNodes()) === null || _a === void 0 ? void 0 : _a.filter(function (assignee) { return !!assignee; });
        if (suggestedAssignees && suggestedAssignees.length) {
            dropdownItems.unshift({
                label: this.renderDropdownGroupLabel(t('Suggested')),
                id: 'suggested-header',
                items: suggestedAssignees,
            });
        }
        return dropdownItems;
    },
    getSuggestedAssignees: function () {
        var _this = this;
        var suggestedOwners = this.state.suggestedOwners;
        if (!suggestedOwners) {
            return null;
        }
        return suggestedOwners
            .map(function (owner) {
            var _a;
            // converts a backend suggested owner to a suggested assignee
            var _b = __read(owner.owner.split(':'), 2), ownerType = _b[0], id = _b[1];
            if (ownerType === 'user') {
                var member = (_a = _this.memberList()) === null || _a === void 0 ? void 0 : _a.find(function (user) { return user.id === id; });
                if (member) {
                    return {
                        type: 'user',
                        id: id,
                        name: member.name,
                        suggestedReason: owner.type,
                        assignee: member,
                    };
                }
            }
            else if (ownerType === 'team') {
                var matchingTeam = _this.assignableTeams().find(function (assignableTeam) { return assignableTeam.id === owner.owner; });
                if (matchingTeam) {
                    return {
                        type: 'team',
                        id: id,
                        name: matchingTeam.team.name,
                        suggestedReason: owner.type,
                        assignee: matchingTeam,
                    };
                }
            }
            return null;
        })
            .filter(function (owner) { return !!owner; });
    },
    render: function () {
        var _a = this.props, className = _a.className, disabled = _a.disabled;
        var _b = this.state, loading = _b.loading, assignedTo = _b.assignedTo;
        var memberList = this.memberList();
        var suggestedActors = this.getSuggestedAssignees();
        return (<div className={className}>
        {loading && (<LoadingIndicator mini style={{ height: '24px', margin: 0, marginRight: 11 }}/>)}
        {!loading && (<DropdownAutoComplete disabled={disabled} maxHeight={400} onOpen={function (e) {
            // This can be called multiple times and does not always have `event`
            if (!e) {
                return;
            }
            e.stopPropagation();
        }} busy={memberList === undefined} items={memberList !== undefined ? this.renderNewDropdownItems() : null} alignMenu="right" onSelect={this.handleAssign} itemSize="small" searchPlaceholder={t('Filter teams and people')} menuHeader={assignedTo && (<MenuItemWrapper data-test-id="clear-assignee" onClick={this.clearAssignTo} py={0}>
                  <IconContainer>
                    <ClearAssigneeIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{t('Clear Assignee')}</Label>
                </MenuItemWrapper>)} menuFooter={<InviteMemberLink to="" data-test-id="invite-member" disabled={loading} onClick={function () { return openInviteMembersModal({ source: 'assignee_selector' }); }}>
                <MenuItemWrapper>
                  <IconContainer>
                    <InviteMemberIcon isCircled size="14px"/>
                  </IconContainer>
                  <Label>{t('Invite Member')}</Label>
                </MenuItemWrapper>
              </InviteMemberLink>} menuWithArrow emptyHidesInput>
            {function (_a) {
            var getActorProps = _a.getActorProps, isOpen = _a.isOpen;
            return (<DropdownButton {...getActorProps({})}>
                {assignedTo ? (<ActorAvatar actor={assignedTo} className="avatar" size={24}/>) : suggestedActors ? (<SuggestedAvatarStack size={24} owners={suggestedActors}/>) : (<StyledIconUser size="20px" color="gray400"/>)}
                <StyledChevron direction={isOpen ? 'up' : 'down'} size="xs"/>
              </DropdownButton>);
        }}
          </DropdownAutoComplete>)}
      </div>);
    },
});
export function putSessionUserFirst(members) {
    // If session user is in the filtered list of members, put them at the top
    if (!members) {
        return [];
    }
    var sessionUser = ConfigStore.get('user');
    var sessionUserIndex = members.findIndex(function (member) { return sessionUser && member.id === sessionUser.id; });
    if (sessionUserIndex === -1) {
        return members;
    }
    var arrangedMembers = [members[sessionUserIndex]];
    arrangedMembers.push.apply(arrangedMembers, __spread(members.slice(0, sessionUserIndex)));
    arrangedMembers.push.apply(arrangedMembers, __spread(members.slice(sessionUserIndex + 1)));
    return arrangedMembers;
}
var AssigneeSelector = styled(AssigneeSelectorComponent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n\n  /* manually align menu underneath dropdown caret */\n  ", " {\n    right: -14px;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n\n  /* manually align menu underneath dropdown caret */\n  ", " {\n    right: -14px;\n  }\n"])), DropdownBubble);
export default AssigneeSelector;
export { AssigneeSelectorComponent };
var StyledIconUser = styled(IconUser)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  /* We need this to center with Avatar */\n  margin-right: 2px;\n"], ["\n  /* We need this to center with Avatar */\n  margin-right: 2px;\n"])));
var IconContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  flex-shrink: 0;\n"])));
var MenuItemWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 13px;\n  ", ";\n"], ["\n  cursor: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 13px;\n  ",
    ";\n"])), function (p) { return (p.disabled ? 'not-allowed' : 'pointer'); }, function (p) {
    return typeof p.py !== 'undefined' &&
        "\n      padding-top: " + p.py + ";\n      padding-bottom: " + p.py + ";\n    ";
});
var InviteMemberLink = styled(Link)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return (p.disabled ? p.theme.disabled : p.theme.textColor); });
var Label = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: 6px;\n"], ["\n  margin-left: 6px;\n"])));
var ClearAssigneeIcon = styled(IconClose)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  opacity: 0.3;\n"], ["\n  opacity: 0.3;\n"])));
var InviteMemberIcon = styled(IconAdd)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  opacity: 0.3;\n"], ["\n  opacity: 0.3;\n"])));
var StyledChevron = styled(IconChevron)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var DropdownButton = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  font-size: 20px;\n"], ["\n  display: flex;\n  align-items: center;\n  font-size: 20px;\n"])));
var GroupHeader = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 600;\n  margin: ", " 0;\n  color: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: 600;\n  margin: ", " 0;\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, space(1), function (p) { return p.theme.gray500; });
var SuggestedReason = styled('span')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=assigneeSelector.jsx.map