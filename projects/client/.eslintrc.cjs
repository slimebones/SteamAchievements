module.exports = {
  parser: "@typescript-eslint/parser",
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  plugins: [
    "@typescript-eslint",
    "unused-imports"
  ],
  parserOptions: {
    project: "./tsconfig.json",
  },
  rules: {
    "indent": "off",
    "prefer-const": "off",
    "@typescript-eslint/object-curly-spacing": [
      "off"
    ],
    "@typescript-eslint/strict-boolean-expressions": [
      "error",
      {
        "allowString": false,
        "allowNumber": false
      }
    ],
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": ["off"],

    // enforce only-typed declarations
    // https://stackoverflow.com/a/75207777/14748231
    "@typescript-eslint/no-inferrable-types": "off",

    "@typescript-eslint/no-explicit-any": "off",
    "@typescript-eslint/no-empty-function": "off",
    "@typescript-eslint/no-empty-interface": "off",
    "@typescript-eslint/no-non-null-assertion": "off",
    "no-empty": "off",
    "@typescript-eslint/typedef": [
        "off"
    ],

    // https://github.com/typescript-eslint/typescript-eslint/blob/main/packages/eslint-plugin/docs/rules/explicit-function-return-type.md
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/explicit-member-accessibility": "error",
    semi: ["error", "always"],
    "brace-style": ["error", "allman", { "allowSingleLine": true}],
    quotes: ["error", "double"],
    "max-len": ["error", {"code": 79}],
    "unused-imports/no-unused-imports": "error",
    // put semicolon at the end of a member (mainly for an interface member)
    // https://stackoverflow.com/a/65388500/14748231
    "@typescript-eslint/member-delimiter-style": [
      "error",
      {
          "multiline": {
              "delimiter": "semi",
              "requireLast": true
          },
          "singleline": {
              "delimiter": "semi",
              "requireLast": false
          }
      }
    ]
  },
  settings: {
    "svelte3/typescript": () => require("typescript"), // pass the TypeScript package to the Svelte plugin
    // OR
    "svelte3/typescript": true, // load TypeScript as peer dependency
    // ...
  }
};
