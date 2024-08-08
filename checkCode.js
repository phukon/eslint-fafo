const { ESLint } = require('eslint');
const fs = require('fs');
const path = require('path');

(async function main() {
  try {
    const eslint = new ESLint();
    const results = await eslint.lintFiles(['samples/**/*.jsx']);
    const transformedData = results.map(({ source, ...rest }) => rest);
    const outputFilePath = path.join(__dirname, 'eslintLog.json');
    const transformedDataString = JSON.stringify(transformedData, null, 2);

    if (results.some((result) => result.errorCount > 0)) {
      console.error('ESLint errors found:');
      console.log(`start>>>> ${transformedDataString} <<<<end`);

      fs.writeFile(outputFilePath, transformedDataString, (err) => {
        if (err) {
          console.error('Error writing file:', err);
          process.exit(1);
        } else {
          console.log(`Transformed data written to ${outputFilePath}`);
          process.exit(1);
        }
      });
    } else {
      console.log('No ESLint errors found.');
      fs.writeFile(outputFilePath, transformedDataString, (err) => {
        if (err) {
          console.error('Error writing file:', err);
        } else {
          console.log(`Transformed data written to ${outputFilePath}`);
        }
      });
    }
  } catch (error) {
    console.error('Unexpected error:', error);
    process.exit(1);
  }
})();
