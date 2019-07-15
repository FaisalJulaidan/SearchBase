var webpack_dev = require("./scripts/webpack.configs/webpack.dev.config.js");
var webpack_prod = require("./scripts/webpack.configs/webpack.prod.config.js");

module.exports = (env, options) => {
    process.on('uncaughtException', function (err) {
        if (err.errno === 'EADDRINUSE')
            console.error("Error: There is a running app on same port:" + err.port);
        else
            console.log(err);
        process.exit(1);
    });



    if (options.mode === 'development')
        return webpack_dev;
    else
        return webpack_prod;
};

