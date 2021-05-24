import { writable } from 'svelte/store';

const promptLinks = ["img1", "img2", "img3", "img4", "img5", "img6", "img7"];
const questions = ["This tool helped me make this argument less toxic.", "question2?", "question3?", "question4?"]
let options = [
  'Strongly Disagree',
  'Disagree',
  'Undecided',
  'Agree',
  'Strongly Agree'
]

// generate initial store state.
let results = {}
for (var promptIdx in promptLinks) {
  var prompt = promptLinks[promptIdx];
  results[prompt] = {}
  for (var questionIdx in questions) {
    var question = questions[questionIdx];
    results[prompt][question] = options[2] // midpoint.
  }
}

// add a bunch of helper vars to the store -- questions can potentially change mid-study with this pattern.
results.totalImages = promptLinks.length;
results.currentImage = 0;
results.promptLinks = promptLinks;
results.questions = questions;
results.options = options;

const surveyResults = writable(results);

export default surveyResults;