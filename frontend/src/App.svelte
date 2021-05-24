<script>
  import ToxicScore from './components/ToxicScore.svelte';
  import {analyzedTextResponse, highlightedTextResponse} from './stores/appStore.js'
  import editHistoryStore from './stores/editHistoryStore.js'
  import Conversation1 from './conversations/Conversation1.svelte'
  import Conversation2 from './conversations/Conversation2.svelte'
  import Conversation3 from './conversations/Conversation3.svelte'
  import Conversation4 from './conversations/Conversation4.svelte'
  import Conversation5 from './conversations/Conversation5.svelte'
  import Conversation6 from './conversations/Conversation6.svelte'
  import Conversation7 from './conversations/Conversation7.svelte'
  import Conversation8 from './conversations/Conversation8.svelte'
  import Conversation9 from './conversations/Conversation9.svelte'

  import InputHighlighter from './components/InputHighlighter.svelte';
  import FlaggingInput from './components/FlaggingInput.svelte';

  import surveyStore from './stores/surveyStore.js'
  import { onMount } from 'svelte';

  var loadTexts = [

    "Would you both shut up, you don't run wikipedia, especially a stupid kid.",
    "Hey why you are spreading misconceptions and trying to spread false information to the people. You not even know who won the battle and who lost. you are the cheapest person on the earth. Bloody ignorant fool. Check sources before spreading rumors.",
    "HELLO HOW DO I GET SOMEBODY TO FIX SHIT AROUND HERE?",
    "It is not redundant. You are redundant.",
    "I know how frustrated you are right now. Stupidity in this place has no limits. Someone with a brain cell or two will eventually show up and clean this mess. Meanwhile hang in there.",
    "I guarantee you didn’t do any research before opening your ignorant trap. But go off girl you definitely doing it",
    "Keep dreaming scumbag.",
    "Lol what rubbish ! Yes I think you’re the only one mate.",
    "Can you get over yourself for five fucking seconds? I'm a fan of your pursuit but you have been a fucking douchebag during this whole pandemic. Go invent something useful, like an actual engine that could get us to Mars in a reasonable amount of time."
  ]

  function randomStr(len, arr) { 
    var ans = ''; 
    for (var i = len; i > 0; i--) { 
      ans +=  
        arr[Math.floor(Math.random() * arr.length)]; 
    } 
    return ans; 
  } 

  var showingInstructions = false

  if (!localStorage.getItem("userToken")) {
    showingInstructions = true
    localStorage.setItem("userToken", randomStr(5, '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
  }

  if (!localStorage.getItem("currentThread")) {
    localStorage.setItem("currentThread", 1)
  }


  var vidEnabledURI = "https://www.youtube.com/" // REMOVED FOR ANONYMINITY
  var vidDisabledURI = "https://www.youtube.com/" // REMOVED FOR ANONYMINITY

  let userToken = localStorage.getItem("userToken")
  var currentThread = localStorage.getItem("currentThread")
  let recastEnabled = currentThread >= 5;
  var url = 'http://localhost:8000';

  fetch(url + '/set_token_type', {
    method: 'POST',
    body: JSON.stringify({
      'uuid': userToken,
      'type': recastEnabled
    }), 
    headers: {
      'Content-Type': 'application/json'
    }
  }, () => {
    console.log("Token SET")
  });

  var totalThread = 8;
  var textEdited = false;
  var showTextEditWarning = false;

  var selectedEditor = "editor"
  if (!recastEnabled) {
    selectedEditor = "dumb-editor"
  }

  const showPrevThread = () => {
    if (currentThread > 1) currentThread--;
  }

  const showNextThread = () => {
    
    const r = document.getElementById(selectedEditor)
    textEdited = r.innerText != "" && !loadTexts.includes(r.innerText)

    if (!textEdited) {
      showTextEditWarning = true;
      return;
    }
    
    showTextEditWarning = false;

    if (currentThread <= totalThread) currentThread++;
    localStorage.setItem("currentThread", currentThread)
    if (currentThread == totalThread + 1) {
      showingFinalAlert = true;
    }

    recastEnabled = currentThread >= 5;
    if (currentThread == 5) {
      selectedEditor = 'editor'
      showingInstructions = true
      // attachEditorChange(selectedEditor)
    }

    // wipe editor
    const event = document.createEvent("HTMLEvents");

    fetch(url + '/submit', {
      method: 'POST',
      body: JSON.stringify({
        'uuid': userToken,
        'submission': r.innerText
      }), 
      headers: {
        'Content-Type': 'application/json'
      }
    }, () => {
      console.log("submitting")
    });

    r.innerText = "";
    event.initEvent("input", true, true);
    event.eventName = "input";
    r.dispatchEvent(event);

  }

  const hideFinalAlert = () => {
    showingFinalAlert = false;
  }

  const setInstructionalAlert = (status) => {
    showingInstructions = status
  }

  var showingFinalAlert = false;
  if (currentThread == totalThread + 1) {
    showingFinalAlert = true;
  }

</script>


<style>
  .embed-container { 
    position: relative; 
    padding-bottom: 56.25%; 
    height: 0; 
    overflow: hidden; 
    max-width: 100%; 
  } 
  .embed-container iframe, .embed-container object, .embed-container embed { 
    position: absolute; 
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%;
  }
</style>

{#if showingInstructions}
  <div id="instructionPopover" style=
    "top: 10%; 
    left: 25%; 
    width: 50%; 
    position: fixed; 
    z-index: 99999;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    " 
    class="popover is-popover-bottom">
    <article class="message">
      <div class="message-header">
        <p>Instructional Video</p>
        <button class="delete" on:click={() => {setInstructionalAlert(false)}} aria-label="delete"></button>
      </div>
      <div style="text-align:center" class="message-body">
        {#if recastEnabled}
        <div class='embed-container'><iframe src={vidEnabledURI} frameborder='0' allowfullscreen></iframe></div>
        {:else}
        <div class='embed-container'><iframe src={vidDisabledURI} frameborder='0' allowfullscreen></iframe></div>
        {/if}
      </div>
    </article>
  </div>
{/if}

{ #if showingFinalAlert }
  <div id="" style=
    "top: 30%; 
    left: 25%; 
    width: 50%; 
    position: fixed; 
    z-index: 99999;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    " 
    class="popover is-popover-bottom">
    <article class="message is-success">
      <div class="message-header">
        <p>Thank you!</p>
        <button class="delete" on:click={() => {hideFinalAlert()}} aria-label="delete"></button>
      </div>
      <div class="message-body">
        Thank you for completing this study! Copy this token: <span style="background-color: #fffd73;">{userToken}</span>, and paste it into the survey.    </div>
    </article>
  </div>
{ /if }


<div class="columns">

  <div class="column is-one-half" style="height:90vh; width: 50%; position: sticky; top: 3.2rem;">
    <div style="padding:5%;">

      {#if recastEnabled}
        {#if showTextEditWarning}
        <label style="color:red; padding-bottom: 5%;">Please make sure you edit the comment submission!</label>
        {/if}
        <div style="padding-left: 2%; padding-right: 2%" class="columns">
          <div style="padding: 0px; text-align: right;" class="column">
            <h5 style="margin-bottom: 1%" class="subtitle is-5">Current toxicity score: 
              {Math.round($analyzedTextResponse["mainInputResults"]["sigmoidOutput"][0]["value"] * 100)}%</h5>
            <progress class="progress" style="margin-bottom:1%" value="{Math.round($analyzedTextResponse["mainInputResults"]["sigmoidOutput"][0]["value"] * 100)}" max="100">
            </progress>
            { #if $highlightedTextResponse.textSelected }
            <h5 style="margin-bottom: 1%" class="subtitle is-5">Selected toxicity score: 
              {Math.round($highlightedTextResponse["originalToxicity"][0] * 100)}%</h5>
            <progress class="progress" style="margin-bottom:1%" value="{Math.round($highlightedTextResponse["originalToxicity"][0] * 100)}" max="100">
            </progress>
            {:else}
            <h5 style="margin-bottom: 1%" class="subtitle is-5">Selected toxicity score: 0%</h5>
            <progress class="progress" style="margin-bottom:1%" value="{0}" max="100">
            </progress>
            { /if }
          </div>
        </div>
        <div style="padding: 0px" class="column">
          <h5 style="margin-bottom: 1%" class="subtitle is-5">Enter some text...</h5>
        </div>
        <div class="columns">
          <div style="width: 50%" class="column">
            <InputHighlighter uuid={userToken} />
          </div>
        </div>
        <button on:click={showNextThread} class="button">Submit</button>

      {:else}

        <div style="padding-top:30%" class="control is-large">
          {#if showTextEditWarning}
          <label style="color:red">Please make sure you edit the comment submission!</label>
          {/if}
          <div id="dumb-editor" class="textarea is-large" spellcheck="false" contenteditable="true" style="overflow:auto" />
        </div>
        <button on:click={showNextThread} class="button">Submit</button>
      { /if }
    </div>

  </div>

  <div class="column">
    <div style="padding-top: 10%; padding-left: 10%; padding-right: 10%; padding-bottom: 5%">
      <h2 class="subtitle is-2">RECAST</h2>
      <button on:click={() => {setInstructionalAlert(true)}} class="button">Show Instructions</button>

      <hr />

      {#if currentThread < totalThread + 1}
        <p style="font-size: 1rem; margin-bottom: 5px">Looking at thread: {currentThread}/{totalThread}</p>
      {/if}

      {#if currentThread == 1}
        <Conversation5 editorId={selectedEditor}/>
      {:else if currentThread == 2}
        <Conversation6 editorId={selectedEditor}/>
      {:else if currentThread == 3}
        <Conversation7 editorId={selectedEditor}/>
      {:else if currentThread == 4}
        <Conversation8 editorId={selectedEditor}/>
      {:else if currentThread == 5}
        <Conversation1 editorId={selectedEditor}/>
      {:else if currentThread == 6}
        <Conversation2 editorId={selectedEditor}/>
      {:else if currentThread == 7}
        <Conversation3 editorId={selectedEditor}/>
      {:else if currentThread == 8}
        <Conversation4 editorId={selectedEditor}/>
      {:else if currentThread == totalThread + 1}
        <p style="font-size: 1.5rem; margin-bottom: 20px">Thank you for completing this study! 
        Copy this token: <span style="background-color: #fffd73;">{userToken}</span>, and paste it into the survey.</p>
      {/if}

      <hr />

      {#if recastEnabled }

        <p style="font-size: 1.5rem; margin-bottom: 20px">Recast is an interactive writing tool designed to help reduce toxicity in language.
        Use the textbox on the left to write comment. You'll notice that RECAST 
        <span style="border-bottom: 4px solid; border-bottom-color: rgba(255, 0, 110, .8);">underlines</span> words
        that cause it to predict a toxic outcome. Recast also captions your comment, 
        <span style="background-color: #fffd73;">highlighting</span> specific words it finds alternatives for.</p> 

        <p style="font-size: 1.5rem; margin-bottom: 20px">To start, try loading a comment from the discussion thread(s) below!</p>

        <p style="font-size: 1.5rem; margin-top: 20px; margin-bottom: 20px">Recast also allows you to explore local toxicity, because sometimes, editing a single word in your input won't make a dent in the overall toxicity. 
        By selecting a group of words, you can see the toxicity of a subsection of the text! Hovering over the selected words allows you to reduce the toxicity of the entire selection as a whole.</p>

        <p style="font-size: 1.5rem; margin-bottom: 20px">Sometimes, RECAST gets it wrong; if you feel like the suggestions/toxicity score 
        for what you've currently inputted is incorrect, feel free to notify us below!</p> 
        <FlaggingInput /> 
      {/if}
    </div>


  </div>
</div>

