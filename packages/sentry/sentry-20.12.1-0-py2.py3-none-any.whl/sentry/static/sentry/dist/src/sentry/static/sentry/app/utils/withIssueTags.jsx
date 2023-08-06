import { __assign, __rest } from "tslib";
import React from 'react';
import createReactClass from 'create-react-class';
import assign from 'lodash/assign';
import Reflux from 'reflux';
import MemberListStore from 'app/stores/memberListStore';
import TagStore from 'app/stores/tagStore';
import TeamStore from 'app/stores/teamStore';
import getDisplayName from 'app/utils/getDisplayName';
var uuidPattern = /[0-9a-f]{32}$/;
var getUsername = function (_a) {
    var isManaged = _a.isManaged, username = _a.username, email = _a.email;
    // Users created via SAML receive unique UUID usernames. Use
    // their email in these cases, instead.
    if (username && uuidPattern.test(username)) {
        return email;
    }
    else {
        return !isManaged && username ? username : email;
    }
};
/**
 * HOC for getting tags and many useful issue attributes as 'tags' for use
 * in autocomplete selectors or condition builders.
 */
var withIssueTags = function (WrappedComponent) {
    return createReactClass({
        displayName: "withIssueTags(" + getDisplayName(WrappedComponent) + ")",
        mixins: [
            Reflux.listenTo(MemberListStore, 'onMemberListStoreChange'),
            Reflux.listenTo(TeamStore, 'onTeamStoreChange'),
            Reflux.listenTo(TagStore, 'onTagsUpdate'),
        ],
        getInitialState: function () {
            var tags = assign({}, TagStore.getAllTags(), TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
            var users = MemberListStore.getAll();
            var teams = TeamStore.getAll();
            return { tags: tags, users: users, teams: teams };
        },
        onMemberListStoreChange: function (users) {
            this.setState({ users: users });
            this.setAssigned();
        },
        onTeamStoreChange: function () {
            this.setState({ teams: TeamStore.getAll() });
            this.setAssigned();
        },
        onTagsUpdate: function (storeTags) {
            var tags = assign({}, storeTags, TagStore.getIssueAttributes(), TagStore.getBuiltInTags());
            this.setState({ tags: tags });
            this.setAssigned();
        },
        setAssigned: function () {
            var _a = this.state, tags = _a.tags, users = _a.users, teams = _a.teams;
            var usernames = users.map(getUsername);
            var teamnames = teams
                .filter(function (team) { return team.isMember; })
                .map(function (team) { return "#" + team.name; });
            var allAssigned = usernames.concat(teamnames);
            allAssigned.unshift('me');
            usernames.unshift('me');
            this.setState({
                tags: __assign(__assign({}, tags), { assigned: __assign(__assign({}, tags.assigned), { values: allAssigned }), bookmarks: __assign(__assign({}, tags.bookmarks), { values: usernames }), owner: __assign(__assign({}, tags.owner), { values: allAssigned }) }),
            });
        },
        render: function () {
            var _a = this.props, tags = _a.tags, props = __rest(_a, ["tags"]);
            return <WrappedComponent {...__assign({ tags: tags !== null && tags !== void 0 ? tags : this.state.tags }, props)}/>;
        },
    });
};
export default withIssueTags;
//# sourceMappingURL=withIssueTags.jsx.map