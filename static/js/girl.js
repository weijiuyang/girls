/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */

var prevScrollpos = window.pageYOffset;
var name;

window.onscroll = function() {

  var currentScrollPos = window.pageYOffset;

  if (prevScrollpos > currentScrollPos) {

    document.getElementById("navbar").style.top = "0";

  } else {

    document.getElementById("navbar").style.top = "-100px";

  }
  // log.console("ssss")

  prevScrollpos = currentScrollPos;

}


/* Open */

function openNav() {

  document.getElementById("myNav").style.display = "block";

}




/* Close */

function closeNav() {

  document.getElementById("myNav").style.display = "none";

}

/* Set the width of the side navigation to 250px */
function openSideNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeSideNav() {
  document.getElementById("mySidenav").style.width = "0";
}






/* Open */
var curaduio = null;
var curtext = null
function playAudio(name) {
  if (curaduio != null) {
    curaduio.pause();
    curtext.style.animation = ``;
    curtext.offsetHeight; 
  }

  audio = document.getElementById(name);
  aduiotext = document.getElementById('text_'+name);
  duration = audio.duration
  aduiotext.style.animation = `breathe 1s ease-in-out `;
  console.log(aduiotext.style.animation)
  aduiotext.style.animationIterationCount = Math.round(duration)

  curaduio = audio
  curtext = aduiotext;
  console.log(curaduio)
  curaduio.play();

}



