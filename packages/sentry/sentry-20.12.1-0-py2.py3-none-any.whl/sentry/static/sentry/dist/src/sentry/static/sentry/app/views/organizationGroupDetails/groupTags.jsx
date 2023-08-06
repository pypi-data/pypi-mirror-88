import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import Alert from 'app/components/alert';
import Count from 'app/components/count';
import DeviceName from 'app/components/deviceName';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import Version from 'app/components/version';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { percent } from 'app/utils';
import withApi from 'app/utils/withApi';
var GroupTags = /** @class */ (function (_super) {
    __extends(GroupTags, _super);
    function GroupTags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            tagList: null,
            loading: true,
            error: false,
        };
        _this.fetchData = function () {
            var _a = _this.props, api = _a.api, group = _a.group, environments = _a.environments;
            _this.setState({
                loading: true,
                error: false,
            });
            api.request("/issues/" + group.id + "/tags/", {
                query: { environment: environments },
                success: function (data) {
                    _this.setState({
                        tagList: data,
                        error: false,
                        loading: false,
                    });
                },
                error: function () {
                    _this.setState({
                        error: true,
                        loading: false,
                    });
                },
            });
        };
        return _this;
    }
    GroupTags.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupTags.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.environments, this.props.environments)) {
            this.fetchData();
        }
    };
    GroupTags.prototype.getTagsDocsUrl = function () {
        return 'https://docs.sentry.io/enriching-error-data/additional-data/';
    };
    GroupTags.prototype.render = function () {
        var baseUrl = this.props.baseUrl;
        var children = [];
        if (this.state.loading) {
            return <LoadingIndicator />;
        }
        else if (this.state.error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        if (this.state.tagList) {
            children = this.state.tagList.map(function (tag, tagIdx) {
                var valueChildren = tag.topValues.map(function (tagValue, tagValueIdx) {
                    var label = null;
                    var pct = percent(tagValue.count, tag.totalValues);
                    var query = tagValue.query || tag.key + ":\"" + tagValue.value + "\"";
                    switch (tag.key) {
                        case 'release':
                            label = <Version version={tagValue.name} anchor={false}/>;
                            break;
                        default:
                            label = <DeviceName value={tagValue.name}/>;
                    }
                    return (<li key={tagValueIdx} data-test-id={tag.key}>
              <GlobalSelectionLink className="tag-bar" to={{
                        pathname: baseUrl + "events/",
                        query: { query: query },
                    }}>
                <span className="tag-bar-background" style={{ width: pct + '%' }}/>
                <span className="tag-bar-label">{label}</span>
                <span className="tag-bar-count">
                  <Count value={tagValue.count}/>
                </span>
              </GlobalSelectionLink>
            </li>);
                });
                return (<TagItem key={tagIdx}>
            <Panel>
              <PanelHeader hasButtons style={{ textTransform: 'none' }}>
                <div style={{ fontSize: 16 }}>{tag.key}</div>
                <DetailsLinkWrapper>
                  <GlobalSelectionLink className="btn btn-default btn-sm" to={baseUrl + "tags/" + tag.key + "/"}>
                    {t('More Details')}
                  </GlobalSelectionLink>
                </DetailsLinkWrapper>
              </PanelHeader>
              <PanelBody withPadding>
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                  {valueChildren}
                </ul>
              </PanelBody>
            </Panel>
          </TagItem>);
            });
        }
        return (<div>
        <Container>{children}</Container>
        <Alert type="info">
          {tct('Tags are automatically indexed for searching and breakdown charts. Learn how to [link: add custom tags to issues]', {
            link: <a href={this.getTagsDocsUrl()}/>,
        })}
        </Alert>
      </div>);
    };
    return GroupTags;
}(React.Component));
var DetailsLinkWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var TagItem = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 0 ", ";\n  width: 50%;\n"], ["\n  padding: 0 ", ";\n  width: 50%;\n"])), space(1));
export default withApi(GroupTags);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=groupTags.jsx.map