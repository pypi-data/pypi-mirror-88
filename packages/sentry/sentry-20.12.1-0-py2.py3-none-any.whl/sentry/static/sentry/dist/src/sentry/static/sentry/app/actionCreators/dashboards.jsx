import { addErrorMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
export function createDashboard(api, orgId, newDashboard) {
    var title = newDashboard.title, widgets = newDashboard.widgets;
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/", {
        method: 'POST',
        data: { title: title, widgets: widgets },
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            addErrorMessage(errorResponse);
        }
        else {
            addErrorMessage(t('Unable to create dashboard'));
        }
    });
    return promise;
}
export function updateDashboard(api, orgId, dashboard) {
    var data = {
        title: dashboard.title,
        widgets: dashboard.widgets,
    };
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/" + dashboard.id + "/", {
        method: 'PUT',
        data: data,
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            addErrorMessage(errorResponse);
        }
        else {
            addErrorMessage(t('Unable to update dashboard'));
        }
    });
    return promise;
}
export function deleteDashboard(api, orgId, dashboardId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/" + dashboardId + "/", {
        method: 'DELETE',
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            addErrorMessage(errorResponse);
        }
        else {
            addErrorMessage(t('Unable to delete dashboard'));
        }
    });
    return promise;
}
export function validateWidget(api, orgId, widget) {
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/widgets/", {
        method: 'POST',
        data: widget,
    });
    return promise;
}
//# sourceMappingURL=dashboards.jsx.map