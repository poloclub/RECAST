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
    "userA1": "2 easy wins against the Eagles",
    "userB1": "Keep dreaming scumbag.",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: After the announcement of the matchups of the NFL regular season for next year, fan of the Dallas Cowboys, User A, talks trash about their rival the Philadeplhia Eagles, when a fan of the Eagles, User B attempts to reply but is filtered:</h2>

<article class="media">
  <figure class="media-left">
    <p class="image is-64x64">
      <img src="https://bulma.io/images/placeholders/128x128.png">
    </p>
  </figure>
  <div class="media-content">
    <div class="content">
      <p>
        <strong>User A</strong>
        <br>
        {selectedText["userA1"]}
        <br>
      </p>
    </div> 
  </div>
</article>
<article class="media">
  <figure class="media-left">
    <p class="image is-64x64">
      <img src="https://bulma.io/images/placeholders/128x128.png">
    </p>
  </figure>
  <div class="media-content" style="background: lightyellow">
    <div class="content">
      <p>
        <strong>User B</strong>
        <br>
        {selectedText["userB1"]}
        <br>
        <small><a on:click={() => {copyText(selectedText["userB1"])}}>Load into RECAST</a> · 3 hrs</small>
      </p>
    </div> 
  </div>
</article>



