/* MathJax runs only on TeX delimiters and ignores source-code elements. */
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true
  },
  options: {
    skipHtmlTags: [
      "script",
      "noscript",
      "style",
      "textarea",
      "pre",
      "code",
      "math",
      "select",
      "option",
      "mjx-container"
    ]
  }
};
