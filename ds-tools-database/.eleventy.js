module.exports = function(eleventyConfig) {
  // Copy assets folder to output
  eleventyConfig.addPassthroughCopy("src/assets");

  // Copy Fuse.js from node_modules for client-side search
  eleventyConfig.addPassthroughCopy({
    "node_modules/fuse.js/dist/fuse.min.js": "assets/js/fuse.min.js"
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    templateFormats: ["njk", "md", "html"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
