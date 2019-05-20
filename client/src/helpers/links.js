export const getLink = (src) => {
    // include the colon if there is port number, which means localhost and not real server
    let colon = "";
    if (window.location.port !== "")
        colon = ":";


    const {protocol, port, hostname} = window.location;
    return protocol + '//' + hostname + colon + port + src;
};
