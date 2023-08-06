import { t } from 'app/locale';
export var EMPTY_DASHBOARD = {
    id: '',
    dateCreated: '',
    createdBy: '',
    title: t('Untitled dashboard'),
    widgets: [],
};
export var DISPLAY_TYPE_CHOICES = [
    { label: t('Area chart'), value: 'area' },
    { label: t('Bar chart'), value: 'bar' },
    { label: t('Line chart'), value: 'line' },
];
export var INTERVAL_CHOICES = [
    { label: t('1 Minute'), value: '1m' },
    { label: t('5 Minutes'), value: '5m' },
    { label: t('15 Minutes'), value: '15m' },
    { label: t('30 Minutes'), value: '30m' },
    { label: t('1 Hour'), value: '1h' },
    { label: t('1 Day'), value: '1d' },
];
//# sourceMappingURL=data.jsx.map