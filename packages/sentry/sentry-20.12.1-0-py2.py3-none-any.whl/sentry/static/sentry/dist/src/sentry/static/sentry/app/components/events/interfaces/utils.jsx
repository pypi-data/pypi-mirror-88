import { __read, __values } from "tslib";
import * as Sentry from '@sentry/react';
import isString from 'lodash/isString';
import * as qs from 'query-string';
import { FILTER_MASK } from 'app/constants';
import { defined } from 'app/utils';
export function escapeQuotes(v) {
    return v.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}
// TODO(dcramer): support cookies
export function getCurlCommand(data) {
    var e_1, _a;
    var _b, _c, _d;
    var result = 'curl';
    if (defined(data.method) && data.method !== 'GET') {
        result += ' \\\n -X ' + data.method;
    }
    // TODO(benvinegar): just gzip? what about deflate?
    var compressed = (_b = data.headers) === null || _b === void 0 ? void 0 : _b.find(function (h) { return h[0] === 'Accept-Encoding' && h[1].indexOf('gzip') !== -1; });
    if (compressed) {
        result += ' \\\n --compressed';
    }
    // sort headers
    var headers = (_d = (_c = data.headers) === null || _c === void 0 ? void 0 : _c.sort(function (a, b) {
        return a[0] === b[0] ? 0 : a[0] < b[0] ? -1 : 1;
    })) !== null && _d !== void 0 ? _d : [];
    try {
        for (var headers_1 = __values(headers), headers_1_1 = headers_1.next(); !headers_1_1.done; headers_1_1 = headers_1.next()) {
            var header = headers_1_1.value;
            result += ' \\\n -H "' + header[0] + ': ' + escapeQuotes(header[1] + '') + '"';
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (headers_1_1 && !headers_1_1.done && (_a = headers_1.return)) _a.call(headers_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    if (defined(data.data)) {
        switch (data.inferredContentType) {
            case 'application/json':
                result += ' \\\n --data "' + escapeQuotes(JSON.stringify(data.data)) + '"';
                break;
            case 'application/x-www-form-urlencoded':
                result +=
                    ' \\\n --data "' +
                        escapeQuotes(qs.stringify(data.data)) +
                        '"';
                break;
            default:
                if (isString(data.data)) {
                    result += ' \\\n --data "' + escapeQuotes(data.data) + '"';
                }
                else if (Object.keys(data.data).length === 0) {
                    // Do nothing with empty object data.
                }
                else {
                    Sentry.withScope(function (scope) {
                        scope.setExtra('data', data);
                        Sentry.captureException(new Error('Unknown event data'));
                    });
                }
        }
    }
    result += ' \\\n "' + getFullUrl(data) + '"';
    return result;
}
export function stringifyQueryList(query) {
    var e_2, _a;
    if (isString(query)) {
        return query;
    }
    var queryObj = {};
    try {
        for (var query_1 = __values(query), query_1_1 = query_1.next(); !query_1_1.done; query_1_1 = query_1.next()) {
            var kv = query_1_1.value;
            if (kv !== null && kv.length === 2) {
                var _b = __read(kv, 2), k = _b[0], v = _b[1];
                if (v !== null) {
                    queryObj[k] = v;
                }
            }
        }
    }
    catch (e_2_1) { e_2 = { error: e_2_1 }; }
    finally {
        try {
            if (query_1_1 && !query_1_1.done && (_a = query_1.return)) _a.call(query_1);
        }
        finally { if (e_2) throw e_2.error; }
    }
    return qs.stringify(queryObj);
}
export function getFullUrl(data) {
    var _a;
    var fullUrl = data === null || data === void 0 ? void 0 : data.url;
    if (!fullUrl) {
        return fullUrl;
    }
    if ((_a = data === null || data === void 0 ? void 0 : data.query) === null || _a === void 0 ? void 0 : _a.length) {
        fullUrl += '?' + stringifyQueryList(data.query);
    }
    if (data.fragment) {
        fullUrl += '#' + data.fragment;
    }
    return fullUrl;
}
/**
 * Converts an object of body/querystring key/value pairs
 * into a tuple of [key, value] pairs, and sorts them.
 *
 * This handles the case for query strings that were decoded like so:
 *
 *   ?foo=bar&foo=baz => { foo: ['bar', 'baz'] }
 *
 * By converting them to [['foo', 'bar'], ['foo', 'baz']]
 */
export function objectToSortedTupleArray(obj) {
    return Object.keys(obj)
        .reduce(function (out, k) {
        var val = obj[k];
        return out.concat(Array.isArray(val)
            ? val.map(function (v) { return [k, v]; }) // key has multiple values (array)
            : [[k, val]] // key has single value
        );
    }, [])
        .sort(function (_a, _b) {
        var _c = __read(_a, 2), keyA = _c[0], valA = _c[1];
        var _d = __read(_b, 2), keyB = _d[0], valB = _d[1];
        // if keys are identical, sort on value
        if (keyA === keyB) {
            return valA < valB ? -1 : 1;
        }
        return keyA < keyB ? -1 : 1;
    });
}
// for context summaries and avatars
export function removeFilterMaskedEntries(rawData) {
    var e_3, _a;
    var cleanedData = {};
    try {
        for (var _b = __values(Object.getOwnPropertyNames(rawData)), _c = _b.next(); !_c.done; _c = _b.next()) {
            var key = _c.value;
            if (rawData[key] !== FILTER_MASK) {
                cleanedData[key] = rawData[key];
            }
        }
    }
    catch (e_3_1) { e_3 = { error: e_3_1 }; }
    finally {
        try {
            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
        }
        finally { if (e_3) throw e_3.error; }
    }
    return cleanedData;
}
export function formatAddress(address, imageAddressLength) {
    return "0x" + address.toString(16).padStart(imageAddressLength !== null && imageAddressLength !== void 0 ? imageAddressLength : 0, '0');
}
export function parseAddress(address) {
    if (address === null) {
        return 0;
    }
    try {
        return parseInt(address, 16) || 0;
    }
    catch (_e) {
        return 0;
    }
}
export function getImageRange(image) {
    // The start address is normalized to a `0x` prefixed hex string. The event
    // schema also allows ingesting plain numbers, but this is converted during
    // ingestion.
    var startAddress = parseAddress(image === null || image === void 0 ? void 0 : image.image_addr);
    // The image size is normalized to a regular number. However, it can also be
    // `null`, in which case we assume that it counts up to the next image.
    var endAddress = startAddress + ((image === null || image === void 0 ? void 0 : image.image_size) || 0);
    return [startAddress, endAddress];
}
export function parseAssembly(assembly) {
    var name;
    var version;
    var culture;
    var publicKeyToken;
    var pieces = assembly ? assembly.split(',') : [];
    if (pieces.length === 4) {
        name = pieces[0];
        version = pieces[1].split('Version=')[1];
        culture = pieces[2].split('Culture=')[1];
        publicKeyToken = pieces[3].split('PublicKeyToken=')[1];
    }
    return { name: name, version: version, culture: culture, publicKeyToken: publicKeyToken };
}
//# sourceMappingURL=utils.jsx.map