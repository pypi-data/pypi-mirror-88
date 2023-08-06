import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import SentryTypes from 'app/sentryTypes';
import ProjectsStore from 'app/stores/projectsStore';
import getDisplayName from 'app/utils/getDisplayName';
/**
 * Higher order component that uses ProjectsStore and provides a list of projects
 */
var withProjects = function (WrappedComponent) {
    return createReactClass({
        displayName: "withProjects(" + getDisplayName(WrappedComponent) + ")",
        propTypes: {
            organization: SentryTypes.Organization,
            project: SentryTypes.Project,
        },
        mixins: [Reflux.listenTo(ProjectsStore, 'onProjectUpdate')],
        getInitialState: function () {
            return ProjectsStore.getState();
        },
        onProjectUpdate: function () {
            this.setState(ProjectsStore.getState());
        },
        render: function () {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        },
    });
};
export default withProjects;
//# sourceMappingURL=withProjects.jsx.map