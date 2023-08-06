import { __awaiter, __extends, __generator, __read, __spread } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import recreateRoute from 'app/utils/recreateRoute';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import OrganizationApiKeysList from './organizationApiKeysList';
/**
 * API Keys are deprecated, but there may be some legacy customers that still use it
 */
var OrganizationApiKeys = /** @class */ (function (_super) {
    __extends(OrganizationApiKeys, _super);
    function OrganizationApiKeys() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleRemove = function (id) { return __awaiter(_this, void 0, void 0, function () {
            var oldKeys, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        oldKeys = __spread(this.state.keys);
                        this.setState(function (state) { return ({
                            keys: state.keys.filter(function (_a) {
                                var existingId = _a.id;
                                return existingId !== id;
                            }),
                        }); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.params.orgId + "/api-keys/" + id + "/", {
                                method: 'DELETE',
                                data: {},
                            })];
                    case 2:
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ keys: oldKeys, busy: false });
                        addErrorMessage(t('Error removing key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleAddApiKey = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({
                            busy: true,
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.params.orgId + "/api-keys/", {
                                method: 'POST',
                                data: {},
                            })];
                    case 2:
                        data = _b.sent();
                        if (data) {
                            this.setState({ busy: false });
                            browserHistory.push(recreateRoute(data.id + "/", {
                                params: this.props.params,
                                routes: this.props.routes,
                            }));
                            addSuccessMessage(t("Created a new API key \"" + data.label + "\""));
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        this.setState({ busy: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    OrganizationApiKeys.prototype.getEndpoints = function () {
        return [['keys', "/organizations/" + this.props.params.orgId + "/api-keys/"]];
    };
    OrganizationApiKeys.prototype.getTitle = function () {
        return routeTitleGen(t('API Keys'), this.props.organization.slug, false);
    };
    OrganizationApiKeys.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationApiKeys.prototype.renderBody = function () {
        return (<OrganizationApiKeysList loading={this.state.loading} busy={this.state.busy} keys={this.state.keys} onRemove={this.handleRemove} onAddApiKey={this.handleAddApiKey} {...this.props}/>);
    };
    return OrganizationApiKeys;
}(AsyncView));
export default withOrganization(OrganizationApiKeys);
//# sourceMappingURL=index.jsx.map