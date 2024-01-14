document.addEventListener("DOMContentLoaded", function () {
  if (Math.floor(Math.random() * 100) <= 10) {
    setTimeout(function () {
      document.getElementById("info").style.display = "flex";

      document.getElementById("rButton").style.visibility = "visible";
      document.getElementById("rButtonCont").style.visibility = "visible";
    }, Math.floor(Math.random() * 1000 + 500)); // Random time

    var div = document.getElementById('info');
    var isLarge = false; // State tracking variable

    function toggleSize() {
      // Change the size of the div based on its current state
      div.style.width = isLarge ? '35%' : '40%';
      /*   div.style.height = isLarge ? '200px' : '300px'; */

      isLarge = !isLarge; // Toggle state
    }

    setInterval(toggleSize, 100); // Adjust the size every 1 second

    //setInterval(toggleSize, 1000);

  }
});

function closePopup() {
  document.getElementById("info").style.display = "none";
}
function buttonClick(number) {
  if (number == 1) {
    document.getElementById("lButton").style.visibility = "visible";
    document.getElementById("info").style.display = "none";

  }
  else if (number == 2) {
    document.getElementById("rButton").style.visibility = "hidden";
    document.getElementById("lButton").style.visibility = "visible";
  }


}