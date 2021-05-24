<script>
  import { onMount, onDestroy } from "svelte";
  import { tweened } from "svelte/motion";
  import { cubicOut } from "svelte/easing";
  export let chartId;
  export let staticProgress;
  export let progressScore;
  export let width;
  export let height;
  export let fontSize;
  export let circular;

  import editHistoryStore from "../stores/editHistoryStore.js";
  
  var mounted = false;
  var progress;
  if (!staticProgress) {
    const unsubscribe = editHistoryStore.subscribe(value => {
      if (!mounted) return;
      progress.update([Math.round(value["selectedOutput"] * 100)]);
    });
    onDestroy(unsubscribe);
  }
  function CircularProgress(element, settings) {
    // HERE: set font size based on that it is given by settings
    var fontsize = fontSize;
    if ("fontsize" in settings) {
      fontsize = settings.fontsize;
    }
    var duration = settings.duration || 500;
    var w = settings.width || 200;
    var h = settings.height || w;
    var outerRadius = settings.outerRadius || w / 2;
    var innerRadius = settings.innerRadius || (w / 2) * (80 / 100);
    var range = settings.range || { min: 0, max: 100 };
    var interpolator = d3.interpolate("#FFFFFF", "#F20100");
    var svg = d3
      .select(element)
      .append("svg")
      .attr("width", w)
      .attr("height", h);

    var arc = d3
      .arc()
      .innerRadius(innerRadius)
      .outerRadius(outerRadius);

    var paths = function(numerators) {
      return numerators.map(function(numerator) {
        var degrees =
          ((numerator - range.min) / (range.max - range.min)) * 360.0;
        var radians = degrees * (Math.PI / 180);
        var data = { value: numerator, startAngle: 0, endAngle: radians };
        return data;
      });
    };

    var g = svg
      .append("g")
      .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");
    var initial_toxicity = 0;

    //initialise the control
    g.datum([initial_toxicity])
      .selectAll("path") // HERE: used initial_toxicity
      .data(paths)
      .enter()
      .append("path")
      .attr("fill", "#FFFFFF")
      .attr("d", arc)
      .each(function(d) {
        this._current = d;
      });

    svg
      .datum([initial_toxicity])
      .selectAll("text") // HERE: used initial_toxicity
      .data(paths)
      .enter()
      .append("text")
      .attr("transform", "translate(" + w / 2 + ", " + h / 1.6 + ")")
      .attr("text-anchor", "middle")
      .attr("font-size", (fontsize || 60) + "px") // HERE: used fontsize instead of fontSize
      .text(function(d) {
        return d.value;
      });

    this.update = function(percent) {
      g.datum(percent)
        .selectAll("path")
        .data(paths)
        .transition()
        .duration(duration)
        .attr("fill", interpolator(percent / 100))
        .attrTween("d", arcTween);
      svg
        .datum(percent)
        .selectAll("text")
        .data(paths)
        .text(function(d) {
          return d.value;
        });
    };

    var arcTween = function(initial) {
      var interpolate = d3.interpolate(this._current, initial);
      this._current = interpolate(0);
      return function(t) {
        return arc(interpolate(t));
      };
    };
  }
  // Here: Initialize delta toxic charts
  function deltaToxicProgress(element, settings) {
    // HERE: set font size based on that it is given by settings
    var fontsize = fontSize;
    if ("fontsize" in settings) {
      fontsize = settings.fontsize;
    }

    var w = settings.width || 200;
    var h = settings.height || w;
    var svg = d3
      .select(element)
      .append("svg")
      .attr("class", "delta-toxicicy")
      .attr("width", w)
      .attr("height", h);

    // Initialize svg
    var initial_toxicity = 0;
    svg
      .datum([initial_toxicity])
      .append("text")
      .attr("transform", "translate(" + w / 2 + ", " + h / 1.6 + ")")
      .attr("text-anchor", "middle")
      .attr("font-size", (fontsize || 60) + "px")
      .text(function(toxic_val) {
        return toxic_val;
      });

    // Update svg
    this.update = function(percent) {
      svg.selectAll("text").text(percent);
    };
  }

  onMount(async () => {
    var charts = document.getElementById(chartId);
    mounted = true;

    if (staticProgress) {
      progress = circular
        ? new CircularProgress(charts, { width, height })
        : new deltaToxicProgress(charts, { width, height });
      var delta = Math.floor(progressScore);
      progress.update([delta]);
    } else {
      progress = new CircularProgress(charts, { width, height });
    }
  });
</script>

<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/icon?family=Material+Icons" />
<div id={chartId} />
