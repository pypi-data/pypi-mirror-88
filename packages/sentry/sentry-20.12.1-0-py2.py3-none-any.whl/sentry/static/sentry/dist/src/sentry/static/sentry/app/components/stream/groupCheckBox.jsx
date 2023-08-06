import React from 'react';
import createReactClass from 'create-react-class';
import PropTypes from 'prop-types';
import Reflux from 'reflux';
import Checkbox from 'app/components/checkbox';
import { t } from 'app/locale';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
var GroupCheckBox = createReactClass({
    displayName: 'GroupCheckBox',
    propTypes: {
        id: PropTypes.string.isRequired,
    },
    mixins: [Reflux.listenTo(SelectedGroupStore, 'onSelectedGroupChange')],
    getInitialState: function () {
        return {
            isSelected: SelectedGroupStore.isSelected(this.props.id),
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                isSelected: SelectedGroupStore.isSelected(nextProps.id),
            });
        }
    },
    shouldComponentUpdate: function (_nextProps, nextState) {
        return nextState.isSelected !== this.state.isSelected;
    },
    onSelectedGroupChange: function () {
        var isSelected = SelectedGroupStore.isSelected(this.props.id);
        if (isSelected !== this.state.isSelected) {
            this.setState({
                isSelected: isSelected,
            });
        }
    },
    onSelect: function () {
        var id = this.props.id;
        SelectedGroupStore.toggleSelect(id);
    },
    render: function () {
        return (<Checkbox aria-label={t('Select Issue')} value={this.props.id} checked={this.state.isSelected} onChange={this.onSelect}/>);
    },
});
export default GroupCheckBox;
//# sourceMappingURL=groupCheckBox.jsx.map