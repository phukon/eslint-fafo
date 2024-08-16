import json

def parse_logs_by_message_id(log_file_path, message_id):
    with open(log_file_path, 'r') as file:
        logs = json.load(file)
    
    filtered_logs = [json.loads(log) for log in logs if json.loads(log).get('message_id') == message_id]
    return filtered_logs

# Example usage
log_file_path = 'logs.json'
message_id = 'rikriki'
filtered_logs = parse_logs_by_message_id(log_file_path, message_id)
print(filtered_logs[0]["extra"])
