import os
import json
import time

PATH = "/Users/arno/Documents/Projecten/data/Messenger_may2023/messages"

NOT_OLDER_THAN = 5 * 1000 * 60 * 60 * 24 * 365 # messages cant be older than ... in ms
CONVO_TIME_DIFFERENCE = 3 * 1000 * 60 * 60 # time in between messages to be a different comvo in ms

current_time = time.time() * 1000 # in ms

with open(os.path.join(PATH, "leonardvanvlierberghe_2347736911995048/message_1.json")) as f:
  data = json.load(f)


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


# Create the QnA format:
QnAs = []

for convo in convos:

  # convo = convos[index] # Remove!

  prev_sender = convo[0]['sender_name']
  answering = False

  if prev_sender == "Arno Van Eetvelde":

    QnAs.append({
      'in': "A: " + convo[0]['content'],
      'out': "",
    })
  
  else:

    QnAs.append({
      'in': "Q: " + convo[0]['content'],
      'out': "",
    })

  for message in convo[1:]:

    if answering:

      if message['sender_name'] == "Arno Van Eetvelde":

        QnAs[-1]['out'] += "\nA: " + message['content']

        prev_sender = message['sender_name']
      
      else:

        answering = False

        prev_context = QnAs[-1]['in'] + QnAs[-1]['out']

        QnAs.append({ # TODO
          'in': prev_context + "\nQ: " + message['content'],
          'out': "",
        })

        prev_sender = message['sender_name']

    else:

      if prev_sender == "Arno Van Eetvelde":
        # I sent the previous message

        prev_sender = message['sender_name']

        if prev_sender == "Arno Van Eetvelde":

          QnAs[-1]['in'] += "\nA: " + message['content']
        
        else:

          QnAs[-1]['in'] += "\nQ: " + message['content']

      else:
        # Someone else sent the previous message

        if message['sender_name'] != "Arno Van Eetvelde":

          QnAs[-1]['in'] += "\nQ: " + message['content']

          prev_sender = message['sender_name']

        else:

          answering = True

          QnAs[-1]['in'] += "\nA: "

          QnAs[-1]['out'] += message['content']

          prev_sender = message['sender_name']
  
  if QnAs[-1]['out'] == '':
    QnAs = QnAs[:-1]

print(len(QnAs))