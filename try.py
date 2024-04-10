### the most correct code till now 
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def extract_faq_data(url):
    
    faq_data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Finding all sections
    sections = soup.find_all('div', class_='faq-content-texts')
    
    for section in sections:
       
        heading = section.find_previous('h1', class_='stellar-title__large black').text.strip()
        # Find all questions and answers within the section
        questions = section.find_all('h4', class_='stellar-title__small black')

        if not questions:
            continue
        for question in questions:
            question_text = question.text.strip()
            # Find all <p> tags following the question until the next question
            answer_texts = []
            next_element = question.find_next_sibling()
            while next_element and next_element.name != 'h4':
                if next_element.name == 'p':
                    answer_texts.append(next_element.text.strip())
                next_element = next_element.find_next_sibling()

            # Join all answer texts to form the answer
            answer_text = ' '.join(answer_texts)

            # Add question and answer pair to dictionary
            faq_data[question_text] = answer_text

        # Check for heading followed by answer
        heading_element = section.find_previous('h3', class_='stellar-title__medium black')
        if heading_element:
            heading_text = heading_element.text.strip()
            answer_text = ' '.join([p.text.strip() for p in section.find_all('p', class_='stellar-body__medium black')])

            # Add heading and answer pair to dictionary
            faq_data[heading_text] = answer_text

    return faq_data


# url = 'https://www.hp.com/in-en/shop/faqs-content#delivery'
# faq_data = extract_faq_data(url)

# for question, answer in faq_data.items():
#     print("Question:", question)
#     print("Answer:", answer)
#     print("-" * 50)


def chatbot_response(user_input, faq_data):
    # Combine questions and headings to create corpus
    corpus = list(faq_data.keys())
    corpus.append(user_input)

    # Vectorize corpus
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    # Calculate cosine similarity
    similarity = cosine_similarity(X[-1], X[:-1])

    # Get index of most similar question
    idx = np.argmax(similarity)

    return faq_data[corpus[idx]]


def main():
    
    url = 'https://www.hp.com/in-en/shop/faqs-content#delivery'
    faq_data = extract_faq_data(url)

    print("Bot: Hi there! How can I assist you today?")

    # Chat loop
    while True:
        user_input = input("You: ").lower()
        if user_input in ['bye', 'goodbye', 'exit', 'quit']:
            print("Bot: Goodbye! Have a great day.")
            break
        elif user_input in ['hello', 'hi', 'hey', 'what\'s up', 'good morning']:
            print("Bot: Hello! Ask me anything related to HP laptop FAQ's")
        else:
            response = chatbot_response(user_input, faq_data)
            print("Bot:", response)


if __name__ == "__main__":
    main()