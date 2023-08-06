import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import ContextData from 'app/components/contextData';
import PreviewPanelItem from 'app/components/events/attachmentViewers/previewPanelItem';
import { getAttachmentUrl, } from 'app/components/events/attachmentViewers/utils';
var JsonViewer = /** @class */ (function (_super) {
    __extends(JsonViewer, _super);
    function JsonViewer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    JsonViewer.prototype.getEndpoints = function () {
        return [['attachmentJson', getAttachmentUrl(this.props)]];
    };
    JsonViewer.prototype.renderBody = function () {
        var attachmentJson = this.state.attachmentJson;
        if (!attachmentJson) {
            return null;
        }
        var json;
        try {
            json = JSON.parse(attachmentJson);
        }
        catch (e) {
            json = null;
        }
        return (<PreviewPanelItem>
        <StyledContextData data={json} maxDefaultDepth={4} preserveQuotes style={{ width: '100%' }} jsonConsts/>
      </PreviewPanelItem>);
    };
    return JsonViewer;
}(AsyncComponent));
export default JsonViewer;
var StyledContextData = styled(ContextData)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=jsonViewer.jsx.map