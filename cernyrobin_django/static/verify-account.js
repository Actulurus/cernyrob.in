  function changeOpenStatusE() {
    console.log(document.getElementById("email-text"))
    var article = document.getElementById("email-text");


      if (article.style.maxHeight) {
        article.style.maxHeight = null;
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
      }
    }
  

  function changeOpenStatusB() {
    console.log(document.getElementById("benefits-text"))
    var article = document.getElementById("benefits-text");

      if (article.style.maxHeight) {
        article.style.maxHeight = null;
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
      }
    }
  
function showVerifyContainer(){
  document.getElementById("tldr-button").style.display = "none"
  document.getElementById("goto-verify").style.display = "none"
  document.getElementById("verification-container").style.display = "block"
  document.getElementById("verify-form").scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
}

  document.addEventListener("DOMContentLoaded", function () {
    changeOpenStatusB()
  });
