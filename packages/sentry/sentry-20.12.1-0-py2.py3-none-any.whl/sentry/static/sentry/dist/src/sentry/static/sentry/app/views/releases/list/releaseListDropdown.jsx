import { __read } from "tslib";
import React from 'react';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
var ReleaseListDropdown = function (_a) {
    var _b;
    var prefix = _a.label, options = _a.options, selected = _a.selected, onSelect = _a.onSelect, className = _a.className;
    var optionEntries = Object.entries(options);
    var selectedLabel = (_b = optionEntries.find(function (_a) {
        var _b = __read(_a, 2), key = _b[0], _value = _b[1];
        return key === selected;
    })) === null || _b === void 0 ? void 0 : _b[1];
    return (<DropdownControl buttonProps={{ prefix: prefix }} label={selectedLabel} className={className}>
      {optionEntries.map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], label = _b[1];
        return (<DropdownItem key={key} onSelect={onSelect} eventKey={key} isActive={selected === key}>
          {label}
        </DropdownItem>);
    })}
    </DropdownControl>);
};
export default ReleaseListDropdown;
//# sourceMappingURL=releaseListDropdown.jsx.map