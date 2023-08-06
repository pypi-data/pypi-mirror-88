import { __extends } from "tslib";
import React from 'react';
import moment from 'moment';
import Link from 'app/components/links/link';
import ResultGrid from 'app/components/resultGrid';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
export var prettyDate = function (x) {
    return moment(x).format('ll');
};
var AdminUsers = /** @class */ (function (_super) {
    __extends(AdminUsers, _super);
    function AdminUsers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getRow = function (row) { return [
            <td key="username">
      <strong>
        <Link to={"/manage/users/" + row.id + "/"}>{row.username}</Link>
      </strong>
      <br />
      {row.email !== row.username && <small>{row.email}</small>}
    </td>,
            <td key="dateJoined" style={{ textAlign: 'center' }}>
      {prettyDate(row.dateJoined)}
    </td>,
            <td key="lastLogin" style={{ textAlign: 'center' }}>
      {prettyDate(row.lastLogin)}
    </td>,
        ]; };
        return _this;
    }
    AdminUsers.prototype.render = function () {
        var columns = [
            <th key="username">User</th>,
            <th key="dateJoined" style={{ textAlign: 'center', width: 150 }}>
        Joined
      </th>,
            <th key="lastLogin" style={{ textAlign: 'center', width: 150 }}>
        Last Login
      </th>,
        ];
        return (<div>
        <h3>{t('Users')}</h3>
        <ResultGrid path="/manage/users/" endpoint="/users/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
            status: {
                name: 'Status',
                options: [
                    ['active', 'Active'],
                    ['disabled', 'Disabled'],
                ],
            },
        }} sortOptions={[['date', 'Date Joined']]} defaultSort="date" {...this.props}/>
      </div>);
    };
    return AdminUsers;
}(AsyncView));
export default AdminUsers;
//# sourceMappingURL=adminUsers.jsx.map