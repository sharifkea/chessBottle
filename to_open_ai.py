from openai import OpenAI

def to_ai(white,black):
  client = OpenAI()
  ai_content = "previous moves ( White moves: "+white+" Black moves: "+black+"). What will be your move? just give me your move."
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": " You are an chess player assistant, playing as black."},
      {"role": "user", "content": ai_content}
    ]
  )
  # Split the string into words
  words = completion.choices[0].message.content.split()
  # Get the last word
  last_word = words[-1]
  if '.' in last_word:
    last_word = last_word.replace('.', '')
  print(completion.choices[0].message.content)
  print(last_word)
  return last_word