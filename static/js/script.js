function showSpeechs() {
    var xhttp = new XMLHttpRequest();
    var speech;
    xhttp.onreadystatechange = function () {
        if (this.status == 200 && this.readyState == 4) {
            //console.log(this.responseText)
            speech=JSON.parse(this.responseText);
            document.getElementById("demo1").innerHTML = speech.speech;
            document.getElementById("demo2").innerHTML = speech.speaker;
            document.getElementById("demo3").innerHTML = speech.source;
        }
    }
    xhttp.open("GET", "/selectSpeech", true);
    //xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}