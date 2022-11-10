module.exports = {
    presets: [
        [
            '@babel/env',
            {
                useBuiltIns: 'entry',
                corejs: 3,
            },
        ],
    ],
    plugins: ['@babel/plugin-transform-runtime'],
};