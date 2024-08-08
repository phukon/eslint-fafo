const { ESLint } = require('eslint');

(async function main() {
  const eslint = new ESLint();
  const results = await eslint.lintFiles(['samples/**/*.jsx']);
  const transformedData = results.map(({ source, ...rest }) => rest);

  console.log(`🎂 <<<start ${JSON.stringify(transformedData)} >>>end`);

  if (results.some((result) => result.errorCount > 0)) {
    console.error('ESLint errors found:');
    process.exit(1);
  } else {
    console.log('No ESLint errors found.');
  }
})();
