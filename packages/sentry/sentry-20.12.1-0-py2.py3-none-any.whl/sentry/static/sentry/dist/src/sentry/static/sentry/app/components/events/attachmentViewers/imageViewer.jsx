import React from 'react';
import { getAttachmentUrl, } from 'app/components/events/attachmentViewers/utils';
import { PanelItem } from 'app/components/panels';
export default function ImageViewer(props) {
    return (<PanelItem justifyContent="center">
      <img src={getAttachmentUrl(props, true)}/>
    </PanelItem>);
}
//# sourceMappingURL=imageViewer.jsx.map