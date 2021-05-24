<script>
  export let editorId;
  const copyText = (text) => {
    const r = document.getElementById(editorId);
    const event = document.createEvent("HTMLEvents");
    r.innerText = text;
    event.initEvent("input", true, true);
    event.eventName = "input";
    r.dispatchEvent(event);
  }

  const selectedText = {
    "userA": "Would you both shut up, you don't run wikipedia, especially a stupid kid.",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: The following prompts are real wikipedia editor forum comments, we wish to understand user editing of toxic language in online comments, and so please edit these comments to be less toxic, as if you were the author attempting to maintain the original intention as best as possible. 
Consider you are an experienced editor on wikipedia, and two new users are attempting to change some edits you have made that you know are correct, however they persist. You are exhausted and lash out, perhaps as this real reply:
</h2>

<article class="media">
  <figure class="media-left">
    <p class="image is-64x64">
      <img src="https://bulma.io/images/placeholders/128x128.png">
    </p>
  </figure>
  <div class="media-content" style="background: lightyellow">
    <div class="content">
      <p>
        <strong>User A</strong>
        <br>
        {selectedText["userA"]}
        <br>
        <small><a on:click={() => {copyText(selectedText["userA"])}}>Load into RECAST</a> · 3 hrs</small>
      </p>
    </div> 
  </div>
</article>
