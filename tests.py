import json
  
questions_file = open('tests/test_questions_v0.json')
  
questions = json.load(questions_file)

name = input("What is the name for this test?\n")
print()

results = []

for q in questions:

    print(q['Q'])

    A = 'azer' # Generate answer
    print(A)

    score = None
    while score not in ['0', '1', '2', '3', '4', '5']:
        score = input("Score (0-5): ")

    results.append({
        "Q": q['Q'],
        "A": A,
        "Score": int(score),
    })

avg_score = 0
for r in results:
    avg_score += r['Score']
avg_score /= len(results)
print(avg_score)

with open(f'tests/results/{name}.json', 'w') as outfile:
    json.dump(results, outfile)