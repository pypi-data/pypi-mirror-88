import React from 'react';
import Link from 'app/components/links/link';
import Tag from 'app/components/tag';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
var DeployBadge = function (_a) {
    var deploy = _a.deploy, orgSlug = _a.orgSlug, projectId = _a.projectId, version = _a.version, className = _a.className;
    var shouldLinkToIssues = !!orgSlug && !!version;
    var badge = (<Tag className={className} type="highlight" icon={shouldLinkToIssues && <IconOpen />} textMaxWidth={80} tooltipText={shouldLinkToIssues ? t('Open In Issues') : undefined}>
      {deploy.environment}
    </Tag>);
    if (!shouldLinkToIssues) {
        return badge;
    }
    return (<Link to={{
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId !== null && projectId !== void 0 ? projectId : null,
            environment: deploy.environment,
            query: stringifyQueryObject(new QueryResults(["release:" + version])),
        },
    }}>
      {badge}
    </Link>);
};
export default DeployBadge;
//# sourceMappingURL=deployBadge.jsx.map