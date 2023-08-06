var rendererMD = new marked.Renderer();
    marked.setOptions({
      renderer: rendererMD,
      gfm: true,
      tables: true,
      breaks: false,
      pedantic: false,
      sanitize: false,
      smartLists: true,
      smartypants: false
    })
   marked.setOptions({
        highlight: function (code) {
        return hljs.highlightAuto(code).value;
      }
    });
const mdview={
    view:function(mdtext,el){
        let html=marked(mdtext);
        $(el).html(html);
    }
}