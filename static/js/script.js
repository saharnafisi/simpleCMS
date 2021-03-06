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

function addSpeech(){
    var xhttp=new XMLHttpRequest();
    var addSpeech;
    var speech=document.getElementById("speech").value;
    var speaker=document.getElementById('speaker').value;
    var source=document.getElementById("source").value;
    console.log(speech);
    xhttp.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            addSpeech=JSON.parse(this.responseText);
            document.getElementById("addSpeechMsg").innerHTML=addSpeech.message;
        }
    }
    xhttp.open("POST", "/add-speech", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("speech="+speech+"&speaker="+speaker+"&source="+source);
}