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
    "userA": "It is not redundant. You are redundant.",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: While editing a piece of minutiae on a highly visited page, there is a spirited debate on whether to include an additional sentence which may be seen as redundant to some in explaining the overall point but to you seems necessary, however every time you add this sentence another user removes it, in the discussion thread in reply to this user you may post:

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
