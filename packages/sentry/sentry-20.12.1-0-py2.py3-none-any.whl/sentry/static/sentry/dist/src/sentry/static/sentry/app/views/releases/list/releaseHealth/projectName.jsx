import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import space from 'app/styles/space';
var ProjectName = function (_a) {
    var orgSlug = _a.orgSlug, releaseVersion = _a.releaseVersion, project = _a.project;
    return (<GlobalSelectionLink to={{
        pathname: "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/",
        query: { project: project.id },
    }}>
    <StyledProjectBadge project={project} avatarSize={16}/>
  </GlobalSelectionLink>);
};
export default ProjectName;
var StyledProjectBadge = styled(ProjectBadge)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    padding-right: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    padding-right: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var templateObject_1;
//# sourceMappingURL=projectName.jsx.map