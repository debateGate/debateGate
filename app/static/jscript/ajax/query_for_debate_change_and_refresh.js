var script = document.currentScript;
var debate_id = script.getAttribute("debate_id");
var round_num = script.getAttribute("round_num");
var debate_stage = script.getAttribute("debate_stage");


function checkDebateForChange() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var json = JSON.parse(this.responseText);

            if(json["moved_on"] == true) {
                window.location.reload();
            }
        }
    };

    xhttp.open("GET", "https://www.debategate.net/api/has-debate-moved-on-boolean/" + debate_id +
               "/" + round_num + "/" + debate_stage , false);
    xhttp.send();
}

window.setInterval(checkDebateForChange, 20000);
