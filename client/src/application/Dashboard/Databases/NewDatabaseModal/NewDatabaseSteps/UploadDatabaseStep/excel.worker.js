if ('function' === typeof importScripts) {
    importScripts('http://localhost:5000/static/xlsx/shim.min.js');
    importScripts('http://localhost:5000/static/xlsx/cpexcel.js');
    importScripts('http://localhost:5000/static/xlsx/jszip.js');
    importScripts('http://localhost:5000/static/xlsx/xlsx.js');
}

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