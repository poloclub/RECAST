async function getToxicity(input, alternatives, uuid) {
  var url = 'http://localhost:8000';
  var data = {}
  if (alternatives) {
    data = { text: input[0], uuid: uuid, alternatives: input[1] };
    url += "/toxicity"
  } else {
    data = { text: input, uuid: uuid };
  }

  const response = await fetch(url, {
    method: 'POST',
    body: JSON.stringify(data), 
    headers: {
      'Content-Type': 'application/json'
    }
  });
  return (await response.json());
}

function nextNode(node) {
  if (node.hasChildNodes()) {
    return node.firstChild;
  } else {
    while (node && !node.nextSibling) {
      node = node.parentNode;
    }
    if (!node) {
      return null;
    }
    return node.nextSibling;
  }
}

function getRangeSelectedNodes(range) {
  var node = range.startContainer;
  var endNode = range.endContainer;
  // Special case for a range that is contained within a single node
  if (node == endNode) {
    return [node];
  }

  // Iterate nodes until we hit the end container
  var rangeNodes = [];
  while (node && node != endNode) {
    rangeNodes.push(node = nextNode(node));
  }

  // Add partially selected nodes at the start of the range
  node = range.startContainer;
  while (node && node != range.commonAncestorContainer) {
    rangeNodes.unshift(node);
    node = node.parentNode;
  }

  return rangeNodes;
}

function isDeleteOperation(alternative) {
  return alternative.replace(/[^a-z0-9+]+/gi, '').length == 0
}

function stylingAttributes(color) {
  if (!color) color = 0;
  color = (Math.log(color) + 1) > 0 ? (Math.log(color) + 1) : .01
  return `
  border-bottom: 4px solid;
  border-bottom-color: rgba(255, 0, 110, ${color});
  `
}

export { getRangeSelectedNodes, nextNode, getToxicity, isDeleteOperation, stylingAttributes }