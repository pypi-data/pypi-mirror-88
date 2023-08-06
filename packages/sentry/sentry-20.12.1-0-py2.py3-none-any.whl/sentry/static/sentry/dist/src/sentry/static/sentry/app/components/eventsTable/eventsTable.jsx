import { __extends } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import EventsTableRow from 'app/components/eventsTable/eventsTableRow';
import { t } from 'app/locale';
import CustomPropTypes from 'app/sentryTypes';
var EventsTable = /** @class */ (function (_super) {
    __extends(EventsTable, _super);
    function EventsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsTable.prototype.render = function () {
        var _a = this.props, events = _a.events, tagList = _a.tagList, orgId = _a.orgId, projectId = _a.projectId, groupId = _a.groupId;
        var hasUser = !!events.find(function (event) { return event.user; });
        return (<table className="table events-table">
        <thead>
          <tr>
            <th>{t('ID')}</th>
            {hasUser && <th>{t('User')}</th>}

            {tagList.map(function (tag) { return (<th key={tag.key}>{tag.name}</th>); })}
          </tr>
        </thead>
        <tbody>
          {events.map(function (event) { return (<EventsTableRow key={event.id} event={event} orgId={orgId} projectId={projectId} groupId={groupId} tagList={tagList} hasUser={hasUser}/>); })}
        </tbody>
      </table>);
    };
    EventsTable.propTypes = {
        events: PropTypes.arrayOf(CustomPropTypes.Event),
        tagList: PropTypes.arrayOf(CustomPropTypes.Tag),
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string.isRequired,
        groupId: PropTypes.string.isRequired,
    };
    return EventsTable;
}(React.Component));
export default EventsTable;
//# sourceMappingURL=eventsTable.jsx.map