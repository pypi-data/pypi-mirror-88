import { __read, __spread } from "tslib";
var StreamManager = /** @class */ (function () {
    // TODO(dcramer): this should listen to changes on GroupStore and remove
    // items that are removed there
    // TODO(ts) Add better typing for store. Generally this is GroupStore, but it could be other things.
    function StreamManager(store, options) {
        if (options === void 0) { options = {}; }
        this.idList = [];
        this.store = store;
        this.limit = options.limit || 100;
    }
    StreamManager.prototype.trim = function () {
        if (this.limit > this.idList.length) {
            return;
        }
        var excess = this.idList.splice(this.limit, this.idList.length - this.limit);
        this.store.remove(excess);
    };
    StreamManager.prototype.push = function (items) {
        if (items === void 0) { items = []; }
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return;
        }
        items = items.filter(function (item) { return item.hasOwnProperty('id'); });
        var ids = items.map(function (item) { return item.id; });
        this.idList = this.idList.filter(function (id) { return !ids.includes(id); });
        this.idList = __spread(this.idList, ids);
        this.trim();
        this.store.add(items);
    };
    StreamManager.prototype.getAllItems = function () {
        var _this = this;
        return this.store
            .getAllItems()
            .slice()
            .sort(function (a, b) { return _this.idList.indexOf(a.id) - _this.idList.indexOf(b.id); });
    };
    StreamManager.prototype.unshift = function (items) {
        if (items === void 0) { items = []; }
        items = Array.isArray(items) ? items : [items];
        if (items.length === 0) {
            return;
        }
        var ids = items.map(function (item) { return item.id; });
        this.idList = this.idList.filter(function (id) { return !ids.includes(id); });
        this.idList = __spread(ids, this.idList);
        this.trim();
        this.store.add(items);
    };
    return StreamManager;
}());
export default StreamManager;
//# sourceMappingURL=streamManager.jsx.map