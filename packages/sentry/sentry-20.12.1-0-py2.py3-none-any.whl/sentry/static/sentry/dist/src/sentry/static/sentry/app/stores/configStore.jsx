import { __assign } from "tslib";
import moment from 'moment-timezone';
import * as qs from 'query-string';
import Reflux from 'reflux';
import { setLocale } from 'app/locale';
var configStoreConfig = {
    // When the app is booted we will _immediately_ hydrate the config store,
    // effecively ensureing this is not empty.
    config: {},
    init: function () {
        this.config = {};
    },
    get: function (key) {
        return this.config[key];
    },
    set: function (key, value) {
        var _a, _b;
        this.config = __assign(__assign({}, this.config), (_a = {}, _a[key] = value, _a));
        this.trigger((_b = {}, _b[key] = value, _b));
    },
    /**
     * This is only called by media query listener so that we can control
     * the auto switching of color schemes without affecting manual toggle
     */
    updateTheme: function (theme) {
        var _a;
        if (((_a = this.config.user) === null || _a === void 0 ? void 0 : _a.options.theme) !== 'system') {
            return;
        }
        this.set('theme', theme);
    },
    getConfig: function () {
        return this.config;
    },
    loadInitialData: function (config) {
        var _a, _b;
        // TODO(dark): Remove staff requirement and add dark mode user preference
        var shouldUseDarkMode = 
        // @ts-ignore
        ((_a = config.user) === null || _a === void 0 ? void 0 : _a.isStaff) && ((_b = config.user) === null || _b === void 0 ? void 0 : _b.options.theme) === 'dark';
        this.config = __assign(__assign({}, config), { features: new Set(config.features || []), theme: shouldUseDarkMode ? 'dark' : 'light' });
        // Language code is passed from django
        var languageCode = config.languageCode;
        // TODO(dcramer): abstract this out of ConfigStore
        if (config.user) {
            config.user.permissions = new Set(config.user.permissions);
            moment.tz.setDefault(config.user.options.timezone);
            var queryString = {};
            // Parse query string for `lang`
            try {
                queryString = qs.parse(window.location.search) || {};
            }
            catch (err) {
                // ignore if this fails to parse
                // this can happen if we have an invalid query string
                // e.g. unencoded "%"
            }
            var queryStringLang = queryString.lang;
            if (Array.isArray(queryStringLang)) {
                queryStringLang = queryStringLang[0];
            }
            languageCode = queryStringLang || config.user.options.language || languageCode;
        }
        // Priority:
        // "?lang=en" --> user configuration options --> django request.LANGUAGE_CODE --> "en"
        setLocale(languageCode || 'en');
        this.trigger(config);
    },
};
export default Reflux.createStore(configStoreConfig);
//# sourceMappingURL=configStore.jsx.map