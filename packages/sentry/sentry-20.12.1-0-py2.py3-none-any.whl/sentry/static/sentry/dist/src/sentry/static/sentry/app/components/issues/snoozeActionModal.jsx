var _this = this;
import React from 'react';
import { t } from 'app/locale';
var SnoozeTimes;
(function (SnoozeTimes) {
    // all values in minutes
    SnoozeTimes[SnoozeTimes["THIRTY_MINUTES"] = 30] = "THIRTY_MINUTES";
    SnoozeTimes[SnoozeTimes["TWO_HOURS"] = 120] = "TWO_HOURS";
    SnoozeTimes[SnoozeTimes["TWENTY_FOUR_HOURS"] = 1440] = "TWENTY_FOUR_HOURS";
})(SnoozeTimes || (SnoozeTimes = {}));
var SnoozeActionModal = function (_a) {
    var Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal, onSnooze = _a.onSnooze;
    var handleSnooze = function (duration) {
        onSnooze(duration);
        closeModal();
    };
    return (<React.Fragment>
      <Body>
        <h5>{t('How long should we ignore this issue?')}</h5>
        <ul className="nav nav-stacked nav-pills">
          <li>
            <a onClick={handleSnooze.bind(_this, SnoozeTimes.THIRTY_MINUTES)}>
              {t('30 minutes')}
            </a>
          </li>
          <li>
            <a onClick={handleSnooze.bind(_this, SnoozeTimes.TWO_HOURS)}>{t('2 hours')}</a>
          </li>
          <li>
            <a onClick={handleSnooze.bind(_this, SnoozeTimes.TWENTY_FOUR_HOURS)}>
              {t('24 hours')}
            </a>
          </li>
          
          <li>
            <a onClick={handleSnooze.bind(_this, undefined)}>{t('Forever')}</a>
          </li>
        </ul>
      </Body>
      <Footer>
        <button type="button" className="btn btn-default" onClick={closeModal}>
          {t('Cancel')}
        </button>
      </Footer>
    </React.Fragment>);
};
export default SnoozeActionModal;
//# sourceMappingURL=snoozeActionModal.jsx.map