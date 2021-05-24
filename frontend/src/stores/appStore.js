import { writable } from "svelte/store";

const analyzedTextResponse = writable({
  mainInputResults: {
    attentionOutput: {},
    sigmoidOutput: [
      { label: "toxic", value: 0.0 },
      { label: "severe_toxic", value: 0.0 },
      { label: "obscene", value: 0.0 },
      { label: "threat", value: 0.0 },
      { label: "insult", value: 0.0 },
      { label: "identity_hate", value: 0.0 },
    ],
  },
  alternatives: [],
});

const highlightedTextResponse = writable({
  alternatives: [],
  originalToxicity: [0],
  textHighlighted: false,
});

export { analyzedTextResponse, highlightedTextResponse };
