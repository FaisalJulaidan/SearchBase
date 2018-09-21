

var globalTSB = {
  id: undefined,
  host: 'http://127.0.0.1:5000',
  files_path: '/userdownloads'
};


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


(async function (global) {

  // Add array index of for old browsers (IE<9)
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


  // Config
  var host = globalTSB.host;
  var files_path = globalTSB.files_path;
  var integration_file = host + files_path + 'integration.js';
  var id = document.querySelector('script[data-name="tsb-widget"][data-id]').getAttribute('data-id');
  globalTSB.id = id;

  // Tags to be added
  var styleTags = ['/style.css', '/pop.css', '/responsive.css', '/bootstrap.min.css', '/slick.css'];
  var scriptTags = [ '/jquery-2.2.4.min.js', '/jQueryRotate.js', '/popper.min.js',
      '/bootstrap.min.js', '/plugins.js', '/slick.min.js', '/active.js', '/footer-reveal.min.js', '/chatbot.js'];


  // create style tags
  var styleLink = undefined;
  for(var i=0; i<styleTags.length; i++) {
    styleLink = document.createElement("link");
    styleLink.rel = "stylesheet";
    styleLink.type = "text/css";
    styleLink.href =  host + files_path + styleTags[i];
    styleLink.media = "all";
    document.getElementsByTagName('head')[0].appendChild(styleLink);
  }



  // Create chatbot div
  var div = document.createElement('div');
  div.id = 'chatbotWidget';

  div.innerHTML = ' <div id="iframediv">' +
          '            <div id="overChatbotIframe">\n' +
          '                <a id="overChatbotIframeHeading">TheSearchBase</a>\n' +
          '                <a id="overChatbotIframeCloseButton">X</a>\n' +
          '            </div>\n' +
          '            <iframe frameBorder="0" id="chatbotIframe" src="'+ host +'"/chatbottemplate/"' + id + '" ></iframe>\n' +
          '        </div>\n' +

          '        <div class="launch_btn_holder">\n' +
          '            <div id="launch_button"></div>\n' +
          '            <div id="launch_button_appendix">' +
          '        </div>\n';

  document.getElementsByTagName('body')[0].appendChild(div);

  // Set images for open chatbot buttons
  document.getElementById('launch_button')
      .style.backgroundImage = "url('" + host + files_path + "/open-assistant-circle.png')";
  document.getElementById('launch_button_appendix')
      .style.backgroundImage = "url('" + host + files_path + "/open-assistant-bar.png')";


  // Create script tags
  var script = undefined;
  for(i=0; i<scriptTags.length; i++) {

    script = document.createElement('script');
    script.type = "text/javascript";
    script.language = "javascript";
    script.src = host + files_path + scriptTags[i];

    document.getElementsByTagName('body')[0].appendChild(script);
    await sleep(100);
  }






})(this);