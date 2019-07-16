const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const webpack = require('webpack');
// const CompressionPlugin = require('compression-webpack-plugin');
// const zopfli = require('@gfx/zopfli');


module.exports = {
    mode: "production", // enable many optimizations for production builds
    entry: {
        app: "./src/index.js"
    },
    output: {
        filename: "chatbot.js",
        sourceMapFilename: "chatbot.map"
    },
    optimization: {
        minimizer: [
            new UglifyJsPlugin({
                cache: true,
                parallel: true,
                uglifyOptions:{
                    output: {
                        comments: false, // remove comments
                    },
                    compress: {
                        loops: true,
                        unused: true,
                        dead_code: true, // big one--strip code that will never execute
                        drop_debugger: true,
                        conditionals: true,
                        evaluate: true,
                        drop_console: true, // strips console statements
                        sequences: true,
                        booleans: true,
                        if_return: true,
                        join_vars: true,
                    }
                },
            }),
        ],
    },
    devtool: "#source-map",
    plugins: [
        new webpack.BannerPlugin(
            `Copyright (C) TheSearchBase, Inc - All Rights Reserved
             Chatbot plugin Version 1.0.0 
             Written by TheSearchBase Engineering Team, March 2019
             `)
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }, {
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
                    {loader: "postcss-loader"}
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
                    {loader: "postcss-loader"}
                ]
            },
            {
                test: /\.less$/,
                use: [
                    {loader: "style-loader"},
                    {loader: "css-loader"},
                    {loader: "less-loader", options: {javascriptEnabled: true}}
                ]
            }
        ]
    }
};
