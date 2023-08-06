import { __extends } from "tslib";
import React from 'react';
import { browserHistory, Router } from 'react-router';
import { CacheProvider } from '@emotion/core'; // This is needed to set "speedy" = false (for percy)
import { cache } from 'emotion'; // eslint-disable-line emotion/no-vanilla
import { ThemeProvider } from 'emotion-theming';
import { loadPreferencesState } from 'app/actionCreators/preferences';
import routes from 'app/routes';
import ConfigStore from 'app/stores/configStore';
import GlobalStyles from 'app/styles/global';
import theme, { darkTheme } from 'app/utils/theme';
import withConfig from 'app/utils/withConfig';
var Main = /** @class */ (function (_super) {
    __extends(Main, _super);
    function Main() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            theme: ConfigStore.get('theme') === 'dark' ? darkTheme : theme,
        };
        return _this;
    }
    Main.prototype.componentDidMount = function () {
        loadPreferencesState();
    };
    Main.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (config.theme !== prevProps.config.theme) {
            // eslint-disable-next-line
            this.setState({
                theme: config.theme === 'dark' ? darkTheme : theme,
            });
        }
    };
    Main.prototype.render = function () {
        return (<ThemeProvider theme={this.state.theme}>
        <GlobalStyles isDark={this.props.config.theme === 'dark'} theme={this.state.theme}/>
        <CacheProvider value={cache}>
          <Router history={browserHistory}>{routes()}</Router>
        </CacheProvider>
      </ThemeProvider>);
    };
    return Main;
}(React.Component));
export default withConfig(Main);
//# sourceMappingURL=main.jsx.map