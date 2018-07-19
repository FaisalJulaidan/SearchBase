var angle = 0;
var degreeInRadians = 2 * Math.PI / 360;
var realX = 0;
var realY = 0;
var opened = false;
var frame = document.getElementById("iframediv");
var but = document.getElementById("launch_button");
var butAp = document.getElementById("launch_button_appendix");
var closeBut = document.getElementById("overChatbotIframeCloseButton");
var hoovered = false;
var btn_text = $("#launch_button_appendix");
var autoPop = "";

$("#launch_button_appendix").rotate({
    animateTo: 90,
});


$(document).ready(function () {
    frame.style = "display:none";
    but.addEventListener("click", openAssistant);
    butAp.addEventListener("click", openAssistant);
    closeBut.addEventListener("click", closeAssistant);

    $(document).on("mouseover", ".launch_btn_holder", function () {
        OpenButtonHover();
    });

    $(document).on("mouseleave", ".launch_btn_holder", function () {
        OpenButtonHoverEnd();
    });
    GetPopSettings();
});


function openAssistant() {
    if (!opened) {
        frame.style = "display:block";
        //$("#iframediv").fadeIn("slow", function () {
        //    // Animation complete
        //});
        $("#iframediv").animate({
            marginBottom: "+=35px",
            opacity: 1
        }, 400);
        but.style = "display:none";
        butAp.style = "display:none";
        opened = true;
    }
}

function closeAssistant() {
    if (opened) {
        $("#iframediv").animate({
            marginBottom: "-=35px",
            opacity: 0
        }, 400);
        setTimeout(function () {
            frame.style = "display:none";
            but.style = "display:inline-block";
            butAp.style = "display:inline-block";
            opened = false;
        }, 400);
    }
}

function OpenButtonHover() {
    if (!hoovered) {
        hoovered = true;
        $("#launch_button_appendix").stop();
        $("#launch_button_appendix").animate({
            // marginLeft: "+=20px",
            // marginBottom: "+=76px",
            marginLeft: "-16px",
            marginBottom: "11px",
            opacity: 1,

        }, 600);
        $("#launch_button_appendix").rotate({
            animateTo: 0,
        })
    }
}

function OpenButtonHoverEnd() {
    if (hoovered) {
        $("#launch_button_appendix").stop();
        $("#launch_button_appendix").animate({
            marginLeft: "-133px",
            marginBottom: "-130px",
            opacity: 0,
        }, 600);
        $("#launch_button_appendix").rotate({
            animateTo: 90,
        })
        hoovered = false;
    }
}

function GetPopSettings() {
    var url = window.location.href;
    params = "URL=" + url;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "https://www.thesearchbase.com/getpopupsettings", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                var data = xhttp.responseText;
                autoPop = data;
                autoPop = autoPop.replace("\"", "");
                if (autoPop != "Off") {
                    setTimeout(openAssistant, parseInt(autoPop) * 1000);
                }
            }
            else {
                console.error(xhttp.statusText);
            }
        }
    };
    xhttp.send(params);
}