import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Link from 'app/components/links/link';
import Panel from 'app/components/panels/panel';
import { IconSentry } from 'app/icons';
import space from 'app/styles/space';
var BODY_CLASSES = ['narrow'];
var Layout = /** @class */ (function (_super) {
    __extends(Layout, _super);
    function Layout() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Layout.prototype.componentDidMount = function () {
        var _a;
        (_a = document.body.classList).add.apply(_a, __spread(BODY_CLASSES));
    };
    Layout.prototype.componentWillUnmount = function () {
        var _a;
        (_a = document.body.classList).remove.apply(_a, __spread(BODY_CLASSES));
    };
    Layout.prototype.render = function () {
        var children = this.props.children;
        return (<div className="app">
        <AuthContainer>
          <div className="pattern-bg"/>
          <AuthPanel>
            <AuthSidebar>
              <SentryButton />
            </AuthSidebar>
            <div>{children}</div>
          </AuthPanel>
        </AuthContainer>
      </div>);
    };
    return Layout;
}(React.Component));
var AuthContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  justify-content: center;\n  padding-top: 5vh;\n"], ["\n  display: flex;\n  align-items: flex-start;\n  justify-content: center;\n  padding-top: 5vh;\n"])));
var AuthPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  min-width: 550px;\n  display: inline-grid;\n  grid-template-columns: 60px 1fr;\n"], ["\n  min-width: 550px;\n  display: inline-grid;\n  grid-template-columns: 60px 1fr;\n"])));
var AuthSidebar = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  padding: ", ";\n  border-radius: ", " 0 0 ", ";\n  margin: -1px;\n  margin-right: 0;\n  background: #564f64;\n  background-image: linear-gradient(\n    -180deg,\n    rgba(52, 44, 62, 0) 0%,\n    rgba(52, 44, 62, 0.5) 100%\n  );\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: flex-start;\n  padding: ", ";\n  border-radius: ", " 0 0 ", ";\n  margin: -1px;\n  margin-right: 0;\n  background: #564f64;\n  background-image: linear-gradient(\n    -180deg,\n    rgba(52, 44, 62, 0) 0%,\n    rgba(52, 44, 62, 0.5) 100%\n  );\n"])), space(3), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var SentryButton = styled(function (p) { return (<Link to="/" {...p}>
      <IconSentry size="24px"/>
    </Link>); })(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: #fff;\n\n  &:hover,\n  &:focus {\n    color: #fff;\n  }\n"], ["\n  color: #fff;\n\n  &:hover,\n  &:focus {\n    color: #fff;\n  }\n"])));
export default Layout;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=layout.jsx.map