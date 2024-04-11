from flask import Flask, request, jsonify
from flask_cors import CORS  # Enables cross-origin requests for the Flask app
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)
CORS(app)  # Apply CORS to all routes

def extract_faq_data(url):
    faq_data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    sections = soup.find_all('div', class_='faq-content-texts')

    for section in sections:
        heading_element = section.find('h3', class_='stellar-title__medium black')
        if heading_element:
            heading_text = heading_element.text.strip()
            answer_text = ' '.join([p.text.strip() for p in section.find_all('p', class_='stellar-body__medium black')])
            faq_data[heading_text] = answer_text

        questions = section.find_all('h4', class_='stellar-title__small black')
        if questions:
            for question in questions:
                question_text = question.text.strip()
                answer_texts = []
                next_element = question.find_next_sibling()
                while next_element and next_element.name != 'h4':
                    if next_element.name == 'p':
                        answer_texts.append(next_element.text.strip())
                    next_element = next_element.find_next_sibling()
                answer_text = ' '.join(answer_texts)
                faq_data[question_text] = answer_text

    return faq_data

def chatbot_response(user_input, faq_data):
    corpus = list(faq_data.keys())
    corpus.append(user_input)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(X[-1], X[:-1])
    idx = np.argmax(similarity)
    return faq_data[corpus[idx]]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['user_input'].lower()
    response = chatbot_response(user_input, faq_data)
    return jsonify({'answer': response})

# Load your FAQ data when the server starts
faq_data = extract_faq_data('https://www.hp.com/in-en/shop/faqs-content#delivery')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
