var globalTSB = {
    id: undefined,
    // host: 'https://www.thesearchbase.com',
    host: 'http://localhost:5000',
    files_path: '/userdownloads',
    iframe_route: '/chatbottemplate_production'
};

var fullLoad = { "jquery": false, "popupsettings": false, "iframe": false };

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


window.onload = (async function (global) {

    // Add array index of for old browsers (IE<9)
    if (!Array.prototype.indexOf) {
        Array.prototype.indexOf = function (obj, start) {
            var i, j;
            i = start || 0;
            j = this.length;
            while (i < j) {
                if (this[i] === obj) {
                    return i;
                }
                i++;
            }
            return -1;
        };
    }



    // Config
    var host = globalTSB.host;
    var files_path = globalTSB.files_path;
    var iframe_route = globalTSB.iframe_route;
    var popupSec = undefined;
    var topBarText = "";

    var integration_file = host + files_path + 'integration.js';
    var id = document.querySelector('script[data-name="tsb-widget"][data-id]').getAttribute('data-id');
    globalTSB.id = id;

    function clickToShowColor() {
        var script = document.getElementsByTagName('script')[0];
        return {
            icon: script.getAttribute('data-icon'),
            circle: script.getAttribute('data-circle')
        };
    }



    // Tags to be added
    var styleTags = ['/pop.css'];
    //var scriptTags = ['/jquery-2.2.4.min.js', '/jQueryRotate.js', '/active.js'];
    var scriptTags = ['/chatbotJSMerge.min.js'];


    // import font-awesome
    styleLink = document.createElement("link");
    styleLink.rel = "stylesheet prefetch";
    styleLink.type = "text/css";
    styleLink.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.2/css/font-awesome.min.css";
    document.getElementsByTagName('head')[0].appendChild(styleLink);

    // create style tags
    var styleLink = undefined;
    for (var i = 0; i < styleTags.length; i++) {
        styleLink = document.createElement("link");
        styleLink.rel = "stylesheet prefetch";
        styleLink.type = "text/css";
        styleLink.href = host + files_path + styleTags[i];
        styleLink.media = "all";
        document.getElementsByTagName('head')[0].appendChild(styleLink);
    }


    // Build The Chatbot Button and iFrame //
    var container = document.createElement('div');
    container.id = 'TSB-container';
    // Create chatbot button div
    var btnDiv = document.createElement('div');
    btnDiv.id = 'TSB-chatbot-widget';

    btnDiv.innerHTML = ' <div class="TSB-circle" style="background-color: '+ clickToShowColor().circle +'; color: '+clickToShowColor().icon+'; ">\n' +
        '               <i class="fa fa-comments"></i>\n' +
        '             </div>';




    // Create chatbot iFrame div
    var iFrameDiv = document.createElement('div');
    iFrameDiv.id = 'TSB-iframediv';
    iFrameDiv.style.height = '0px';
    iFrameDiv.style.opacity = '0';

    iFrameDiv.innerHTML = '<div class="TSB-contact-profile">\n' +
        '        <img src=\"'+host+'/static/user_downloads/favicon-96x96.png\" alt=""/>\n' +
        '        <p id="tsb-bot-header" class="TSB-bot-title">Bot</p>\n' +
        '\n' +
        '        <div class="TSB-social-media" id=\'TSB-closeIframe\'>\n' +
        '            <i class="fa fa-close" aria-hidden="true"></i>\n' +
        '        </div>\n' +
        '\n' +
        '        <div id=\'TSB-refreshIframe\' class="TSB-social-media" >\n' +
        '            <i class="fa fa-refresh" aria-hidden="true"></i>\n' +
        '        </div>\n' +
        '    </div>\n' +
        '    <iframe frameborder="0" id="TSB-chatbotIframe" src=\"\"></iframe>';

    // Add the container and two  divs to the page dom
    document.getElementsByTagName('body')[0].appendChild(container);
    document.getElementById('TSB-container').appendChild(btnDiv);
    document.getElementById('TSB-container').appendChild(iFrameDiv);
    // === ==== ==== ===== ==== ==== ====


    // Create script tags
    var script = undefined;
    var popOpen = false;
    for (i = 0; i < scriptTags.length; i++) {

        script = document.createElement('script');
        script.type = "text/javascript";
        script.language = "javascript";
        script.src = host + files_path + scriptTags[i];

        document.getElementsByTagName('body')[0].appendChild(script);
        await sleep(100);
    }



    document.getElementById("TSB-iframediv").style.display = "none";

    // Open iframe
    document.getElementById('TSB-chatbot-widget').addEventListener('click', e => {
        if (!popOpen) {
            $chatbotWidget = $("#TSB-chatbot-widget");
            $chatbotWidget.animate({
                height: '0px',
                opacity: '0',
            }, 500, () => {
                $("#TSB-chatbot-widget").hide();
            });

            iFrameDiv = document.getElementById("TSB-iframediv");
            iFrameDiv.style.display = "block";
            iFrameDiv = $("#TSB-iframediv");
            iFrameDiv.animate({
                height: "530px",
                opacity: '1'
            });
            popOpen = true;
        }

    });


    document.getElementById('TSB-closeIframe').addEventListener('click', e => {
        if (popOpen) {
            $chatbotWidget = $("#TSB-chatbot-widget");
            $chatbotWidget.show();
            $chatbotWidget.css('height', 'auto');
            $chatbotWidget.animate({
                opacity: '1',
            });

            $("#TSB-iframediv").animate({
                height: '0px',
                opacity: '0',
            }, 500, () => {
                $("#TSB-iframediv").hide();
            });
            popOpen = false;
        }
    });

    // Reset the iframe
     document.getElementById('TSB-refreshIframe').addEventListener('click', e => {
          document.getElementById('TSB-chatbotIframe').src = host  + iframe_route + '/' + id;
    });

     // Popup
     function getPopupSettings(){
        return new Promise(function(resolve, reject){
            var xhr = new XMLHttpRequest();
            xhr.open('GET', host + '/getpopupsettings/' + id);
            xhr.onload = function () {
                fullLoad["popupsettings"] = true;
                if (xhr.status === 200) {
                    popupSec = JSON.parse(xhr.responseText).data.SecondsUntilPopUp;
                    topBarText = JSON.parse(xhr.responseText).data.TopBarText;
                    return resolve(true);
                }
                else {
                    console.log(xhr.status);
                    reject(false);
                }
            };
            xhr.send();
        });

     }

    getPopupSettings();

    var interval = setInterval(checkForFullLoad, 500);

    function checkForFullLoad() {
        try {
            $("#TSB-container"); //check if jquery has loaded
            fullLoad["jquery"] = true;
        } catch (error) { }
        if (fullLoad["jquery"] && fullLoad["popupsettings"]) {
            $("#tsb-bot-header")[0].innerHTML = topBarText;

            fadein(document.getElementById("TSB-container"));

            clearInterval(interval);
            document.getElementById('TSB-chatbotIframe').src = host + iframe_route + '/' + id;

            setTimeout(function () {
                if (!popOpen) {
                    document.getElementById('TSB-chatbot-widget').click();
                }
            }, popupSec * 1000);
        }
    }

    function fadein(element) {
        var op = 0.1;  // initial opacity
        element.style.opacity = op;
        element.style.display = 'block';
        var timer = setInterval(function () {
            if (op >= 1) {
                clearInterval(timer);
            }
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op += op * 0.1;
        }, 10);
    }


    // Chatbot box width responsiveness
    const phones = window.matchMedia('(min-width:461px)').matches;
    iFrameDiv.style.width = window.screen.width - 41 + 'px';
    if (phones) {
        iFrameDiv.style.width = "460px";
    }

})(this);
