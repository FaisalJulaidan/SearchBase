function includeHTML() {
    console.log("Starting chatbot process")
    var z, i, elmnt, file, xhttp;
    var link = "https://www.thesearchbase.com/assistant/pagerequest";
    /*loop through a collection of all HTML elements:*/
    z = document.getElementsByTagName("div");
    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        /*search for elements with a certain atrribute:*/
        //file = elmnt.getAttribute("w3-include-html");
        file = link
        console.log(file);
        if (file) {
            /*make an HTTP request using the attribute value as the file name:*/
            console.log("Getting chatbot from TheSearchBase");
            var xhttp = new XMLHttpRequest();
            if (!"withCredentials" in xhttp) {
                xhttp = new XDomainRequest();
            }
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) { elmnt.innerHTML = this.responseText; }
                    if (this.status == 404) { elmnt.innerHTML = "Page not found."; }
                    /*remove the attribute, and call this function once more:*/
                    elmnt.removeAttribute("w3-include-html");
                    link = "Stop";
                    console.log("Initialising chatbot");
                    //put self-call here for multiple pulls
                }
            }
            xhttp.open("GET", file, true);
            xhttp.send();
            /*exit the function:*/
            return;
        } else {
            //used for multiple pulls
        }
    }
}
includeHTML();