export function getAttachmentUrl(props, withPrefix) {
    var orgId = props.orgId, projectId = props.projectId, event = props.event, attachment = props.attachment;
    return (withPrefix ? '/api/0' : '') + "/projects/" + orgId + "/" + projectId + "/events/" + event.id + "/attachments/" + attachment.id + "/?download";
}
//# sourceMappingURL=utils.jsx.map