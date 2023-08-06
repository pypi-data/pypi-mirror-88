import { __extends } from "tslib";
import { updateTeam } from 'app/actionCreators/teams';
import FormModel from 'app/views/settings/components/forms/model';
var TeamFormModel = /** @class */ (function (_super) {
    __extends(TeamFormModel, _super);
    function TeamFormModel(orgId, teamId) {
        var _this = _super.call(this) || this;
        _this.orgId = orgId;
        _this.teamId = teamId;
        return _this;
    }
    TeamFormModel.prototype.doApiRequest = function (_a) {
        var _this = this;
        var data = _a.data;
        return new Promise(function (resolve, reject) {
            return updateTeam(_this.api, {
                orgId: _this.orgId,
                teamId: _this.teamId,
                data: data,
            }, {
                success: resolve,
                error: reject,
            });
        });
    };
    return TeamFormModel;
}(FormModel));
export default TeamFormModel;
//# sourceMappingURL=model.jsx.map