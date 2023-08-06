import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import ProgressBar from 'app/components/progressBar';
describe('ProgressBar', function () {
    it('basic', function () {
        var progressBarValue = 50;
        var wrapper = mountWithTheme(<ProgressBar value={progressBarValue}/>);
        // element exists
        expect(wrapper.length).toEqual(1);
        var elementProperties = wrapper.find('div').props();
        expect(elementProperties).toHaveProperty('role', 'progressbar');
        // check aria attributes
        expect(elementProperties).toHaveProperty('aria-valuenow', progressBarValue);
        expect(elementProperties).toHaveProperty('aria-valuemin', 0);
        expect(elementProperties).toHaveProperty('aria-valuemax', 100);
    });
});
//# sourceMappingURL=progressBar.spec.jsx.map