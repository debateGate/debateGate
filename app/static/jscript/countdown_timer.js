function reloadPage() {
    window.location.reload();
}


function countdownLoop() {
    var now = new Date().getTime();

    var days = Math.floor(distance / (1000 * 60 * 60 *24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (minutes > 5) {
        utcTimeHtmlContainer.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    } else if (minutes <= 5 && hours == 0 && days == 0) {
        utcTimeHtmlContainer.innerHTML = "<span style=\"color:red;\">" + days + "d " + hours + "h "
            + minutes + "m " + seconds + "s " + "</span>";
    } else {
        utcTimeHtmlContainer.innerHTML = "<b> Time is up! Refreshing debate... </b>";
        window.setTimeout(reloadPage, 5000);
    }
}

var utcTimeHtmlContainer = document.getElementById("timecontainer");

window.setInterval(countdownLoop, 1000);
