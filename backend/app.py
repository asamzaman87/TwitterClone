from flask import Flask

app = Flask(__name__)

# if __name__ == '__main__':
#     app.run()

import requests
API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

sen = input("Sentence: ")
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
    "inputs": sen,
    "parameters": {"candidate_labels": ["sports", "music", "fitness"]}
})
for i in output['scores']:
    if (i > .7):
        print(output['sequence'])