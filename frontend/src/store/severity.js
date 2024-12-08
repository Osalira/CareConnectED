// store/severity.js
import { defineStore } from 'pinia';

export const useSeverityStore = defineStore('severity', {
  state: () => ({
    severity: '',
  }),
  actions: {
    setSeverity(value) {
      this.severity = value;
    },
  },
});
