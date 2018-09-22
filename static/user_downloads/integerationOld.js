
(function (global) {

  // add array index of for old browsers (IE<9)
  if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function(obj, start) {
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

  var scriptTag = document.getElementsByTagName('script');

  // Create a div
    var div = document.createElement('div');
    console.log('kfkfkfkfkk');

    div.id = 'contents1';

    // add the cleanslate classs for extreme-CSS reset.
    // div.className = 'dclg-impact-indicators-embeddable .dashboard_widget cleanslate';

    // scriptTag.parentNode.insertBefore(div, scriptTag);

    var file = '<link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/style.css">\\n\' +\n' +
        '      \'    <link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/pop.css">\\n\' +\n' +
        '      \'    <link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/responsive.css">\\n\' +\n' +
        '      \'    <link href="http://127.0.0.1:5000/userdownloads/open-assistant-bar.png">\\n\' +\n' +
        '      \'    <link href="http://127.0.0.1:5000/userdownloads/open-assistant-circle.png">\\n\' +\n' +
        '      \'    \\n\' +\n' +
        '      \'    \\n\' +\n' +
        '      \'    \\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/jquery-2.2.4.min.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/jQueryRotate.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/popper.min.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/bootstrap.min.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/plugins.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/slick.min.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/active.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/footer-reveal.min.js"></script>\\n\' +\n' +
        '      \'    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/chatbot.js"></script>\\n\' +\n' +
        '      \'    \\n\' +';


    div.innerHTML = '<div id="iframediv">\n' +
      '            <div id="overChatbotIframe">\n' +
      '                <a id="overChatbotIframeHeading">TheSearchBase</a>\n' +
      '                <a id="overChatbotIframeCloseButton">X</a>\n' +
      '            </div>\n' +
      '            <!-- Will change this after the demo -->\n' +
      '            <iframe frameBorder="0" id="chatbotIframe" src="http://127.0.0.1:5000/chatbottemplate/1"></iframe>\n' +
      '        </div>\n' +
      '        <div class="launch_btn_holder">\n' +
      '            <div id="launch_button"></div>\n' +
      '            <div id="launch_button_appendix"></div>\n' +
      '        </div>';


        // scriptTag.parentNode.insertBefore(div, scriptTag);

        var body = document.getElementsByTagName("body")[0];
        // console.log(head);
        body.appendChild(div);
        body.appendChild(file);

  //
  // // make a global object to store stuff in
  // if(!global.OpenDataCommunities) { global.OpenDataCommunities = {}; }
  // var OpenDataCommunities = global.OpenDataCommunities;
  //
  // // To keep track of which embeds we have already processed
  // if(!OpenDataCommunities.processedScripts) { OpenDataCommunities.processedScripts = []; }
  // var processedScripts = OpenDataCommunities.processedScripts;
  //
  // if(!OpenDataCommunities.styleTags) { OpenDataCommunities.styleTags = []; }
  // var styleTags = OpenDataCommunities.styleTags;
  //
  // // var scriptTags = document.getElementsByTagName('script');
  //
  //
  //
  //
  // var thisRequestUrl = '<%= raw(request.url) %>';
  //
  // for(var i = 0; i < scriptTags.length; i++) {
  //   var scriptTag = scriptTags[i];
  //
  //   // src matches the url of this request, and not processed it yet.
  //   if (scriptTag.src === thisRequestUrl && processedScripts.indexOf(scriptTag) < 0) {
  //
  //     processedScripts.push(scriptTag);
  //
  //     // add the style tag into the head (once only)
  //     if(styleTags.length === 0) {
  //       // add a style tag to the head
  //       var styleTag = document.createElement("link");
  //       styleTag.rel = "stylesheet";
  //       styleTag.type = "text/css";
  //       styleTag.href =  "http://opendatacommunities.org/assets/impact_indicators_embed.css";
  //       styleTag.media = "all";
  //       console.log(styleTag);
  //       document.getElementsByTagName('head')[0].appendChild(styleTag);
  //       styleTags.push(styleTag);
  //
  //     }
  //
  //     // Create a div
  //     var div = document.createElement('div');
  //     console.log('kfkfkfkfkk');
  //
  //     div.id = 'contents1';
  //
  //     // add the cleanslate classs for extreme-CSS reset.
  //     // div.className = 'dclg-impact-indicators-embeddable .dashboard_widget cleanslate';
  //
  //     // scriptTag.parentNode.insertBefore(div, scriptTag);
  //
  //     div.innerHTML = ' <link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/style.css">\n' +
  //         '    <link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/pop.css">\n' +
  //         '    <link rel="stylesheet" href="http://127.0.0.1:5000/userdownloads/responsive.css">\n' +
  //         '    <link href="http://127.0.0.1:5000/userdownloads/open-assistant-bar.png">\n' +
  //         '    <link href="http://127.0.0.1:5000/userdownloads/open-assistant-circle.png">\n' +
  //         '    \n' +
  //         '    \n' +
  //         '    \n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/jquery-2.2.4.min.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/jQueryRotate.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/popper.min.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/bootstrap.min.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/plugins.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/slick.min.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/active.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/footer-reveal.min.js"></script>\n' +
  //         '    <script type="text/javascript" src="http://127.0.0.1:5000/userdownloads/chatbot.js"></script>\n' +
  //         '    \n' +
  //         '        <div id="iframediv">\n' +
  //         '            <div id="overChatbotIframe">\n' +
  //         '                <a id="overChatbotIframeHeading">TheSearchBase</a>\n' +
  //         '                <a id="overChatbotIframeCloseButton">X</a>\n' +
  //         '            </div>\n' +
  //         '            <!-- Will change this after the demo -->\n' +
  //         '            <iframe frameBorder="0" id="chatbotIframe" src="http://127.0.0.1:5000/chatbottemplate/1"></iframe>\n' +
  //         '        </div>\n' +
  //         '        <div class="launch_btn_holder">\n' +
  //         '            <div id="launch_button"></div>\n' +
  //         '            <div id="launch_button_appendix"></div>\n' +
  //         '        </div>';
  //
  //   }
  // }





})(this);




















