import os
import json
import time

INPUT_PATH = "./data/messages"
OUTPUT_PATH = "./data/formatted_messages.json"

NOT_OLDER_THAN = 5 * 1000 * 60 * 60 * 24 * 365 # messages cant be older than ... in ms
CONVO_TIME_DIFFERENCE = 3 * 1000 * 60 * 60 # time in between messages to be a different comvo in ms

def create_convos(data):

  current_time = time.time() * 1000 # in ms

  # Create the convos:
  convos = []
  current_convo_timestamp = 0

  for message in reversed(data['messages'][:-1]):

    if message['timestamp_ms'] > current_time - NOT_OLDER_THAN:

      if 'content' in message.keys():

        if message['timestamp_ms'] - CONVO_TIME_DIFFERENCE > current_convo_timestamp: 
          # New convo

          convos.append([{
            'content': message['content'],
            'sender_name': message['sender_name'],
            }])
        
        else:
          # Current convo
          
          convos[-1].append({
            'content': message['content'],
            'sender_name': message['sender_name'],
            })
        
        current_convo_timestamp = message['timestamp_ms']

  return convos


def format_convos(convos):

  # Create the QnA format:
  QnAs = []

  for convo in convos:

    # convo = convos[index] # Remove!

    prev_sender = convo[0]['sender_name']
    answering = False

    if prev_sender == "Arno Van Eetvelde":

      QnAs.append({
        "instruction": "Answer messages as if you are Arno.",
        'input': "A: " + convo[0]['content'],
        'output': "",
      })
    
    else:

      QnAs.append({
        "instruction": "Answer messages as if you are Arno.",
        'input': "Q: " + convo[0]['content'],
        'output': "",
      })

    for message in convo[1:]:

      if answering:

        if message['sender_name'] == "Arno Van Eetvelde":

          QnAs[-1]['output'] += "\nA: " + message['content']

          prev_sender = message['sender_name']
        
        else:

          answering = False

          prev_context = QnAs[-1]['input'] + QnAs[-1]['output']

          QnAs.append({
            "instruction": "Answer messages as if you are Arno.",
            'input': prev_context + "\nQ: " + message['content'],
            'output': "",
          })

          prev_sender = message['sender_name']

      else:

        if prev_sender == "Arno Van Eetvelde":
          # I sent the previous message

          prev_sender = message['sender_name']

          if prev_sender == "Arno Van Eetvelde":

            QnAs[-1]['input'] += "\nA: " + message['content']
          
          else:

            QnAs[-1]['input'] += "\nQ: " + message['content']

        else:
          # Someone else sent the previous message

          if message['sender_name'] != "Arno Van Eetvelde":

            QnAs[-1]['input'] += "\nQ: " + message['content']

            prev_sender = message['sender_name']

          else:

            answering = True

            QnAs[-1]['input'] += "\nA: "

            QnAs[-1]['output'] += message['content']

            prev_sender = message['sender_name']
    
    if QnAs[-1]['output'] == '':
      QnAs = QnAs[:-1]

  return QnAs

def format_messages(input_folder):

  with open(os.path.join(input_folder, "message_1.json")) as f:
    data = json.load(f)
  
  convos = create_convos(data)

  formatted_convos = format_convos(convos)

  print(len(formatted_convos))

  old_data = []
  if os.path.exists(OUTPUT_PATH):
    with open(OUTPUT_PATH) as f:
      old_data = json.load(f)

  with open(OUTPUT_PATH, 'w') as f:
    json.dump(old_data + formatted_convos, f)


if __name__ == "__main__":

  for folder in os.listdir(INPUT_PATH):
    if folder == ".DS_Store":
      continue

    print(folder)
    format_messages(os.path.join(INPUT_PATH, folder))