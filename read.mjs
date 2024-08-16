import fs from 'fs'

function readJsonFile(filePath) {
  fs.readFile(filePath, 'utf-8', (err, data) => {
    if (err) {
      console.error('There was an error reading the file.', err)
    }

    try {
      const jsonArray = JSON.parse(data)
      // console.log(jsonArray)

      jsonArray.forEach(jsonStr => {
        const logEntry = JSON.parse(jsonStr)
        console.log(logEntry)
      })

    }catch (err) {
      console.error(err)
    }
  })
}

readJsonFile('logs.json')