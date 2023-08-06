import { __read, __spread } from "tslib";
import React from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getRuntimeKnownData from './getRuntimeKnownData';
import { RuntimeIgnoredDataType, RuntimeKnownDataType } from './types';
var runtimeKnownDataValues = [RuntimeKnownDataType.NAME, RuntimeKnownDataType.VERSION];
var runtimeIgnoredDataValues = [RuntimeIgnoredDataType.BUILD];
var Runtime = function (_a) {
    var data = _a.data;
    return (<React.Fragment>
      <ContextBlock data={getRuntimeKnownData(data, runtimeKnownDataValues)}/>
      <ContextBlock data={getUnknownData(data, __spread(runtimeKnownDataValues, runtimeIgnoredDataValues))}/>
    </React.Fragment>);
};
export default Runtime;
//# sourceMappingURL=runtime.jsx.map