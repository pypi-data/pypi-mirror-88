var _a, _b, _c, _d;
import { __assign } from "tslib";
import { t } from 'app/locale';
export var SessionTerm;
(function (SessionTerm) {
    SessionTerm["CRASHES"] = "crashes";
    SessionTerm["CRASHED"] = "crashed";
    SessionTerm["ABNORMAL"] = "abnormal";
    SessionTerm["CRASH_FREE_USERS"] = "crash-free-users";
    SessionTerm["CRASH_FREE_SESSIONS"] = "crash-free-sessions";
    SessionTerm["HEALTHY"] = "healthy";
    SessionTerm["ERRORED"] = "errored";
    SessionTerm["UNHANDLED"] = "unhandled";
})(SessionTerm || (SessionTerm = {}));
export var sessionTerm = (_a = {},
    _a[SessionTerm.CRASHES] = t('Crashes'),
    _a[SessionTerm.CRASHED] = t('Crashed'),
    _a[SessionTerm.ABNORMAL] = t('Abnormal'),
    _a[SessionTerm.CRASH_FREE_USERS] = t('Crash Free Users'),
    _a[SessionTerm.CRASH_FREE_SESSIONS] = t('Crash Free Sessions'),
    _a[SessionTerm.HEALTHY] = t('Healthy'),
    _a[SessionTerm.ERRORED] = t('Errored'),
    _a[SessionTerm.UNHANDLED] = t('Unhandled'),
    _a);
// This should never be used directly (except in tests)
export var commonTermsDescription = (_b = {},
    _b[SessionTerm.CRASHES] = t('Number of sessions with a crashed state'),
    _b[SessionTerm.CRASH_FREE_USERS] = t('Number of unique users with non-crashed sessions'),
    _b[SessionTerm.CRASH_FREE_SESSIONS] = t('Number of non-crashed sessions'),
    _b);
// This should never be used directly (except in tests)
export var mobileTermsDescription = (_c = {},
    _c[SessionTerm.CRASHED] = t('The process was terminated due to an unhandled exception or a request to the server that ended with an error'),
    _c[SessionTerm.CRASH_FREE_SESSIONS] = t('Number of unique sessions that did not crash'),
    _c[SessionTerm.ABNORMAL] = t('An unknown session exit. Like due to loss of power or killed by the operating system'),
    _c[SessionTerm.HEALTHY] = t('A session without any errors'),
    _c[SessionTerm.ERRORED] = t('A crash which experienced errors'),
    _c[SessionTerm.UNHANDLED] = t('Not handled by user code'),
    _c);
// This should never be used directly (except in tests)
export var desktopTermDescriptions = (_d = {
        crashed: t('The application crashed with a hard crash (eg. segfault)')
    },
    _d[SessionTerm.ABNORMAL] = t('The application did not properly end the session, for example, due to force-quit'),
    _d[SessionTerm.HEALTHY] = t('The application exited normally and did not observe any errors'),
    _d[SessionTerm.ERRORED] = t('The application exited normally but observed error events while running'),
    _d[SessionTerm.UNHANDLED] = t('The application crashed with a hard crash'),
    _d);
function getTermDescriptions(platform) {
    var _a, _b, _c, _d, _e, _f;
    var technology = platform === 'react-native' ||
        platform === 'java-spring' ||
        platform === 'apple-ios' ||
        platform === 'dotnet-aspnetcore'
        ? platform
        : platform === null || platform === void 0 ? void 0 : platform.split('-')[0];
    switch (technology) {
        case 'dotnet':
        case 'java':
            return __assign(__assign({}, commonTermsDescription), mobileTermsDescription);
        case 'java-spring':
        case 'dotnet-aspnetcore':
            return __assign(__assign(__assign({}, commonTermsDescription), mobileTermsDescription), (_a = {}, _a[SessionTerm.CRASHES] = t('A request that resulted in an unhandled exception and hence a Server Error response'), _a));
        case 'android':
        case 'cordova':
        case 'react-native':
        case 'flutter':
            return __assign(__assign(__assign({}, commonTermsDescription), mobileTermsDescription), (_b = {}, _b[SessionTerm.CRASHED] = t('An unhandled exception that resulted in the application crashing'), _b));
        case 'apple': {
            return __assign(__assign(__assign({}, commonTermsDescription), mobileTermsDescription), (_c = {}, _c[SessionTerm.CRASHED] = t('An error that resulted in the application crashing'), _c));
        }
        case 'node':
        case 'javascript':
            return __assign(__assign({}, commonTermsDescription), (_d = {}, _d[SessionTerm.CRASHED] = t("During the session an error with mechanism.handled===false occurred calling the 'onerror' on 'unhandledrejection' handler"), _d[SessionTerm.ABNORMAL] = t('Non applicable for Javascript'), _d[SessionTerm.HEALTHY] = t('No errors were captured during session life-time'), _d[SessionTerm.ERRORED] = t('During the session at least one error occurred that did not bubble up to the global handler. The application loading process did not crash'), _d[SessionTerm.UNHANDLED] = "An error was captured by the global 'onerror' or 'onunhandledrejection' handler", _d));
        case 'apple-ios':
        case 'minidump':
        case 'native':
            return __assign(__assign({}, commonTermsDescription), desktopTermDescriptions);
        case 'rust':
            return __assign(__assign(__assign({}, commonTermsDescription), desktopTermDescriptions), (_e = {}, _e[SessionTerm.CRASHED] = t('The application had an unrecovable error (a panic)'), _e));
        default:
            return __assign(__assign({}, commonTermsDescription), (_f = {}, _f[SessionTerm.CRASHED] = t('Number of users who experienced an unhandled error'), _f[SessionTerm.ABNORMAL] = t('An unknown session exit'), _f[SessionTerm.HEALTHY] = mobileTermsDescription.healthy, _f[SessionTerm.ERRORED] = mobileTermsDescription.errored, _f[SessionTerm.UNHANDLED] = mobileTermsDescription.unhandled, _f));
    }
}
export function getSessionTermDescription(term, platform) {
    return getTermDescriptions(platform)[term];
}
//# sourceMappingURL=sessionTerm.jsx.map