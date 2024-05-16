import json

def update_viewed_by_details(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Iterate over each conversation
    for conversation in data:
        messages = conversation['messages']
        prev_sender = None

        # Iterate backwards through the messages to check for unviewed messages by the same sender
        for i in range(len(messages) - 1, -1, -1):
            if 'viewed_by' not in messages[i]:
                # Insert default viewed_by details if missing
                messages[i]['viewed_by'] = {
                    'viewer': 'UNREAD',
                    'view_timestamp': 'UNREAD'
                }
                prev_sender = messages[i]['sender']
            elif messages[i]['sender'] == prev_sender:
                # Check if the previous message was from the same sender and also missing viewed_by details
                if 'viewed_by' not in messages[i]:
                    messages[i]['viewed_by'] = {
                        'viewer': 'UNREAD',
                        'view_timestamp': 'UNREAD'
                    }

    # Save the updated JSON data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Set the path to your JSON file
file_path = "C:\\Users\\erikl\\Desktop\\TRASCRIPTNARJAN.json"
update_viewed_by_details(file_path)

print("Updated JSON file has been saved.")
