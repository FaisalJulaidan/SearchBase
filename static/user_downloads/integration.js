var globalTSB = {
    id: undefined,
    host: 'https://www.thesearchbase.com',
    // host: 'http://localhost:5000',
    files_path: '/userdownloads',
    iframe_route: '/chatbottemplate_production'
};


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
    var integration_file = host + files_path + 'integration.js';
    var id = document.querySelector('script[data-name="tsb-widget"][data-id]').getAttribute('data-id');
    globalTSB.id = id;


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

    btnDiv.innerHTML = ' <div class="TSB-circle">\n' +
        '               <i class="fa fa-cloud"></i>\n' +
        '             </div>';




    // Create chatbot iFrame div
    var iFrameDiv = document.createElement('div');
    iFrameDiv.id = 'TSB-iframediv';
    iFrameDiv.style.width = '320px';
    iFrameDiv.style.height = '0px';
    iFrameDiv.style.opacity = '0';

    iFrameDiv.innerHTML = '<div class="TSB-contact-profile">\n' +
        '        <img src=\"'+host+'/static/user_downloads/favicon-96x96.png\" alt=""/>\n' +
        '        <p class="TSB-bot-title">Bot</p>\n' +
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
    for (i = 0; i < scriptTags.length; i++) {

        script = document.createElement('script');
        script.type = "text/javascript";
        script.language = "javascript";
        script.src = host + files_path + scriptTags[i];

        document.getElementsByTagName('body')[0].appendChild(script);
        await sleep(100);
    }


    // Animations
    function reloadIframe(){
      document.getElementById('TSB-chatbotIframe').src = host  + iframe_route + '/' + id;
    }

    document.getElementById("TSB-iframediv").style.display = "none";

    // Open iframe
    document.getElementById('TSB-chatbot-widget').addEventListener('click', e => {
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
            height: '370px',
            opacity: '1',
        });

        reloadIframe();

    });


    document.getElementById('TSB-closeIframe').addEventListener('click', e => {

        $chatbotWidget = $("#TSB-chatbot-widget");
        $chatbotWidget.show();
        $chatbotWidget.css('height','auto');
        $chatbotWidget.animate({
            opacity: '1',
        });

        $("#TSB-iframediv").animate({
            height: '0px',
            opacity: '0',
        }, 500, () => {
            $("#TSB-iframediv").hide();
        })
    });

    // Reset the iframe
     document.getElementById('TSB-refreshIframe').addEventListener('click', e => {
       reloadIframe()
    });



})(this);
