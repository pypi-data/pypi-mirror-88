jQuery(function ($) {
  var render = function () {
    $("#content .trac-mathjax").each(function() {
      var node = $(this);
      var type = /^div$/i.test(this.tagName) ?
                 'math/tex; mode=display' : 'math/tex';
      var script = $('<script></script>').attr('type', type).text(node.text());
      node.replaceWith(script);
    });
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
  };
  render();
  $(document).ajaxSuccess(render);
});
