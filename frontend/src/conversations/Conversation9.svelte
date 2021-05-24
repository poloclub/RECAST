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
    "musk1": "Elon Musk, billionaire CEO of electric car company Tesla is suing the county where a Tesla factory is located due to local COVID-19 restrictions preventing the factory reopening. User A is supportive of this move, while User B is critical of it and their response is filtered.",
    "userA1": "Anything we can do to help? Does reaching out to politicians help in any way?",
    "musk2": "Yes",
    "userB1": "Can you get over yourself for five fucking seconds? I'm a fan of your pursuit but you have been a fucking douchebag during this whole pandemic. Go invent something useful, like an actual engine that could get us to Mars in a reasonable amount of time."
  }

</script>

<h2 style="margin-top: 20px" class="subtitle is-6">CONTEXT: Elon Musk, billionaire CEO of electric car company Tesla is suing the county where a Tesla factory is located due to local COVID-19 restrictions preventing the factory reopening. User A is supportive of this move, while User B is critical of it and their response is filtered.
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
        <strong>Elon Musk</strong>
        <br>
        {selectedText["musk1"]}
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
        <strong>Elon Musk</strong>
        <br>
        {selectedText["musk2"]}
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
