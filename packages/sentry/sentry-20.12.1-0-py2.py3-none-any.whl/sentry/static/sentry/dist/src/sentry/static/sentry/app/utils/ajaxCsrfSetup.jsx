import { CSRF_COOKIE_NAME } from 'app/constants';
import getCookie from 'app/utils/getCookie';
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method !== null && method !== void 0 ? method : '');
}
export default function ajaxCsrfSetup(xhr, settings) {
    var _a;
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', (_a = getCookie(CSRF_COOKIE_NAME)) !== null && _a !== void 0 ? _a : '');
    }
}
//# sourceMappingURL=ajaxCsrfSetup.jsx.map