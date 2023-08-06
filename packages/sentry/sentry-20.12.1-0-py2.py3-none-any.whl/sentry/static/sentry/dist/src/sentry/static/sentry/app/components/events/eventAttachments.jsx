import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import Feature from 'app/components/acl/feature';
import ImageViewer from 'app/components/events/attachmentViewers/imageViewer';
import JsonViewer from 'app/components/events/attachmentViewers/jsonViewer';
import LogFileViewer from 'app/components/events/attachmentViewers/logFileViewer';
import RRWebJsonViewer from 'app/components/events/attachmentViewers/rrwebJsonViewer';
import EventAttachmentActions from 'app/components/events/eventAttachmentActions';
import EventDataSection from 'app/components/events/eventDataSection';
import FileSize from 'app/components/fileSize';
import { PanelTable } from 'app/components/panels';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import AttachmentUrl from 'app/utils/attachmentUrl';
import withApi from 'app/utils/withApi';
import EventAttachmentsCrashReportsNotice from './eventAttachmentsCrashReportsNotice';
var EventAttachments = /** @class */ (function (_super) {
    __extends(EventAttachments, _super);
    function EventAttachments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            attachmentList: [],
            expanded: false,
            attachmentPreviews: {},
        };
        _this.handleDelete = function (deletedAttachmentId) { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.setState(function (prevState) { return ({
                    attachmentList: prevState.attachmentList.filter(function (attachment) { return attachment.id !== deletedAttachmentId; }),
                }); });
                return [2 /*return*/];
            });
        }); };
        _this.attachmentPreviewIsOpen = function (attachment) {
            return !!_this.state.attachmentPreviews[attachment.id];
        };
        return _this;
    }
    EventAttachments.prototype.componentDidMount = function () {
        this.fetchData();
    };
    EventAttachments.prototype.componentDidUpdate = function (prevProps) {
        var doFetch = false;
        if (!prevProps.event && this.props.event) {
            // going from having no event to having an event
            doFetch = true;
        }
        else if (this.props.event && this.props.event.id !== prevProps.event.id) {
            doFetch = true;
        }
        if (doFetch) {
            this.fetchData();
        }
    };
    // TODO(dcramer): this API request happens twice, and we need a store for it
    EventAttachments.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var event, data, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        event = this.props.event;
                        if (!event) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + this.props.orgId + "/" + this.props.projectId + "/events/" + event.id + "/attachments/")];
                    case 2:
                        data = _a.sent();
                        this.setState({
                            attachmentList: data,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        // TODO: Error-handling
                        this.setState({
                            attachmentList: [],
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    EventAttachments.prototype.getInlineAttachmentRenderer = function (attachment) {
        switch (attachment.mimetype) {
            case 'text/plain':
                return attachment.size > 0 ? LogFileViewer : undefined;
            case 'text/json':
            case 'text/x-json':
            case 'application/json':
                if (attachment.name === 'rrweb.json') {
                    return RRWebJsonViewer;
                }
                return JsonViewer;
            case 'image/jpeg':
            case 'image/png':
            case 'image/gif':
                return ImageViewer;
            default:
                return undefined;
        }
    };
    EventAttachments.prototype.hasInlineAttachmentRenderer = function (attachment) {
        return !!this.getInlineAttachmentRenderer(attachment);
    };
    EventAttachments.prototype.renderInlineAttachment = function (attachment) {
        var Component = this.getInlineAttachmentRenderer(attachment);
        if (!Component || !this.attachmentPreviewIsOpen(attachment)) {
            return null;
        }
        return (<AttachmentPreviewWrapper>
        <Component orgId={this.props.orgId} projectId={this.props.projectId} event={this.props.event} attachment={attachment}/>
      </AttachmentPreviewWrapper>);
    };
    EventAttachments.prototype.togglePreview = function (attachment) {
        this.setState(function (_a) {
            var _b;
            var attachmentPreviews = _a.attachmentPreviews;
            return ({
                attachmentPreviews: __assign(__assign({}, attachmentPreviews), (_b = {}, _b[attachment.id] = !attachmentPreviews[attachment.id], _b)),
            });
        });
    };
    EventAttachments.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, projectId = _a.projectId, orgId = _a.orgId, location = _a.location;
        var attachmentList = this.state.attachmentList;
        var crashFileStripped = event.metadata.stripped_crash;
        if (!attachmentList.length && !crashFileStripped) {
            return null;
        }
        var title = t('Attachments (%s)', attachmentList.length);
        var lastAttachmentPreviewed = attachmentList.length > 0 &&
            this.attachmentPreviewIsOpen(attachmentList[attachmentList.length - 1]);
        return (<EventDataSection type="attachments" title={title}>
        {crashFileStripped && (<EventAttachmentsCrashReportsNotice orgSlug={orgId} projectSlug={projectId} groupId={event.groupID} location={location}/>)}

        {attachmentList.length > 0 && (<StyledPanelTable headers={[
            <Name key="name">{t('File Name')}</Name>,
            <Size key="size">{t('Size')}</Size>,
            t('Actions'),
        ]}>
            {attachmentList.map(function (attachment) { return (<React.Fragment key={attachment.id}>
                <Name>{attachment.name}</Name>
                <Size>
                  <FileSize bytes={attachment.size}/>
                </Size>
                <AttachmentUrl projectId={projectId} eventId={event.id} attachment={attachment}>
                  {function (url) { return (<div>
                      <EventAttachmentActions url={url} onDelete={_this.handleDelete} onPreview={function (_attachmentId) { return _this.togglePreview(attachment); }} withPreviewButton previewIsOpen={_this.attachmentPreviewIsOpen(attachment)} hasPreview={_this.hasInlineAttachmentRenderer(attachment)} attachmentId={attachment.id}/>
                    </div>); }}
                </AttachmentUrl>
                <Feature features={['event-attachments-viewer']}>
                  {_this.renderInlineAttachment(attachment)}

                  
                  {lastAttachmentPreviewed && (<React.Fragment>
                      <div style={{ display: 'none' }}/>
                      <div style={{ display: 'none' }}/>
                    </React.Fragment>)}
                </Feature>
              </React.Fragment>); })}
          </StyledPanelTable>)}
      </EventDataSection>);
    };
    EventAttachments.propTypes = {
        api: PropTypes.object.isRequired,
        event: PropTypes.object.isRequired,
        orgId: PropTypes.string.isRequired,
        projectId: PropTypes.string.isRequired,
    };
    return EventAttachments;
}(React.Component));
export default withApi(EventAttachments);
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 1fr auto auto;\n"], ["\n  grid-template-columns: 1fr auto auto;\n"])));
var Name = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var Size = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var AttachmentPreviewWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-column: auto / span 3;\n  border: none;\n  padding: 0;\n"], ["\n  grid-column: auto / span 3;\n  border: none;\n  padding: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventAttachments.jsx.map