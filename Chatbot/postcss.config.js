let path = require('path');
module.exports = {
    plugins: [
        require('autoprefixer'),
        require('postcss-autoreset')({
            reset: {
                margin: 0,
                // padding: 0,
                // borderRadius: 0,
                color: 'black',
                // all: 'initial',
                transition: 'none',
                fontFamily: 'inherit',
                fontSize: 'inherit',
            }
        }),
        require('postcss-initial'),
        require('postcss-import'),
        require('postcss-url'),
        require('postcss-preset-env')({
            browsers: 'last 2 versions',
            stage: 0,
        }),
        require('postcss-safe-important')({
            // options
            keepcomments: false // all the `no important` comments will be erased
        })

    ],
};