import openai
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def convert_to_gitlabci(circleci_config):
    # Set up OpenAI request
    prompt = f"Convert the following CircleCI configuration to GitlabCI:\n\n{circleci_config}\n\n---\n\n"
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Parse response and return GitlabCI configuration
    gitlabci_config = response.choices[0].text.strip()
    return gitlabci_config

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        circleci_config = request.form['circleci_config']
        gitlabci_config = convert_to_gitlabci(circleci_config)
        return render_template('index.html', gitlabci_config=gitlabci_config)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()