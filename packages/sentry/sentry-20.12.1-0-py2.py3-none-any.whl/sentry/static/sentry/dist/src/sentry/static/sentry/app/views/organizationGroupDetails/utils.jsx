import { __awaiter, __generator, __read, __spread } from "tslib";
import React from 'react';
import orderBy from 'lodash/orderBy';
import { Client } from 'app/api';
import { t, tct } from 'app/locale';
/**
 * Fetches group data and mark as seen
 *
 * @param orgId organization slug
 * @param groupId groupId
 * @param eventId eventId or "latest" or "oldest"
 * @param envNames
 * @param projectId project slug required for eventId that is not latest or oldest
 */
export function fetchGroupEvent(api, orgId, groupId, eventId, envNames, projectId) {
    return __awaiter(this, void 0, void 0, function () {
        var url, query, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    url = eventId === 'latest' || eventId === 'oldest'
                        ? "/issues/" + groupId + "/events/" + eventId + "/"
                        : "/projects/" + orgId + "/" + projectId + "/events/" + eventId + "/";
                    query = {};
                    if (envNames.length !== 0) {
                        query.environment = envNames;
                    }
                    return [4 /*yield*/, api.requestPromise(url, { query: query })];
                case 1:
                    data = _a.sent();
                    return [2 /*return*/, data];
            }
        });
    });
}
export function markEventSeen(api, orgId, projectId, groupId) {
    api.bulkUpdate({
        orgId: orgId,
        projectId: projectId,
        itemIds: [groupId],
        failSilently: true,
        data: { hasSeen: true },
    }, {});
}
export function fetchGroupUserReports(groupId, query) {
    var api = new Client();
    return api.requestPromise("/issues/" + groupId + "/user-reports/", {
        includeAllArgs: true,
        query: query,
    });
}
/**
 * Returns the environment name for an event or null
 *
 * @param event
 */
export function getEventEnvironment(event) {
    var tag = event.tags.find(function (_a) {
        var key = _a.key;
        return key === 'environment';
    });
    return tag ? tag.value : null;
}
var SUBSCRIPTION_REASONS = {
    commented: t("You're receiving workflow notifications because you have commented on this issue."),
    assigned: t("You're receiving workflow notifications because you were assigned to this issue."),
    bookmarked: t("You're receiving workflow notifications because you have bookmarked this issue."),
    changed_status: t("You're receiving workflow notifications because you have changed the status of this issue."),
    mentioned: t("You're receiving workflow notifications because you have been mentioned in this issue."),
};
/**
 * @param group
 * @param removeLinks add/remove links to subscription reasons text (default: false)
 * @returns Reason for subscription
 */
export function getSubscriptionReason(group, removeLinks) {
    if (removeLinks === void 0) { removeLinks = false; }
    if (group.subscriptionDetails && group.subscriptionDetails.disabled) {
        return tct('You have [link:disabled workflow notifications] for this project.', {
            link: removeLinks ? <span /> : <a href="/account/settings/notifications/"/>,
        });
    }
    if (!group.isSubscribed) {
        return t('Subscribe to workflow notifications for this issue');
    }
    if (group.subscriptionDetails) {
        var reason = group.subscriptionDetails.reason;
        if (reason === 'unknown') {
            return t("You're receiving workflow notifications because you are subscribed to this issue.");
        }
        if (reason && SUBSCRIPTION_REASONS.hasOwnProperty(reason)) {
            return SUBSCRIPTION_REASONS[reason];
        }
    }
    return tct("You're receiving updates because you are [link:subscribed to workflow notifications] for this project.", {
        link: removeLinks ? <span /> : <a href="/account/settings/notifications/"/>,
    });
}
export function getGroupMostRecentActivity(activities) {
    // Most recent activity
    return orderBy(__spread(activities), function (_a) {
        var dateCreated = _a.dateCreated;
        return new Date(dateCreated);
    }, ['desc'])[0];
}
export var ReprocessingStatus;
(function (ReprocessingStatus) {
    ReprocessingStatus["REPROCESSED_AND_HASNT_EVENT"] = "reprocessed_and_hasnt_event";
    ReprocessingStatus["REPROCESSED_AND_HAS_EVENT"] = "reprocessed_and_has_event";
    ReprocessingStatus["REPROCESSING"] = "reprocessing";
    ReprocessingStatus["NO_STATUS"] = "no_status";
})(ReprocessingStatus || (ReprocessingStatus = {}));
// Reprocessing Checks
export function getGroupReprocessingStatus(group, mostRecentActivity) {
    var status = group.status, count = group.count, activities = group.activity;
    var groupCount = Number(count);
    switch (status) {
        case 'reprocessing':
            return ReprocessingStatus.REPROCESSING;
        case 'unresolved': {
            var groupMostRecentActivity = mostRecentActivity !== null && mostRecentActivity !== void 0 ? mostRecentActivity : getGroupMostRecentActivity(activities);
            if ((groupMostRecentActivity === null || groupMostRecentActivity === void 0 ? void 0 : groupMostRecentActivity.type) === 'reprocess') {
                if (groupCount === 0) {
                    return ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT;
                }
                return ReprocessingStatus.REPROCESSED_AND_HAS_EVENT;
            }
            return ReprocessingStatus.NO_STATUS;
        }
        default:
            return ReprocessingStatus.NO_STATUS;
    }
}
//# sourceMappingURL=utils.jsx.map