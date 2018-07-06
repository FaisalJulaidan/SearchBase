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

$(document).ready(function () {
    frame.style = "display:none";
    but.addEventListener("click", openAssistant);
    butAp.addEventListener("click", openAssistant);
    closeBut.addEventListener("click", function () {
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
    });

    $(document).on("mouseover", ".launch_btn_holder", function () {
        OpenButtonHover();
    });

    $(document).on("mouseleave", ".launch_btn_holder", function () {
        OpenButtonHoverEnd();
    });
});


function openAssistant() {
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

function OpenButtonHover() {
    if (!hoovered) {
        $("#launch_button_appendix").animate({
            // marginLeft: "+=20px",
            // marginBottom: "+=76px",
            marginLeft: "-20px",
            marginBottom: "0px",
            opacity: 1,

        }, 600);
        $("#launch_button_appendix").rotate({
            animateTo: 0,
        })
        hoovered = true;

    }
}
function OpenButtonHoverEnd() {
    if (hoovered) {
        $("#launch_button_appendix").animate({
            marginLeft: "-177px",
            marginBottom: "-147px",
            opacity: 0,
        }, 600);
        $("#launch_button_appendix").rotate({
            animateTo: 90,
        })
        hoovered = false;
    }
}