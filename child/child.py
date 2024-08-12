import json
from logger import get_logger
logger = get_logger()

def childFunction():
    logger.info("hit hit hit")
    with open('eslintLog.json', 'r') as file:
        data = json.load(file)

    for item in data:
        print(f"File Path 🎂: {item['filePath']}")
        if item['errorCount'] > 0:
            print(f"Errors in file {item['filePath']}:")
            for message in item['messages']:
                print(f"  - Line {message['line']}, Column {message['column']}: {message['message']}")

    total_errors = sum(item['errorCount'] for item in data)
    print(f"Total errors: {total_errors}")