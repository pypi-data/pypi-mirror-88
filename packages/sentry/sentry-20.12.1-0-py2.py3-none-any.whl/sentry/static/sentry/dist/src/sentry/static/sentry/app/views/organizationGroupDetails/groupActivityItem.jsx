import React from 'react';
import CommitLink from 'app/components/commitLink';
import Duration from 'app/components/duration';
import Link from 'app/components/links/link';
import PullRequestLink from 'app/components/pullRequestLink';
import Version from 'app/components/version';
import { t, tct, tn } from 'app/locale';
import MemberListStore from 'app/stores/memberListStore';
import TeamStore from 'app/stores/teamStore';
import { GroupActivityType, } from 'app/types';
function GroupActivityItem(_a) {
    var activity = _a.activity, orgSlug = _a.orgSlug, projectId = _a.projectId, author = _a.author;
    var issuesLink = "/organizations/" + orgSlug + "/issues/";
    function getIgnoredMessage(data) {
        if (data.ignoreDuration) {
            return tct('[author] ignored this issue for [duration]', {
                author: author,
                duration: <Duration seconds={data.ignoreDuration * 60}/>,
            });
        }
        if (data.ignoreCount && data.ignoreWindow) {
            return tct('[author] ignored this issue until it happens [count] time(s) in [duration]', {
                author: author,
                count: data.ignoreCount,
                duration: <Duration seconds={data.ignoreWindow * 60}/>,
            });
        }
        if (data.ignoreCount) {
            return tct('[author] ignored this issue until it happens [count] time(s)', {
                author: author,
                count: data.ignoreCount,
            });
        }
        if (data.ignoreUserCount && data.ignoreUserWindow) {
            return tct('[author] ignored this issue until it affects [count] user(s) in [duration]', {
                author: author,
                count: data.ignoreUserCount,
                duration: <Duration seconds={data.ignoreUserWindow * 60}/>,
            });
        }
        if (data.ignoreUserCount) {
            return tct('[author] ignored this issue until it affects [count] user(s)', {
                author: author,
                count: data.ignoreUserCount,
            });
        }
        return tct('[author] ignored this issue', { author: author });
    }
    function getAssignedMessage(data) {
        var assignee = undefined;
        if (data.assigneeType === 'team') {
            var team = TeamStore.getById(data.assignee);
            assignee = team ? team.slug : '<unknown-team>';
            return tct('[author] assigned this issue to #[assignee]', {
                author: author,
                assignee: assignee,
            });
        }
        if (activity.user && activity.assignee === activity.user.id) {
            return tct('[author] assigned this issue to themselves', { author: author });
        }
        assignee = MemberListStore.getById(data.assignee);
        if (typeof assignee === 'object' && (assignee === null || assignee === void 0 ? void 0 : assignee.email)) {
            return tct('[author] assigned this issue to [assignee]', {
                author: author,
                assignee: assignee.email,
            });
        }
        return tct('[author] assigned this issue to an unknown user', { author: author });
    }
    function renderContent() {
        var _a;
        switch (activity.type) {
            case GroupActivityType.NOTE:
                return tct('[author] left a comment', { author: author });
            case GroupActivityType.SET_RESOLVED:
                return tct('[author] marked this issue as resolved', { author: author });
            case GroupActivityType.SET_RESOLVED_BY_AGE:
                return tct('[author] marked this issue as resolved due to inactivity', {
                    author: author,
                });
            case GroupActivityType.SET_RESOLVED_IN_RELEASE:
                return activity.data.version
                    ? tct('[author] marked this issue as resolved in [version]', {
                        author: author,
                        version: (<Version version={activity.data.version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : tct('[author] marked this issue as resolved in the upcoming release', {
                        author: author,
                    });
            case GroupActivityType.SET_RESOLVED_IN_COMMIT:
                return tct('[author] marked this issue as resolved in [version]', {
                    author: author,
                    version: (<CommitLink inline commitId={activity.data.commit.id} repository={activity.data.commit.repository}/>),
                });
            case GroupActivityType.SET_RESOLVED_IN_PULL_REQUEST: {
                var data = activity.data;
                var pullRequest = data.pullRequest;
                return tct('[author] marked this issue as resolved in [version]', {
                    author: author,
                    version: (<PullRequestLink inline pullRequest={pullRequest} repository={pullRequest.repository}/>),
                });
            }
            case GroupActivityType.SET_UNRESOLVED:
                return tct('[author] marked this issue as unresolved', { author: author });
            case GroupActivityType.SET_IGNORED: {
                var data = activity.data;
                return getIgnoredMessage(data);
            }
            case GroupActivityType.SET_PUBLIC:
                return tct('[author] made this issue public', { author: author });
            case GroupActivityType.SET_PRIVATE:
                return tct('[author] made this issue private', { author: author });
            case GroupActivityType.SET_REGRESSION: {
                var data = activity.data;
                return data.version
                    ? tct('[author] marked this issue as a regression in [version]', {
                        author: author,
                        version: (<Version version={data.version} projectId={projectId} tooltipRawVersion/>),
                    })
                    : tct('[author] marked this issue as a regression', { author: author });
            }
            case GroupActivityType.CREATE_ISSUE: {
                var data = activity.data;
                return tct('[author] created an issue on [provider] titled [title]', {
                    author: author,
                    provider: data.provider,
                    title: <Link to={data.location}>{data.title}</Link>,
                });
            }
            case GroupActivityType.UNMERGE_SOURCE: {
                var data = activity.data;
                var destination = data.destination, fingerprints = data.fingerprints;
                return tn('%2$s migrated %1$s fingerprint to %3$s', '%2$s migrated %1$s fingerprints to %3$s', fingerprints.length, author, destination ? (<Link to={"" + issuesLink + destination.id}>{destination.shortId}</Link>) : (t('a group')));
            }
            case GroupActivityType.UNMERGE_DESTINATION: {
                var data = activity.data;
                var source = data.source, fingerprints = data.fingerprints;
                return tn('%2$s migrated %1$s fingerprint from %3$s', '%2$s migrated %1$s fingerprints from %3$s', fingerprints.length, author, source ? (<Link to={"" + issuesLink + source.id}>{source.shortId}</Link>) : (t('a group')));
            }
            case GroupActivityType.FIRST_SEEN:
                return tct('[author] first saw this issue', { author: author });
            case GroupActivityType.ASSIGNED: {
                var data = activity.data;
                return getAssignedMessage(data);
            }
            case GroupActivityType.UNASSIGNED:
                return tct('[author] unassigned this issue', { author: author });
            case GroupActivityType.MERGE:
                return tn('%2$s merged %1$s issue into this issue', '%2$s merged %1$s issues into this issue', activity.data.issues.length, author);
            case GroupActivityType.REPROCESS: {
                var data = activity.data;
                var oldGroupId = data.oldGroupId, eventCount = data.eventCount;
                return tct('[author] reprocessed the events in this issue. [new-events]', (_a = {
                        author: author
                    },
                    _a['new-events'] = (<Link to={"/organizations/" + orgSlug + "/issues/?query=reprocessing.original_issue_id:" + oldGroupId}>
              {tn('See %s new event', 'See %s new events', eventCount)}
            </Link>),
                    _a));
            }
            default:
                return ''; // should never hit (?)
        }
    }
    return <React.Fragment>{renderContent()}</React.Fragment>;
}
export default GroupActivityItem;
//# sourceMappingURL=groupActivityItem.jsx.map