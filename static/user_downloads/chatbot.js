var angle = 0;
var degreeInRadians = 2 * Math.PI / 360;
var realX = 0;
var realY = 0;
var opened = false;
var frame = undefined;
var but = undefined;
var butAp = undefined;
var closeBut = undefined;
var btn_text = undefined;
var hoovered = false;
var autoPop = "";


$(document).ready(function () {
    frame = document.getElementById("iframediv");
    but = document.getElementById("launch_button");
    butAp = document.getElementById("launch_button_appendix");
    closeBut = document.getElementById("overChatbotIframeCloseButton");
    frame.style = "display:none";
    btn_text = $("#launch_button_appendix");
    console.log(btn_text);

    btn_text.rotate({
    animateTo: 90
    });

    but.addEventListener("click", openAssistant);
    butAp.addEventListener("click", openAssistant);
    closeBut.addEventListener("click", closeAssistant);

    $(document).on("mouseover", ".launch_btn_holder", function () {
        OpenButtonHover();
    });

    $(document).on("mouseleave", ".launch_btn_holder", function () {
        OpenButtonHoverEnd();
    });




    loadIframe(globalTSB.host, globalTSB.id);
    GetPopSettings(globalTSB.host, globalTSB.id);

});




function openAssistant() {
    if (!opened) {
        frame.style.display = "block";
        //$("#iframediv").fadeIn("slow", function () {
        //    // Animation complete
        //});
        $("#iframediv").animate({
            marginBottom: "+=35px",
            opacity: 1
        }, 400);
        but.style.display = "none";
        butAp.style.display= "none";
        opened = true;
    }
}

function closeAssistant() {
            console.log('aaaaa');

    if (opened) {
        $("#iframediv").animate({
            marginBottom: "-=35px",
            opacity: 0
        }, 400);
        setTimeout(function () {
            frame.style.display = "display:none";
            but.style.display = "inline-block";
            butAp.style.display = "inline-block";
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

function loadIframe(host, id) {
    var $iframe = $('#' + "chatbotIframe");
    url = host + "/chatbottemplate/" + id;
    $iframe.attr('src', url);
}

function GetPopSettings(host, id) {
    $.ajax({
        url: host + "/getpopupsettings/" + id,
        type: "GET"
    }).done(function (res) {

        console.log("Pop settings retrieved successfully!");
        var data = JSON.parse(res).data;

        setTimeout(openAssistant, parseInt(data['SecondsUntilPopUp']) * 1000);
        //var frameText = data.split("&&&")[1]
        //document.getElementById("overChatbotIframeHeading").innerHTML = frameText;

    }).fail(function (res) {
        console.log("Error in retrieving pop settings.");
        console.log(res);
    });
}

