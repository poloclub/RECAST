<script>

  import { analyzedTextResponse, highlightedTextResponse } from '../stores/appStore.js'
  import ToxicScore from './ToxicScore.svelte';
  export let loading = false
  export let uuid;
  import ToxicCaption from './ToxicCaption.svelte';
  import editHistoryStore from '../stores/editHistoryStore.js';
  import { onMount } from 'svelte';
  import { getRangeSelectedNodes, nextNode, getToxicity, isDeleteOperation, stylingAttributes } from '../utils.js'

  let intersectionWords = []
  let currTimeout = null;
  let selectionTimeout = null;
  let highlightedIds = [];
  let updateEditor = null;
  let popoverVisible = false;
  let showMultipleToxicity = false;
  let sel, textSegments, textContent, anchorIndex, focusIndex, currentIndex;
  let currentResponse = null;

  // Component Popover Behviour
  window.showPopOver = (ctx, id) => {

    var getTopPostiion = (domRect) => domRect.height + domRect.y
    var getLeftPostiion = (domRect) => (domRect.width / 2 + domRect.x)

    // move off window to hide component
    var avgLeft = -10000
    var avgTop = -10000

    // check if multiple words are included in a highlight -- show the popover between those words.
    if (highlightedIds.includes(id)) { 
      showMultipleToxicity = intersectionWords.length != 0
      var firstElem = document.getElementById('word' + (highlightedIds[0] * 2));
      var lastElem = document.getElementById('word' + (highlightedIds[highlightedIds.length - 1] * 2));
      avgLeft = getLeftPostiion(ctx.getBoundingClientRect())
      avgTop = getTopPostiion(ctx.getBoundingClientRect())
    } else {
      showMultipleToxicity = false
      avgLeft = getLeftPostiion(ctx.getBoundingClientRect())
      avgTop = getTopPostiion(ctx.getBoundingClientRect())
    }

    const domRect = ctx.getBoundingClientRect();
    const d = document.getElementById('alternativePopover');
    if (d.style.visible == true) return;
    $editHistoryStore.hoveredToken = id;

    
    // check if an alternative exists in the text-highlighted range.
    var alternativeInRange = highlightedIds.includes(id) && Object.keys($analyzedTextResponse["alternatives"])
      .map((elem) => +elem) 
      .reduce((curr, next) => curr 
        || (next <= highlightedIds[highlightedIds.length - 1] && next >= highlightedIds[0]), false);

    if ($editHistoryStore.hoveredToken in $analyzedTextResponse["alternatives"] || alternativeInRange) {
      d.style.top = avgTop + 'px'
      d.style.left = avgLeft + 'px'
      d.style.visible = true;
      d.style.opacity = 1;
    }

    popoverVisible = true;

    d.onmouseleave = function() { 
      hidePopOver();
    }
  }

  window.hidePopOver = (event) => {
    const d = document.getElementById('alternativePopover');
    
    // Initial call -> ignore this function
    popoverVisible = false;

    if (!event) {
      d.style.top = '-10000px';
      d.style.left = '-100000px';
      d.style.visible = false;
      d.style.opacity = 0;
      $editHistoryStore.hoveredToken = null;
      return;
    }


    let ctx = event.fromElement;
    // Get the mouse position
    let mouseX = event.clientX
    let mouseY = event.clientY
    
    // Get the range of the popup box
    const d_content = d.childNodes[0]
    let top = parseFloat(d.style.top) - 10
    let left = d_content.offsetLeft
    let right = d_content.offsetRight
    // Mouseout upward
    if (mouseY < top) {
      d.style.top = '-10000px';
      d.style.left = '-100000px';
      d.style.visible = false;
      d.style.opacity = 0;
      $editHistoryStore.hoveredToken = null;

    } else if ((mouseX < left) || (mouseX > right)) {
      d.style.top = '-10000px';
      d.style.left = '-100000px';
      d.style.visible = false;
      d.style.opacity = 0;
      $editHistoryStore.hoveredToken = null;
    }
  }



  onMount(async () => {

    document.addEventListener("selectionchange", event => {
      checkEditorSelection();
    })

    window.hidePopOver();
    const editor = document.getElementById('editor');
    const selectionOutput = document.getElementById('selection');

    function getTextSegments(element) {
      const textSegments = [];
      Array.from(element.childNodes).forEach((node) => {
        switch (node.nodeType) {
          case Node.TEXT_NODE:
            textSegments.push({
              text: node.nodeValue,
              node
            });
            break;

          case Node.ELEMENT_NODE:
            textSegments.splice(textSegments.length, 0, ...(getTextSegments(node)));
            break;

          default:
            throw new Error(`Unexpected node type: ${node.nodeType}`);
        }
      });
      return textSegments;
    }

    function checkEditorSelection() {
      var selectedNodes = []
      sel = window.getSelection();
      if (!sel.isCollapsed) {
        selectedNodes = getRangeSelectedNodes(sel.getRangeAt(0))
          .filter((curr) => curr.nodeName == "#text" && curr.data.trim().length != 0)
      } 

      highlightedIds = selectedNodes.map((node) => +(node.parentNode.id.substring(4) / 2)) // 4 because "word" is length 4.
      var alternativeIds = Object.keys($analyzedTextResponse["alternatives"]).map((elem) => +elem)
      intersectionWords = highlightedIds.filter(value => alternativeIds.includes(value))

      if (selectedNodes.length != 0) {

        var highlightedText = selectedNodes
          .reduce((curr, elem) => {return curr + " " + elem.data}, "")
          .substring(1)
        
        clearTimeout(selectionTimeout);
        showMultipleToxicity = true
        loading = true
        selectionTimeout = setTimeout(() => {
          var precomputedAlternatives = {}
          if (intersectionWords.length) {
            var offsetIdx = highlightedIds[0]
            intersectionWords.forEach((intersectionIndex) => {
              precomputedAlternatives[intersectionIndex - offsetIdx] = 
                $analyzedTextResponse.alternatives[intersectionIndex].map((elem) =>  elem[0])
            })
          }
          loading = true
          getToxicity([highlightedText, precomputedAlternatives], true, uuid).then((response) => {
            highlightedTextResponse.set(response)
            loading = false
            $highlightedTextResponse.textSelected = true
          });
        }, 750)
      } else {
        $highlightedTextResponse.textSelected = false
      }

    }

    updateEditor = (overrideSegments, alternatives, idxs) => {

      sel = window.getSelection();
      textSegments = getTextSegments(editor);

      if (!overrideSegments) {
        textContent = textSegments.map(({
          text
        }) => text).join('');
      } else {
        textContent = textSegments.map(({
          text
        }) => text).join('');
        let splitText = textContent.trim().split(/\s+/)
        for (var i = 0; i < alternatives.length; i++) {
          splitText[idxs[i]] = alternatives[i];
        }

        window.hidePopOver(false) // forcibly close the popover.
        textContent = splitText.join(" ");
      }

      anchorIndex = null;
      focusIndex = null;
      currentIndex = 0;

      textSegments.forEach(({
        text,
        node
      }) => {
        if (node === sel.anchorNode) {
          anchorIndex = currentIndex + sel.anchorOffset;
        }
        if (node === sel.focusNode) {
          focusIndex = currentIndex + sel.focusOffset;
        }
        currentIndex += text.length;
      });

      loading = true
      // editing prevents the timeout from running and sets a new one.
      clearTimeout(currTimeout);

      currTimeout = setTimeout(() => {
        loading = false
        getToxicity(textContent, false, uuid).then((response) => {
          
          $editHistoryStore.selectedOutput = response["mainInputResults"]["sigmoidOutput"][0]["value"]
          if ($editHistoryStore.history.length == 0) {
            $editHistoryStore.original = response["mainInputResults"]["sigmoidOutput"][0]["value"] * 100
          }
          currentResponse = response;
          analyzedTextResponse.set(response);
          textSegments = getTextSegments(editor);
          textContent = textSegments.map(({
            text
          }) => text).join('');
          editor.innerHTML = renderText(textContent);
          restoreSelection(anchorIndex, focusIndex, textContent.length);
          loading = false;
        });

        editor.innerHTML = renderText(textContent);
        restoreSelection(anchorIndex, focusIndex, textContent.length);

      }, 750)
      

    }

    function restoreSelection(absoluteAnchorIndex, absoluteFocusIndex, originalLength) {

      absoluteAnchorIndex = absoluteAnchorIndex > originalLength ? originalLength : absoluteAnchorIndex;
      absoluteFocusIndex = absoluteFocusIndex > originalLength ? originalLength : absoluteFocusIndex;

      const sel = window.getSelection();
      const textSegments = getTextSegments(editor);
      let anchorNode = editor;
      let anchorIndex = 0;
      let focusNode = editor;
      let focusIndex = 0;
      let currentIndex = 0;
      textSegments.forEach(({
        text,
        node
      }) => {
        const startIndexOfNode = currentIndex;
        const endIndexOfNode = startIndexOfNode + text.length;
        if (startIndexOfNode <= absoluteAnchorIndex && absoluteAnchorIndex <= endIndexOfNode) {
          anchorNode = node;
          anchorIndex = absoluteAnchorIndex - startIndexOfNode;
        }
        if (startIndexOfNode <= absoluteFocusIndex && absoluteFocusIndex <= endIndexOfNode) {
          focusNode = node;
          focusIndex = absoluteFocusIndex - startIndexOfNode;
        }
        currentIndex += text.length;
      });

      sel.setBaseAndExtent(anchorNode, anchorIndex, focusNode, focusIndex);
    }

    function renderText(text) {
      const textAttention = $analyzedTextResponse["mainInputResults"]["attentionOutput"];
      const words = text.split(/(\s+)/);
      let attentionIndex = 0;
      let originalWords = []

      let highlightedWords = new Set();
      var historyEmpty = $editHistoryStore.history.length == 0;

      if (!historyEmpty) {
        highlightedWords = 
          $editHistoryStore.history[$editHistoryStore.history.length - 1]["editIdx"]
      }

      const output = words.map((word, id) => {
        if (word.trim().length == 0) return word; // skip over blank/empty text spaces.
        originalWords.push(word)
        // if 
        
        const backgroundColor = $analyzedTextResponse["alternatives"][id / 2] ? 
          "background-color: #fffd73; color: black; background-clip: padding-box;" : "";

        return `<span onmouseenter="showPopOver(this, ${attentionIndex})" onmouseleave=hidePopOver(event)
        id="word${id}" class="text-span" style="${stylingAttributes(textAttention[attentionIndex++])} ${backgroundColor}">${word}</span>`
      })

      $editHistoryStore.currentTokens = originalWords
      return output.join('');
    }

    editor.addEventListener('input', () => {updateEditor();});
    updateEditor();
  });

  function handleAlternativeClick(alternative, idx) {
  
    var historyEmpty = $editHistoryStore.history.length == 0;
    var edits = new Set();
    
    if (!historyEmpty) {
      // shallow clone old set
      edits = new Set($editHistoryStore.history[$editHistoryStore.history.length - 1]["editIdx"]) 
    }

    $editHistoryStore.history.push(
      {
        "alternatives": $editHistoryStore.currentData, 
        "selected": alternative, 
        "currentTokens": $editHistoryStore.currentTokens,
        "editIdx": edits
      }
    )
    updateEditor(true, alternative, idx)
  }


  function enterAlternative(alternativeScore) {
    $editHistoryStore.selectedOutput = alternativeScore
  }

  function leaveMain() {
    $editHistoryStore.selectedOutput = currentResponse["mainInputResults"]["sigmoidOutput"][0]["value"]
  }

</script>

<style>
tr { 
  vertical-align: middle;
}

td { 
  vertical-align: middle;
}


tbody { 
  font-size: 20px;
}

.clickable { 
  cursor: pointer;
}

.clickable:hover { 
  background:rgba(0,0,0,0.3);
}

[contentEditable=true]:empty:not(:focus):before{
  content:attr(data-ph)
}
</style>

<div class="control is-large {loading ? 'is-loading' : ''}">
  <div id="editor" data-ph="Enter some text..." class="textarea is-large" spellcheck="false" contenteditable="true" style="overflow:auto" />
</div>
<ToxicCaption alts={$editHistoryStore.currentTokens}/>
<div id="alternativePopover" style="position: fixed; z-index: 99999" class="popover is-popover-bottom">
  <div style="overflow: auto; max-height: 500px;" class="popover-content">
    { #if loading }
      <p>loading...</p>
    { :else }
      <table class="table">
        <thead>
          <tr>
            <th>Original</th>
            <th style="width: 150%">{showMultipleToxicity ? "Local Toxicity" : "Toxicity"}</th>
          </tr>
        </thead>
        <tbody>
          <td>
            { #if showMultipleToxicity }
              {intersectionWords.map((id) => $editHistoryStore.currentTokens[id]).join(", ")}
            { :else }
              {$editHistoryStore.currentTokens[$editHistoryStore.hoveredToken]}
            { /if }
          </td>
          <td>
            <div class="columns">
              { #if showMultipleToxicity }
                <div class="column is-2" style="font-size: 17px">{Math.round($highlightedTextResponse["originalToxicity"][0] * 100)}%</div>
                <div class="column" style="padding-top: 7%; padding-left:7%">
                  <progress class="progress" value="{Math.round($highlightedTextResponse["originalToxicity"][0] * 100)}" max="100">
                  </progress>
                </div>              
              { :else if $analyzedTextResponse }
                <div class="column is-2" style="font-size: 17px">{Math.round($analyzedTextResponse["mainInputResults"]["sigmoidOutput"][0]["value"] * 100)}%</div>
                <div class="column" style="padding-top: 7%; padding-left:7%">
                  <progress class="progress" value="{Math.round($analyzedTextResponse["mainInputResults"]["sigmoidOutput"][0]["value"] * 100)}" max="100">
                  </progress>
                </div>
              { /if }
            </div>
          </td>
        </tbody>
      </table>
      <div>
      <table class="table">
        <thead>
          <tr>
            <th>Alternative</th>
            <th style="width: 150%"></th>
          </tr>
        </thead>
        <tbody on:mouseleave={leaveMain}>
        
          { #if showMultipleToxicity && intersectionWords.length > 0 }
            { #each $highlightedTextResponse["alternatives"] as alternative, idx }
              <tr 
                class="clickable"
                on:mouseenter={() => {}}
                on:mousedown="{() => {handleAlternativeClick(alternative[1], intersectionWords)}}"> 

                <td>
                  {alternative[1].reduce((curr, word) => {
                    return curr + (isDeleteOperation(word) ? ", [delete]" : ", " + word)
                  }, "").slice(1)}
                </td>
                <td>
                  <div class="columns">
                    <div class="column is-2" style="font-size: 17px">{Math.round(alternative[0]*100)}%</div>
                    <div class="column" style="padding-top: 7%; padding-left:7%">
                      <progress class="progress" value="{Math.round(alternative[0]*100)}" max="100">
                      </progress>
                    </div>
                  </div>
                </td>
              </tr>
            { /each }        
          { :else if ($analyzedTextResponse && $editHistoryStore.hoveredToken in $analyzedTextResponse["alternatives"])}
            { #each $analyzedTextResponse["alternatives"][$editHistoryStore.hoveredToken] as alternative, idx }
              <tr 
                class="clickable"
                on:mouseenter={() => {enterAlternative(alternative[1])}}
                on:mousedown="{() => {handleAlternativeClick([alternative[0]], [$editHistoryStore.hoveredToken])}}"> 

                <td>
                  {#if isDeleteOperation(alternative[0])}
                    {"[delete]"}
                  {:else}
                    {alternative[0]}
                  {/if}
                </td>
                <td>

                  <div class="columns">
                    <div class="column is-2" style="font-size: 17px">{Math.round(alternative[1]*100)}%</div>
                    <div class="column" style="padding-top: 7%; padding-left:7%">
                      <progress class="progress" value="{Math.round(alternative[1]*100)}" max="100"></progress>
                    </div>
                  </div>
                </td>
              </tr>
            { /each }
          { /if }
        </tbody>
      </table>
      </div>
    { /if }
  </div>
</div>
