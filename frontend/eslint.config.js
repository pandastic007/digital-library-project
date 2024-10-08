import globals from 'globals';
import pluginJs from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';

export default [
  { files: ['**/*.{js,mjs,cjs,vue}'] },
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  ...pluginVue.configs['flat/essential'],
];
module.exports = {
  parser: 'vue-eslint-parser',
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2018, // 或者你使用的 ECMAScript 版本
    ecmaFeatures: {
      jsx: false, // 如果你不需要 JSX 支持，可以设置为 false
    },
  },
  extends: ['eslint:recommended', 'plugin:vue/recommended'],
  rules: {
    // 你的自定义规则
  },
};
