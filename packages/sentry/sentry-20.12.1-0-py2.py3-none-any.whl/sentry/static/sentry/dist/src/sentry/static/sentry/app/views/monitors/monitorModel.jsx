import { __extends, __read } from "tslib";
import FormModel from 'app/views/settings/components/forms/model';
var MonitorModel = /** @class */ (function (_super) {
    __extends(MonitorModel, _super);
    function MonitorModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MonitorModel.prototype.getTransformedData = function () {
        return Object.entries(this.fields.toJSON()).reduce(function (data, _a) {
            var _b = __read(_a, 2), k = _b[0], v = _b[1];
            if (k.indexOf('config.') !== 0) {
                data[k] = v;
                return data;
            }
            if (!data.config) {
                data.config = {};
            }
            if (k === 'config.schedule.frequency' || k === 'config.schedule.interval') {
                if (!Array.isArray(data.config.schedule)) {
                    data.config.schedule = [null, null];
                }
            }
            if (k === 'config.schedule.frequency') {
                data.config.schedule[0] = parseInt(v, 10);
            }
            else if (k === 'config.schedule.interval') {
                data.config.schedule[1] = v;
            }
            else {
                data.config[k.substr(7)] = v;
            }
            return data;
        }, {});
    };
    MonitorModel.prototype.getTransformedValue = function (id) {
        return id.indexOf('config') === 0 ? this.getValue(id) : _super.prototype.getTransformedValue.call(this, id);
    };
    return MonitorModel;
}(FormModel));
export default MonitorModel;
//# sourceMappingURL=monitorModel.jsx.map