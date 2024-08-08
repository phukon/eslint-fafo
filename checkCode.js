const { ESLint } = require("eslint");

(async function main() {
  const eslint = new ESLint();
  const results = await eslint.lintFiles(["samples/**/*.jsx"]);
  console.log(`🎂 <<<start ${JSON.stringify(results)} >>>end`)

  if (results.some(result => result.errorCount > 0)) {
    console.error("ESLint errors found:");
    console.error(resultText);
    process.exit(1);
  } else {
    console.log("No ESLint errors found.");
  }
})();
