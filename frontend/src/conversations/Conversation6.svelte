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
    "userA1": "Why did it take too long to arrest two culprits? Cuz they are white and the victim is black and this is America. So yea ... so infuriated",
    "userB1": "It’s actually because of the Georgia laws but go on with your fake outcry.",
    "userA2": '"gEoRgiA LaWs" ...as if 2 black men would get away with murdering a white man thats minding his business. There was clearly no Stand Your Ground defense. Outright execution',
    "userB2": 'I guarantee you didn’t do any research before opening your ignorant trap. But go off girl you definitely doing it'
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: The following prompts are real twitter replies that had been marked as potentially toxic by the twitter platform. We wish to understand user editing of toxic language in online comments, and so please edit these comments to be less toxic, as if you were the author attempting to maintain the original intention as best as possible. 
In this thread discussing the fatal shooting of Ahmaud Arbery, and the delay in finding suspects. User A suggests racial bias while User B disagrees, in this thread the final reply was filtered as toxic and so please edit it from the perspective of User B.

</h2>

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
  <div class="media-content">
    <div class="content">
      <p>
        <strong>User B</strong>
        <br>
        {selectedText["userB1"]}
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
  <div class="media-content">
    <div class="content">
      <p>
        <strong>User A</strong>
        <br>
        {selectedText["userA2"]}
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
        {selectedText["userB2"]}
        <br>
        <small><a on:click={() => {copyText(selectedText["userB2"])}}>Load into RECAST</a> · 3 hrs</small>
      </p>
    </div> 
  </div>
</article>
