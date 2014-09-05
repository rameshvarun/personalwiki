window.search_index = lunr(function() {
  this.field('title', 10)
  this.field('tags', 100)
  this.field('body')

  this.ref('id')
})

window.article_index = {}
$.getJSON(path_to_root + "index.json", function(data) {
  window.article_index = data
  for(name in data) {
    window.search_index.add({
      id : name,
      body : data[name].body,
      title : data[name].title,
      tags : data[name].tags.join(" ")
    })
  }
})


$(function() {
  $("#search").select2({
    width : 200,
    placeholder: "Article Search",
    query: function (query) {
      search_results = window.search_index.search(query.term)

      var data = {results: []}
      for(var i = 0; i < search_results.length; ++i) {
        var article = window.article_index[search_results[i].ref];
        data.results.push({ id: article.id, text: article.title })
      }
      query.callback(data)
    }
  })

  $("#search").on("change", function(e) {
    window.location = path_to_root + e.val + ".html"
  });

  // Random titles
  var titles = ["The Dungeon", "The Spawning Pool", "The Nursery"];
  $("#wiki-title").html(titles[Math.floor(Math.random()*titles.length)]);
});
