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
    "userA": "HELLO HOW DO I GET SOMEBODY TO FIX SHIT AROUND HERE?",
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: In the process of using the website there are a myriad of technical malfunctions preventing you from doing important work, for which you may have a time constraint and as a result may post in a support thread:

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
