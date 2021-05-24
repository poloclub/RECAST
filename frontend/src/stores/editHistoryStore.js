import { writable } from 'svelte/store';

const editHistoryStore = writable({
  original: 0,
  history: [],
  hoveredToken: null,
  selectedTokens: [],
  selectedOutput: 0,
  currentTokens: [],
  currentData: []
});

export default editHistoryStore;