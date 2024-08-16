import json
from logger import get_logger

logger = get_logger()

def childFunction():
    logger.info("Starting childFunction", extra={"function": "childFunction"})
    try:
        with open('eslintLog.json', 'r') as file:
            data = json.load(file)
        logger.info("Successfully read eslintLog.json", extra={"file": "eslintLog.json"})
    except Exception as e:
        logger.error(f"Failed to read eslintLog.json: {str(e)}", extra={"file": "eslintLog.json"})
        return
    extra={
              "reranked_desc_filtered_file_contents": 2343,
              "reranked_code_filtered_file_contents": 324,
              "mapping": 23423,
          }
    logger.info("lol",extra=extra)

    for item in data:
        
        logger.info(f"Processing file: {item['filePath']}", extra={"file": item['filePath']})
        if item['errorCount'] > 0:
            logger.warning(f"Errors in file {item['filePath']}:", extra={"file": item['filePath']})
            for message in item['messages']:
                logger.warning(
                    f"  - Line {message['line']}, Column {message['column']}: {message['message']}",
                    extra={
                        "file": item['filePath'],
                        "line": message['line'],
                        "column": message['column'],
                        "ruleId": message.get('ruleId')
                    }
                )
    
    total_errors = sum(item['errorCount'] for item in data)
    logger.info(f"Total errors: {total_errors}", extra={"total_errors": total_errors})