def incoming_data_extraction(data: dict) -> dict:
    try:
        if 'incoming_message' not in data or not data['incoming_message']:
            raise ValueError("incoming_message missing or empty")

        message = data['incoming_message'][0]
        context = message.get('context', {})
        if message.get('message_type','') == 'INTERACTIVE':
            if 'button_reply' in message.get('interactive_type',''):
                text=message.get('interactive_type',{}).get('button_reply','').get('title','')
            else:
                text=message.get('interactive_type',{}).get("list_reply",'').get('title','')
        else:
            text=message.get('text_type', {}).get('text', '') if message.get('text_type') else ''

        return {
            'context_message_id': context.get('message_id', ''),
            'context_ncmessage_id': context.get('ncmessage_id', ''),
            'from_number': message.get('from', ''),
            'from_name': message.get('from_name', ''),
            'message_id': message.get('message_id', ''),
            'message_type': message.get('message_type', ''),
            'received_at': message.get('received_at', ''),
            'text': text,
            'to_number': message.get('to', '')
        }
    except Exception as e:
        print("Failed to extract incoming message data:", e)
        # Instead of returning None, return empty dict with required keys
        return {
            'context_message_id': '',
            'context_ncmessage_id': '',
            'from_number': '',
            'from_name': '',
            'message_id': '',
            'message_type': '',
            'received_at': '',
            'text': '',
            'to_number': ''
        }
