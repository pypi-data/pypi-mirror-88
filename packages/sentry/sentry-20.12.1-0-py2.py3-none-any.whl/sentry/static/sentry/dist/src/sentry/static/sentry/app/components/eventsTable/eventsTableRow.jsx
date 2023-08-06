import { __extends } from "tslib";
import React from 'react';
import UserAvatar from 'app/components/avatar/userAvatar';
import DateTime from 'app/components/dateTime';
import DeviceName from 'app/components/deviceName';
import FileSize from 'app/components/fileSize';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import AttachmentUrl from 'app/utils/attachmentUrl';
import withOrganization from 'app/utils/withOrganization';
var EventsTableRow = /** @class */ (function (_super) {
    __extends(EventsTableRow, _super);
    function EventsTableRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsTableRow.prototype.renderCrashFileLink = function () {
        var _a = this.props, event = _a.event, projectId = _a.projectId;
        if (!event.crashFile) {
            return null;
        }
        var crashFileType = event.crashFile.type === 'event.minidump' ? 'Minidump' : 'Crash file';
        return (<AttachmentUrl projectId={projectId} eventId={event.id} attachment={event.crashFile}>
        {function (url) {
            var _a, _b;
            return url && (<small>
              {crashFileType}: <a href={url + "?download=1"}>{(_a = event.crashFile) === null || _a === void 0 ? void 0 : _a.name}</a> (
              <FileSize bytes={((_b = event.crashFile) === null || _b === void 0 ? void 0 : _b.size) || 0}/>)
            </small>);
        }}
      </AttachmentUrl>);
    };
    EventsTableRow.prototype.render = function () {
        var _a = this.props, className = _a.className, event = _a.event, orgId = _a.orgId, groupId = _a.groupId, tagList = _a.tagList, hasUser = _a.hasUser;
        var tagMap = {};
        event.tags.forEach(function (tag) {
            tagMap[tag.key] = tag.value;
        });
        var link = "/organizations/" + orgId + "/issues/" + groupId + "/events/" + event.id + "/";
        return (<tr key={event.id} className={className}>
        <td>
          <h5>
            <GlobalSelectionLink to={link}>
              <DateTime date={event.dateCreated}/>
            </GlobalSelectionLink>
            <small>{event.title.substr(0, 100)}</small>
            {this.renderCrashFileLink()}
          </h5>
        </td>

        {hasUser && (<td className="event-user table-user-info">
            {event.user ? (<div>
                <UserAvatar user={event.user} // TODO(ts): Some of the user fields are optional from event, this cast can probably be removed in the future
         size={24} className="avatar" gravatar={false}/>
                {event.user.email}
              </div>) : (<span>—</span>)}
          </td>)}

        {tagList.map(function (tag) { return (<td key={tag.key}>
            <div>
              {tag.key === 'device' ? (<DeviceName value={tagMap[tag.key]}/>) : (tagMap[tag.key])}
            </div>
          </td>); })}
      </tr>);
    };
    return EventsTableRow;
}(React.Component));
export { EventsTableRow };
export default withOrganization(EventsTableRow);
//# sourceMappingURL=eventsTableRow.jsx.map