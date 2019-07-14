function main() {
    const getLink = (src) => {

        // let colon = "";
        // if (window.location.port !== "")
            // colon = ":";
        const {protocol, port, hostname} = window.location;
        return 'https://www.thesearchbase.com/' + src;
    };

    fetch(getLink("/static/widgets/chatbot/asset-manifest.json?NoCache=" + new Date().getTime()))
        .then(response => response.json())
        .then(manifest => {
            // request and get assistant data
            const scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
            const isDirectLink = scriptTag.getAttribute('directLink') || '';
            const assistantID = scriptTag.getAttribute('data-id');
            const btnColor = scriptTag.getAttribute('data-circle') || '#1890ff';

            const s = document.createElement("script");
            s.src = getLink(`/static/widgets/chatbot${manifest.files['main.js']}`);
            s.async = true;
            s.defer = true;
            s.setAttribute('data-directLink', isDirectLink || '');
            s.setAttribute('data-name', 'tsb-widget');
            s.setAttribute('data-id', assistantID);
            s.setAttribute('data-circle', btnColor);
            s.setAttribute("id", "oldBotScript");

            document.body.appendChild(s);

            const l = document.createElement("link");
            l.href = getLink(`/static/widgets/chatbot${manifest.files['main.css']}`);
            l.type = "text/css";
            l.rel = "stylesheet";
            document.getElementsByTagName("head")[0].appendChild(l);
        });
}

main();
