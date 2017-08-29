function showSpeechs() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.status == 200 && this.readyState == 4) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    }
    xhttp.open("GET", "/selectSpeech", true);
    //xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}