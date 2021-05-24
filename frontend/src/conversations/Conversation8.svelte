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
    "userA1": "I can’t be the only one who rates Karius over Adrian?",
    "userB1": "Lol what rubbish ! Yes I think you’re the only one mate.",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: As Liverpool Football Club announced their intention to terminate their contract with player Loris Karius, who is replaced by a different player, Adrián. User A discusses his view that he liked the play of Karius better, while User B disagrees in a very typical British English Dialect that is filtered as potentially toxic:</h2>

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


