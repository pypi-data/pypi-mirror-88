import { __extends } from "tslib";
import React from 'react';
import Pagination from 'app/components/pagination';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import OrganizationRepositories from './organizationRepositories';
var OrganizationRepositoriesContainer = /** @class */ (function (_super) {
    __extends(OrganizationRepositoriesContainer, _super);
    function OrganizationRepositoriesContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Callback used by child component to signal state change
        _this.onRepositoryChange = function (data) {
            var itemList = _this.state.itemList;
            itemList === null || itemList === void 0 ? void 0 : itemList.forEach(function (item) {
                if (item.id === data.id) {
                    item.status = data.status;
                }
            });
            _this.setState({ itemList: itemList });
        };
        return _this;
    }
    OrganizationRepositoriesContainer.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [
            ['itemList', "/organizations/" + orgId + "/repos/", { query: { status: '' } }],
            ['repoConfig', "/organizations/" + orgId + "/config/repos/"],
        ];
    };
    OrganizationRepositoriesContainer.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitleGen(t('Repositories'), orgId, false);
    };
    OrganizationRepositoriesContainer.prototype.renderBody = function () {
        return (<React.Fragment>
        <OrganizationRepositories {...this.props} itemList={this.state.itemList} api={this.api} onRepositoryChange={this.onRepositoryChange}/>
        {this.state.itemListPageLinks && (<Pagination pageLinks={this.state.itemListPageLinks} {...this.props}/>)}
      </React.Fragment>);
    };
    return OrganizationRepositoriesContainer;
}(AsyncView));
export default OrganizationRepositoriesContainer;
//# sourceMappingURL=index.jsx.map