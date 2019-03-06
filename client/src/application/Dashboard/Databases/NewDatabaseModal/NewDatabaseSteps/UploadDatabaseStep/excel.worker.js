if ('function' === typeof importScripts) {
    const {protocol, port, hostname} = location;
    const colon = port ? ":" : "";
    const uri = protocol + '//' + hostname + colon + port;

    importScripts(`${uri}/static/xlsx/shim.min.js`);
    importScripts(`${uri}/static/xlsx/cpexcel.js`);
    importScripts(`${uri}/static/xlsx/jszip.js`);
    importScripts(`${uri}/static/xlsx/xlsx.js`);
}

//eslint-disable-next-line
self.addEventListener('message', (e) => {
    // MY CODE ***************************************************************
    const workbook = XLSX.read(e.data, {type: 'binary', cellDates: true});
    const first_worksheet = workbook.Sheets[workbook.SheetNames[0]];
    /* DO SOMETHING WITH workbook HERE */

    let sheet_to_json = XLSX.utils.sheet_to_json(first_worksheet);

    return postMessage({
        headers: sheet_to_json[0] ? Object.keys(sheet_to_json[0]) : null,
        data: sheet_to_json[1] ? sheet_to_json : null
    });
});