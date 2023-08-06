export var SavedSearchType;
(function (SavedSearchType) {
    SavedSearchType[SavedSearchType["ISSUE"] = 0] = "ISSUE";
    SavedSearchType[SavedSearchType["EVENT"] = 1] = "EVENT";
})(SavedSearchType || (SavedSearchType = {}));
export var GroupActivityType;
(function (GroupActivityType) {
    GroupActivityType["NOTE"] = "note";
    GroupActivityType["SET_RESOLVED"] = "set_resolved";
    GroupActivityType["SET_RESOLVED_BY_AGE"] = "set_resolved_by_age";
    GroupActivityType["SET_RESOLVED_IN_RELEASE"] = "set_resolved_in_release";
    GroupActivityType["SET_RESOLVED_IN_COMMIT"] = "set_resolved_in_commit";
    GroupActivityType["SET_RESOLVED_IN_PULL_REQUEST"] = "set_resolved_in_pull_request";
    GroupActivityType["SET_UNRESOLVED"] = "set_unresolved";
    GroupActivityType["SET_IGNORED"] = "set_ignored";
    GroupActivityType["SET_PUBLIC"] = "set_public";
    GroupActivityType["SET_PRIVATE"] = "set_private";
    GroupActivityType["SET_REGRESSION"] = "set_regression";
    GroupActivityType["CREATE_ISSUE"] = "create_issue";
    GroupActivityType["UNMERGE_SOURCE"] = "unmerge_source";
    GroupActivityType["UNMERGE_DESTINATION"] = "unmerge_destination";
    GroupActivityType["FIRST_SEEN"] = "first_seen";
    GroupActivityType["ASSIGNED"] = "assigned";
    GroupActivityType["UNASSIGNED"] = "unassigned";
    GroupActivityType["MERGE"] = "merge";
    GroupActivityType["REPROCESS"] = "reprocess";
})(GroupActivityType || (GroupActivityType = {}));
export var RepositoryStatus;
(function (RepositoryStatus) {
    RepositoryStatus["ACTIVE"] = "active";
    RepositoryStatus["DISABLED"] = "disabled";
    RepositoryStatus["HIDDEN"] = "hidden";
    RepositoryStatus["PENDING_DELETION"] = "pending_deletion";
    RepositoryStatus["DELETION_IN_PROGRESS"] = "deletion_in_progress";
})(RepositoryStatus || (RepositoryStatus = {}));
export var ReleaseStatus;
(function (ReleaseStatus) {
    ReleaseStatus["Active"] = "open";
    ReleaseStatus["Archived"] = "archived";
})(ReleaseStatus || (ReleaseStatus = {}));
export var OnboardingTaskKey;
(function (OnboardingTaskKey) {
    OnboardingTaskKey["FIRST_PROJECT"] = "create_project";
    OnboardingTaskKey["FIRST_EVENT"] = "send_first_event";
    OnboardingTaskKey["INVITE_MEMBER"] = "invite_member";
    OnboardingTaskKey["SECOND_PLATFORM"] = "setup_second_platform";
    OnboardingTaskKey["USER_CONTEXT"] = "setup_user_context";
    OnboardingTaskKey["RELEASE_TRACKING"] = "setup_release_tracking";
    OnboardingTaskKey["SOURCEMAPS"] = "setup_sourcemaps";
    OnboardingTaskKey["USER_REPORTS"] = "setup_user_reports";
    OnboardingTaskKey["ISSUE_TRACKER"] = "setup_issue_tracker";
    OnboardingTaskKey["ALERT_RULE"] = "setup_alert_rules";
    OnboardingTaskKey["FIRST_TRANSACTION"] = "setup_transactions";
})(OnboardingTaskKey || (OnboardingTaskKey = {}));
export var ResolutionStatus;
(function (ResolutionStatus) {
    ResolutionStatus["RESOLVED"] = "resolved";
    ResolutionStatus["UNRESOLVED"] = "unresolved";
    ResolutionStatus["IGNORED"] = "ignored";
})(ResolutionStatus || (ResolutionStatus = {}));
export var EventGroupVariantType;
(function (EventGroupVariantType) {
    EventGroupVariantType["CUSTOM_FINGERPRINT"] = "custom-fingerprint";
    EventGroupVariantType["COMPONENT"] = "component";
    EventGroupVariantType["SALTED_COMPONENT"] = "salted-component";
})(EventGroupVariantType || (EventGroupVariantType = {}));
//# sourceMappingURL=index.jsx.map