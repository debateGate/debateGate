function convertFromUTCToLocal() {
    //get offset between UTC and Local time
    var offset = new Date().getTimezoneOffset();

    //nab the UTC time from the HTML and parse it into a Date object
    var utcTimeHtmlContainer = document.getElementById("timecontainer");
    var newDate = new Date(utcTimeHtmlContainer.innerHTML);

    //convert the newDate object from UTC to Local
    newDate.setMinutes(newDate.getMinutes() - offset);

    //set the time HTML container to the new local Date object
    utcTimeHtmlContainer.innerHTML = newDate.toString();
}

convertFromUTCToLocal();
