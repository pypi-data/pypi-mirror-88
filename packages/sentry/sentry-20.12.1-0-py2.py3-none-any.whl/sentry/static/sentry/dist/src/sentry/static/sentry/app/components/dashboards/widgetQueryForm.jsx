import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import { fetchSavedQueries } from 'app/actionCreators/discoverSavedQueries';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { explodeField, generateFieldAsString, } from 'app/utils/discover/fields';
import SearchBar from 'app/views/events/searchBar';
import { QueryField } from 'app/views/eventsV2/table/queryField';
import Input from 'app/views/settings/components/forms/controls/input';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
import Field from 'app/views/settings/components/forms/field';
/**
 * Contain widget query interactions and signal changes via the onChange
 * callback. This component's state should live in the parent.
 */
var WidgetQueryForm = /** @class */ (function (_super) {
    __extends(WidgetQueryForm, _super);
    function WidgetQueryForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            selectedQuery: null,
            source: 'new',
        };
        // Handle scalar field values changing.
        _this.handleFieldChange = function (field) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            return function handleChange(value) {
                var _a;
                var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
                onChange(newQuery);
            };
        };
        // Handle new fields being added.
        _this.handleAddField = function (event) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            event.preventDefault();
            var newQuery = __assign(__assign({}, widgetQuery), { fields: __spread(widgetQuery.fields, ['']) });
            onChange(newQuery);
        };
        // Remove fields from the field list and signal an update.
        _this.handleRemoveField = function (event, fieldIndex) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            event.preventDefault();
            var newQuery = cloneDeep(widgetQuery);
            newQuery.fields.splice(fieldIndex, fieldIndex + 1);
            onChange(newQuery);
        };
        _this.handleQueryField = function (fieldIndex, value) {
            var _a = _this.props, widgetQuery = _a.widgetQuery, onChange = _a.onChange;
            var newQuery = cloneDeep(widgetQuery);
            set(newQuery, "fields." + fieldIndex, generateFieldAsString(value));
            onChange(newQuery);
        };
        _this.handleSavedQueryChange = function (option) {
            var _a, _b;
            var _c = _this.props, onChange = _c.onChange, widgetQuery = _c.widgetQuery;
            var newQuery = cloneDeep(widgetQuery);
            newQuery.fields = [(_a = option.query.yAxis) !== null && _a !== void 0 ? _a : 'count()'];
            newQuery.conditions = (_b = option.query.query) !== null && _b !== void 0 ? _b : '';
            newQuery.name = option.query.name;
            onChange(newQuery);
            _this.setState({ selectedQuery: option });
        };
        _this.handleLoadOptions = function (inputValue) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            return new Promise(function (resolve, reject) {
                fetchSavedQueries(api, organization.slug, inputValue)
                    .then(function (queries) {
                    var results = queries.map(function (query) { return ({
                        label: query.name,
                        value: query.id,
                        query: query,
                    }); });
                    resolve(results);
                })
                    .catch(reject);
            });
        };
        _this.handleSourceChange = function (value) {
            _this.setState(function (prevState) {
                return __assign(__assign({}, prevState), { source: value, selectedQuery: value === 'new' ? null : prevState.selectedQuery });
            });
        };
        return _this;
    }
    WidgetQueryForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, canRemove = _a.canRemove, errors = _a.errors, fieldOptions = _a.fieldOptions, organization = _a.organization, selection = _a.selection, widgetQuery = _a.widgetQuery;
        var _b = this.state, selectedQuery = _b.selectedQuery, source = _b.source;
        return (<QueryWrapper>
        {canRemove && (<RemoveButtonWrapper>
            <Button data-test-id="remove-query" priority="default" size="zero" borderless onClick={this.props.onRemove} icon={<IconDelete />} title={t('Remove this query')}/>
          </RemoveButtonWrapper>)}
        <Field data-test-id="source" label="Source" inline={false} flexibleControlStateSize stacked required>
          <RadioGroup orientInline value={this.state.source} label="" onChange={this.handleSourceChange} choices={[
            ['new', t('New Query')],
            ['existing', t('Existing Discover Query')],
        ]}/>
        </Field>
        {source === 'new' && (<Field data-test-id="new-query" label={t('Query')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.conditions} required>
            <SearchBar organization={organization} projectIds={selection.projects} query={widgetQuery.conditions} fields={[]} onSearch={this.handleFieldChange('conditions')} onBlur={this.handleFieldChange('conditions')} useFormWrapper={false}/>
          </Field>)}
        {source === 'existing' && (<Feature organization={organization} features={['discover-query']}>
            {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<Field data-test-id="discover-query" label={t('Query')} inline={false} flexibleControlStateSize stacked required>
                <SelectControl async defaultOptions value={selectedQuery} name="discoverQuery" loadOptions={_this.handleLoadOptions} onChange={_this.handleSavedQueryChange} options={[]} disabled={!hasFeature} cache onSelectResetsInput={false} onCloseResetsInput={false} onBlurResetsInput={false}/>
              </Field>);
        }}
          </Feature>)}
        {canRemove && (<Field data-test-id="Query Name" label="Y-Axis" inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.name}>
            <Input type="text" name="name" required value={widgetQuery.name} onChange={function (event) { return _this.handleFieldChange('name')(event.target.value); }}/>
          </Field>)}
        <Field data-test-id="y-axis" label="Y-Axis" inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.fields} required>
          {widgetQuery.fields.map(function (field, i) { return (<QueryFieldWrapper key={field + ":" + i}>
              <QueryField fieldValue={explodeField({ field: field })} fieldOptions={fieldOptions} onChange={function (value) { return _this.handleQueryField(i, value); }}/>
              {widgetQuery.fields.length > 1 && (<Button size="zero" borderless onClick={function (event) { return _this.handleRemoveField(event, i); }} icon={<IconDelete />} title={t('Remove this field')}/>)}
            </QueryFieldWrapper>); })}
          <div>
            <Button data-test-id="add-field" size="small" onClick={this.handleAddField} icon={<IconAdd isCircled/>}>
              {t('Add an overlay')}
            </Button>
          </div>
        </Field>
      </QueryWrapper>);
    };
    return WidgetQueryForm;
}(React.Component));
var QueryWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space(2));
var QueryFieldWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space(1), space(1));
var RemoveButtonWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n"])), space(2), space(2));
export default WidgetQueryForm;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=widgetQueryForm.jsx.map