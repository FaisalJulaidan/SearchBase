function main() {
    const getLink = (src) => {
        const {protocol, port, hostname} = window.location;
        // return 'http://localhost:5000' + src;
        return 'https://www.thesearchbase.com' + src;
    };

    fetch(getLink("/api/static/widgets/chatbot/asset-manifest.json?NoCache=" + new Date().getTime()),
        {mode: 'no-cors'})
        .then(response => response.text())
        .then(manifest => {
            manifest = manifest.files ? JSON.parse(manifest) : {};

            // request and get assistant data
            const scriptTag = document.querySelector('script[data-name="tsb-widget"][data-id]');
            const isDirectLink = scriptTag.getAttribute('directLink') || '';
            const assistantID = scriptTag.getAttribute('data-id');
            const btnColor = scriptTag.getAttribute('data-circle') || '#1890ff';

            const s = document.createElement("script");
            s.src = getLink(`/api/static/widgets/chatbot${manifest.files['main.js']}`);
            s.async = true;
            s.defer = true;
            s.setAttribute('data-directLink', isDirectLink || '');
            s.setAttribute('data-name', 'tsb-widget');
            s.setAttribute('data-id', assistantID);
            s.setAttribute('data-circle', btnColor);
            s.setAttribute("id", "oldBotScript");

            document.body.appendChild(s);

            const l = document.createElement("link");
            l.href = getLink(`/api/static/widgets/chatbot${manifest.files['main.css']}`);
            l.type = "text/css";
            l.rel = "stylesheet";
            document.getElementsByTagName("head")[0].appendChild(l);
            // resolve(manifest ? JSON.parse(manifest) : {})
        }).catch((error) => {
        // reject(error)
    });
}

main();
