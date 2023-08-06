import { __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import { IconDelete, IconEdit } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { logException } from 'app/utils/logging';
import withApi from 'app/utils/withApi';
var MonitorHeaderActions = function (_a) {
    var api = _a.api, monitor = _a.monitor, orgId = _a.orgId, onUpdate = _a.onUpdate;
    var handleDelete = function () {
        var redirectPath = "/organizations/" + orgId + "/monitors/";
        addLoadingMessage(t('Deleting Monitor...'));
        api
            .requestPromise("/monitors/" + monitor.id + "/", {
            method: 'DELETE',
        })
            .then(function () {
            browserHistory.push(redirectPath);
        })
            .catch(function () {
            addErrorMessage(t('Unable to remove monitor.'));
        });
    };
    var updateMonitor = function (data) {
        addLoadingMessage();
        api
            .requestPromise("/monitors/" + monitor.id + "/", {
            method: 'PUT',
            data: data,
        })
            .then(function (resp) {
            clearIndicators();
            onUpdate === null || onUpdate === void 0 ? void 0 : onUpdate(resp);
        })
            .catch(function (err) {
            logException(err);
            addErrorMessage(t('Unable to update monitor.'));
        });
    };
    var toggleStatus = function () {
        return updateMonitor({
            status: monitor.status === 'disabled' ? 'active' : 'disabled',
        });
    };
    return (<ButtonContainer>
      <ButtonBar gap={1}>
        <Button size="small" icon={<IconEdit size="xs"/>} to={"/organizations/" + orgId + "/monitors/" + monitor.id + "/edit/"}>
          &nbsp;
          {t('Edit')}
        </Button>
        <Button size="small" onClick={toggleStatus}>
          {monitor.status !== 'disabled' ? t('Pause') : t('Enable')}
        </Button>
        <Confirm onConfirm={handleDelete} message={t('Deleting this monitor is permanent. Are you sure you wish to continue?')}>
          <Button size="small" icon={<IconDelete size="xs"/>}>
            {t('Delete')}
          </Button>
        </Confirm>
      </ButtonBar>
    </ButtonContainer>);
};
var ButtonContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  display: flex;\n  flex-shrink: 1;\n"], ["\n  margin-bottom: ", ";\n  display: flex;\n  flex-shrink: 1;\n"])), space(3));
export default withApi(MonitorHeaderActions);
var templateObject_1;
//# sourceMappingURL=monitorHeaderActions.jsx.map