from flask import Flask, request, jsonify, render_template
import csv
import random

app = Flask(__name__)

# Function to load data from CSV file
def load_data_from_csv(file_path, encoding='utf-8'):
    data = []
    with open(file_path, 'r', encoding=encoding) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            row = {key: value.strip() for key, value in row.items()}  
            data.append(row)
    return data

# Function to get response based on user input
def get_response(user_input, data):
    user_input_lower = user_input.lower()
    for item in data:
        if user_input_lower in item["Question"].lower():
            return item["Answer"]
    return random.choice(["I'm sorry, I don't have information on that topic.", "I don't understand. Can you rephrase your question?", "I'm still learning!"])

# Load data from CSV file
csv_file_path = 'chat.csv'  
data = load_data_from_csv(csv_file_path)

@app.route('/')
def index():
    return "Hey!"

@app.route('/chat', methods=['POST'])
def api_chat():
    try:
        user_input = request.json['user_input']
    except KeyError:
        return jsonify({'error': 'Missing "user_input" parameter'}), 400

    response = get_response(user_input, data)
    return jsonify({ 'response': response})

if __name__ == '__main__':
    app.run(debug=True)
