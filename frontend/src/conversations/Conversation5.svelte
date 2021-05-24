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
    "userA": "I know how frustrated you are right now. Stupidity in this place has no limits. Someone with a brain cell or two will eventually show up and clean this mess. Meanwhile hang in there.",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: Finally in a thread with a fellow editor, who is having similar difficulties as you, you attempt to commiserate with the post:

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
