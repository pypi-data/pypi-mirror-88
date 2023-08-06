/**
 * For all routes with a `path`, find the first route without a route param (e.g. :apiKey)
 *
 * @param routes A list of react-router route objects
 * @param route If given, will only take into account routes between `route` and end of the routes list
 * @return Object Returns a react-router route object
 */
export default function findFirstRouteWithoutRouteParam(routes, route) {
    var routeIndex = route !== undefined ? routes.indexOf(route) : -1;
    var routesToSearch = route && routeIndex > -1 ? routes.slice(routeIndex) : routes;
    return (routesToSearch.filter(function (_a) {
        var path = _a.path;
        return !!path;
    }).find(function (_a) {
        var path = _a.path;
        return !(path === null || path === void 0 ? void 0 : path.includes(':'));
    }) ||
        route);
}
//# sourceMappingURL=findFirstRouteWithoutRouteParam.jsx.map