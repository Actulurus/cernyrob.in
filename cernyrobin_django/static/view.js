  function changeOpenStatus() {
    var articles = document.getElementsByClassName("answer-text");
    for (var i = 0; i < articles.length; i++) {
      var article = articles[i];
      if (article.style.maxHeight) {
        article.style.maxHeight = null;
/*         article.style.margin = "0px 0px -5.5px 0px" */
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
/*         article.style.margin = "3px 3px 3px 3px" */
      }
    }
  }


  document.addEventListener("DOMContentLoaded", function () {
    changeOpenStatus()
  });