"use strict";

function main() {
    var getLink = function getLink(src) {
        var _window$location = window.location,
            protocol = _window$location.protocol,
            port = _window$location.port,
            hostname = _window$location.hostname;

        // return 'http://localhost:5000' + src;
        return 'https://www.thesearchbase.com' + src;
    };

    var options = {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'text/json',
            'Accept': 'application/json',
        }
    };
    fetch(getLink("/api/static/widgets/chatbot/asset-manifest.json?NoCache=" + new Date().getTime()), options).then(function (response) {
        return response.json();
    }).then(function (manifest) {
        // request and get assistant data
        var scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
        var isDirectLink = scriptTag.getAttribute('directLink') || '';
        var assistantID = scriptTag.getAttribute('data-id');
        var btnColor = scriptTag.getAttribute('data-circle') || '#1890ff';
        var s = document.createElement("script");
        s.src = getLink("/api/static/widgets/chatbot".concat(manifest.files['main.js']));
        s.async = true;
        s.defer = true;
        s.setAttribute('data-directLink', isDirectLink || '');
        s.setAttribute('data-name', 'tsb-widget');
        s.setAttribute('data-id', assistantID);
        s.setAttribute('data-circle', btnColor);
        s.setAttribute("id", "oldBotScript");
        document.body.appendChild(s);
        var l = document.createElement("link");
        l.href = getLink("/api/static/widgets/chatbot".concat(manifest.files['main.css']));
        l.type = "text/css";
        l.rel = "stylesheet";
        document.getElementsByTagName("head")[0].appendChild(l);
    }).catch(function (error) {
        console.log(error);
    });
}

main();
