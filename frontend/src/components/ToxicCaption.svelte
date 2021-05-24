<script>
import {analyzedTextResponse} from '../stores/appStore.js'
export let alts; 

</script>

<style>
  p {
    margin-top: 10px;
    color: gray;
    font-style: italic;
  }
</style>

<p>
  {#if $analyzedTextResponse["mainInputResults"]["sigmoidOutput"][0]["value"] < .5}
    {"Our model tells us this is a non-toxic sentence!"}
  {:else if Object.keys($analyzedTextResponse["alternatives"]).length == 0}
    {"Sorry. We can't find any alternative words to improve the toxicity score of this sentence."}
  {:else}
    {"Try hovering over, or dragging and selecting, the word(s): "}
      {#each Object.keys($analyzedTextResponse["alternatives"]) as key}
        {#if alts[key] != undefined}
          <br/><span style="background-color: #fffd73;"><b>{alts[key] + " "}</b></span>
        {/if}
      {/each}
  {/if}
</p>