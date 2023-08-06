import { __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import PropTypes from 'prop-types';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import AuditLogList from './auditLogList';
// Please keep this list sorted
var EVENT_TYPES = [
    'member.invite',
    'member.add',
    'member.accept-invite',
    'member.remove',
    'member.edit',
    'member.join-team',
    'member.leave-team',
    'member.pending',
    'team.create',
    'team.edit',
    'team.remove',
    'project.create',
    'project.edit',
    'project.remove',
    'project.set-public',
    'project.set-private',
    'project.request-transfer',
    'project.accept-transfer',
    'org.create',
    'org.edit',
    'org.remove',
    'org.restore',
    'tagkey.remove',
    'projectkey.create',
    'projectkey.edit',
    'projectkey.remove',
    'projectkey.enable',
    'projectkey.disable',
    'sso.enable',
    'sso.disable',
    'sso.edit',
    'sso-identity.link',
    'api-key.create',
    'api-key.edit',
    'api-key.remove',
    'rule.create',
    'rule.edit',
    'rule.remove',
    'servicehook.create',
    'servicehook.edit',
    'servicehook.remove',
    'servicehook.enable',
    'servicehook.disable',
    'integration.add',
    'integration.edit',
    'integration.remove',
    'ondemand.edit',
    'trial.started',
    'plan.changed',
    'plan.cancelled',
];
var OrganizationAuditLog = /** @class */ (function (_super) {
    __extends(OrganizationAuditLog, _super);
    function OrganizationAuditLog() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleEventSelect = function (value) {
            // Dont update if event has not changed
            if (_this.props.location.query.event === value) {
                return;
            }
            browserHistory.push({
                pathname: _this.props.location.pathname,
                search: "?event=" + value,
            });
        };
        return _this;
    }
    OrganizationAuditLog.prototype.getEndpoints = function () {
        return [
            [
                'entryList',
                "/organizations/" + this.props.params.orgId + "/audit-logs/",
                {
                    query: this.props.location.query,
                },
            ],
        ];
    };
    OrganizationAuditLog.prototype.getTitle = function () {
        return routeTitleGen(t('Audit Log'), this.context.organization.slug, false);
    };
    OrganizationAuditLog.prototype.renderBody = function () {
        var currentEventType = this.props.location.query.event;
        return (<AuditLogList entries={this.state.entryList} pageLinks={this.state.pageLinks} eventType={currentEventType} eventTypes={EVENT_TYPES} onEventSelect={this.handleEventSelect} {...this.props}/>);
    };
    OrganizationAuditLog.contextTypes = {
        router: PropTypes.object,
        organization: SentryTypes.Organization,
    };
    return OrganizationAuditLog;
}(AsyncView));
export default OrganizationAuditLog;
//# sourceMappingURL=index.jsx.map