function showSpeechs(){
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange(function(){
        if(self.status==200 && self.readyState==4){
            document.getElementById("demo").innerHTML="sahaar"
        }
    })
    xhttp.open("POST","/firstPage",true);
    xhttp.send();
}