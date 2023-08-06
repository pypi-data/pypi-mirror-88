import { __decorate, __extends, __makeTemplateObject, __read, __rest, __spread } from "tslib";
import React from 'react';
import keydown from 'react-keydown';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import PlatformIcon from 'platformicons';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import categoryList from 'app/data/platformCategories';
import platforms from 'app/data/platforms';
import { IconClose, IconProject, IconSearch } from 'app/icons';
import { t, tct } from 'app/locale';
import { inputStyles } from 'app/styles/input';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var PLATFORM_CATEGORIES = __spread(categoryList, [{ id: 'all', name: t('All') }]);
var PlatformPicker = /** @class */ (function (_super) {
    __extends(PlatformPicker, _super);
    function PlatformPicker() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            category: PLATFORM_CATEGORIES[0].id,
            filter: _this.props.noAutoFilter ? '' : (_this.props.platform || '').split('-')[0],
        };
        _this.logSearch = debounce(function () {
            if (_this.state.filter) {
                analytics('platformpicker.search', {
                    query: _this.state.filter.toLowerCase(),
                    num_results: _this.platformList.length,
                });
            }
        }, 300);
        _this.searchInput = React.createRef();
        return _this;
    }
    Object.defineProperty(PlatformPicker.prototype, "platformList", {
        get: function () {
            var category = this.state.category;
            var currentCategory = categoryList.find(function (_a) {
                var id = _a.id;
                return id === category;
            });
            var filter = this.state.filter.toLowerCase();
            var subsetMatch = function (platform) {
                return platform.id.includes(filter) || platform.name.toLowerCase().includes(filter);
            };
            var categoryMatch = function (platform) {
                var _a;
                return category === 'all' || ((_a = currentCategory === null || currentCategory === void 0 ? void 0 : currentCategory.platforms) === null || _a === void 0 ? void 0 : _a.includes(platform.id));
            };
            var filtered = platforms
                .filter(this.state.filter ? subsetMatch : categoryMatch)
                .sort(function (a, b) { return a.id.localeCompare(b.id); });
            return this.props.showOther ? filtered : filtered.filter(function (_a) {
                var id = _a.id;
                return id !== 'other';
            });
        },
        enumerable: false,
        configurable: true
    });
    PlatformPicker.prototype.focusSearch = function (e) {
        var _a, _b;
        if (e.target !== this.searchInput.current) {
            (_b = (_a = this.searchInput) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.focus();
            e.preventDefault();
        }
    };
    PlatformPicker.prototype.render = function () {
        var _this = this;
        var platformList = this.platformList;
        var _a = this.props, setPlatform = _a.setPlatform, listProps = _a.listProps, listClassName = _a.listClassName;
        var _b = this.state, filter = _b.filter, category = _b.category;
        return (<React.Fragment>
        <NavContainer>
          <CategoryNav>
            {PLATFORM_CATEGORIES.map(function (_a) {
            var id = _a.id, name = _a.name;
            return (<ListLink key={id} onClick={function (e) {
                analytics('platformpicker.select_tab', { category: id });
                _this.setState({ category: id, filter: '' });
                e.preventDefault();
            }} to="" isActive={function () { return id === (filter ? 'all' : category); }}>
                {name}
              </ListLink>);
        })}
          </CategoryNav>
          <SearchBar>
            <IconSearch size="xs"/>
            <input type="text" ref={this.searchInput} value={filter} placeholder={t('Filter Platforms')} onChange={function (e) { return _this.setState({ filter: e.target.value }, _this.logSearch); }}/>
          </SearchBar>
        </NavContainer>
        <PlatformList className={listClassName} {...listProps}>
          {platformList.map(function (platform) { return (<PlatformCard data-test-id={"platform-" + platform.id} key={platform.id} platform={platform} selected={_this.props.platform === platform.id} onClear={function (e) {
            setPlatform(null);
            e.stopPropagation();
        }} onClick={function () {
            analytics('platformpicker.select_platform', { platform: platform.id });
            setPlatform(platform.id);
        }}/>); })}
        </PlatformList>
        {platformList.length === 0 && (<EmptyMessage icon={<IconProject size="xl"/>} title={t("We don't have an SDK for that yet!")}>
            {tct("Not finding your platform? You can still create your project,\n              but looks like we don't have an official SDK for your platform\n              yet. However, there's a rich ecosystem of community supported\n              SDKs (including Perl, CFML, Clojure, and ActionScript). Try\n              [search:searching for Sentry clients] or contacting support.", {
            search: (<ExternalLink href="https://github.com/search?q=-org%3Agetsentry+topic%3Asentry&type=Repositories"/>),
        })}
          </EmptyMessage>)}
      </React.Fragment>);
    };
    PlatformPicker.defaultProps = {
        showOther: true,
    };
    __decorate([
        keydown('/')
    ], PlatformPicker.prototype, "focusSearch", null);
    return PlatformPicker;
}(React.Component));
var NavContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  margin-bottom: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr minmax(0, 300px);\n  align-items: start;\n"], ["\n  border-bottom: 1px solid ", ";\n  margin-bottom: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr minmax(0, 300px);\n  align-items: start;\n"])), function (p) { return p.theme.border; }, space(2), space(2));
var SearchBar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  padding: 0 8px;\n  color: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 15px;\n\n  input {\n    border: none;\n    background: none;\n    padding: 2px 4px;\n    width: 100%;\n    /* Ensure a consistent line height to keep the input the desired height */\n    line-height: 24px;\n\n    &:focus {\n      outline: none;\n    }\n  }\n"], ["\n  ", ";\n  padding: 0 8px;\n  color: ", ";\n  display: flex;\n  align-items: center;\n  font-size: 15px;\n\n  input {\n    border: none;\n    background: none;\n    padding: 2px 4px;\n    width: 100%;\n    /* Ensure a consistent line height to keep the input the desired height */\n    line-height: 24px;\n\n    &:focus {\n      outline: none;\n    }\n  }\n"])), function (p) { return inputStyles(p); }, function (p) { return p.theme.subText; });
var CategoryNav = styled(NavTabs)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0;\n  margin-top: 4px;\n  white-space: nowrap;\n\n  > li {\n    float: none;\n    display: inline-block;\n  }\n"], ["\n  margin: 0;\n  margin-top: 4px;\n  white-space: nowrap;\n\n  > li {\n    float: none;\n    display: inline-block;\n  }\n"])));
var PlatformList = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 112px);\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(auto-fill, 112px);\n  margin-bottom: ", ";\n"])), space(1), space(2));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(2));
var ClearButton = styled(function (p) { return (<Button {...p} icon={<IconClose isCircled size="xs"/>} size="xsmall" borderless/>); })(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: absolute;\n  top: -6px;\n  right: -6px;\n  height: 22px;\n  width: 22px;\n  border-radius: 50%;\n  background: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  top: -6px;\n  right: -6px;\n  height: 22px;\n  width: 22px;\n  border-radius: 50%;\n  background: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.textColor; });
var PlatformCard = styled(function (_a) {
    var platform = _a.platform, selected = _a.selected, onClear = _a.onClear, props = __rest(_a, ["platform", "selected", "onClear"]);
    return (<div {...props}>
    <StyledPlatformIcon platform={platform.id} size={56} radius={5} withLanguageIcon format="lg"/>

    <h3>{platform.name}</h3>
    {selected && <ClearButton onClick={onClear}/>}
  </div>);
})(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  padding: 0 0 14px;\n  border-radius: 4px;\n  cursor: pointer;\n  background: ", ";\n\n  &:hover {\n    background: #ebebef;\n  }\n\n  h3 {\n    flex-grow: 1;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 100%;\n    text-align: center;\n    font-size: 15px;\n    margin: 0;\n    padding: 0 ", ";\n    line-height: 1.2;\n  }\n"], ["\n  position: relative;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  padding: 0 0 14px;\n  border-radius: 4px;\n  cursor: pointer;\n  background: ", ";\n\n  &:hover {\n    background: #ebebef;\n  }\n\n  h3 {\n    flex-grow: 1;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 100%;\n    text-align: center;\n    font-size: 15px;\n    margin: 0;\n    padding: 0 ", ";\n    line-height: 1.2;\n  }\n"])), function (p) { return p.selected && '#ecf5fd'; }, space(0.5));
export default PlatformPicker;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=platformPicker.jsx.map