const path = require("path");
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const webpack = require('webpack');

module.exports = {
    mode: "development", // enabled useful tools for development
    devServer: {
        contentBase: path.join(__dirname, "../../"),
        port: 9000,
        publicPath: '/dist',
        hot: true,
        inline: true,

    },
    // devtool: '#inline-source-map',
    // devtool: '#source-map',
    // devtool: 'eval',
    devtool: '#inline-source-map',
    cache: true,
    performance: {
        hints: false
    },
    optimization: {
        namedModules: true,
        namedChunks: true,
        flagIncludedChunks: false,
        occurrenceOrder: false,
        sideEffects: false,
        usedExports: false,
        concatenateModules: false,
        splitChunks: {
            hidePathInfo: false,
            minSize: 10000,
            maxAsyncRequests: Infinity,
            maxInitialRequests: Infinity,
        },
        noEmitOnErrors: false,
        checkWasmTypes: false,
        minimize: false,
        minimizer: [new UglifyJsPlugin({
            parallel: true,
            sourceMap: true
        })]
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
    ],
    watch: true,
    watchOptions: {
        poll: 1000 // Check for changes every second
    },
    entry: {
        app: "./src/index.js"
    },
    output: {
        filename: "chatbot.js",
        sourceMapFilename: "chatbot.map",
        pathinfo: true
    },
    module: {
        rules: [

            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            },
            {
                test: /^(?:(?!module).)*\.css$/,
                // exclude: /node_modules/,
                use: [
                    {loader: "style-loader"},
                    {
                        loader: "css-loader",
                        options: {
                            localIdentName: "[path]___[name]__[local]___[hash:base64:3]"
                        }
                    },
                    {loader: "postcss-loader"},
                ]
            },
            {
                test: /\.module\.css$/,
                // exclude: /node_modules/,
                use: [
                    {loader: "style-loader"},
                    {
                        loader: "css-loader",
                        options: {
                            modules: true,
                            localIdentName: "[path]___[name]__[local]___[hash:base64:5]"
                        }
                    },
                    {loader: "postcss-loader"},
                ]
            },
            {
                test: /\.less$/,
                use: [
                    {loader: "style-loader"},
                    {loader: "css-loader"},
                    {loader: "less-loader", options: {javascriptEnabled: true}}
                ]
            },

        ]
    }
};
