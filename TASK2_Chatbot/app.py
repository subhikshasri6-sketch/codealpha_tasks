import streamlit as st
import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('stopwords')
faq_data = [
    {
        "question": "How do I track my order?",
        "answer": "You can track your order using the tracking link sent to your email or by visiting the My Orders section."
    },
    {
        "question": "Why is my package delayed?",
        "answer": "Delivery delays may occur due to weather conditions, high order volumes, or courier issues. Please check your tracking information for updates."
    },
    {
        "question": "Can I change my shipping address after ordering?",
        "answer": "You can change your shipping address only before the order has been shipped."
    },
    {
        "question": "Do you ship to my country?",
        "answer": "We offer international shipping to selected countries. Check the shipping information page for availability."
    },
    {
        "question": "How long will it take for my order to arrive?",
        "answer": "Standard delivery usually takes 3 to 7 business days depending on your location."
    },
    {
        "question": "What is your return policy?",
        "answer": "Products can be returned within 30 days of delivery if they meet our return conditions."
    },
    {
        "question": "How do I get a prepaid return label?",
        "answer": "You can request a prepaid return label through the Returns section in your account."
    },
    {
        "question": "When will I receive my refund?",
        "answer": "Refunds are usually processed within 5 to 7 business days after the returned item is received and inspected."
    },
    {
        "question": "Can I exchange an item for a different size?",
        "answer": "Yes, size exchanges are available depending on product availability."
    },
    {
        "question": "What should I do if my item arrives damaged?",
        "answer": "Please contact customer support immediately and provide photos of the damaged item."
    },
    {
        "question": "Can I cancel my order before it ships?",
        "answer": "Yes, orders can be canceled before they are dispatched from our warehouse."
    },
    {
        "question": "Why was my credit card declined?",
        "answer": "Your card may have been declined due to insufficient funds, incorrect details, or bank restrictions."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept credit cards, debit cards, UPI, net banking, and digital wallets."
    },
    {
        "question": "How do I apply a discount code?",
        "answer": "Enter your discount code during checkout in the promo code field and click Apply."
    },
    {
        "question": "Can I edit items in my order after placing it?",
        "answer": "Order modifications are possible only before the order enters processing."
    },
    {
        "question": "How do I choose the right size?",
        "answer": "Please refer to our size guide available on each product page for accurate measurements."
    },
    {
        "question": "Is this item back in stock soon?",
        "answer": "You can subscribe to back-in-stock notifications on the product page."
    },
    {
        "question": "How do I reset my account password?",
        "answer": "Click 'Forgot Password' on the login page and follow the instructions sent to your email."
    },
    {
        "question": "Are my personal and payment details secure?",
        "answer": "Yes, we use industry-standard encryption and secure payment gateways to protect your information."
    },
    {
        "question": "I didn't receive an order confirmation email. What should I do?",
        "answer": "Check your spam folder first. If you still cannot find it, contact customer support."
    },
    {
        "question": "I received the wrong item. How do I get the correct one?",
        "answer": "Contact customer support and we will arrange a replacement or return process."
    },
    {
        "question": "An item is missing from my package. Was it shipped separately?",
        "answer": "Some items may be shipped separately. Check your order details and tracking information."
    },
    {
        "question": "My tracking says Delivered, but I can't find my package.",
        "answer": "Please check with neighbors, building reception, or the courier service before contacting support."
    },
    {
        "question": "Why isn't the checkout page loading?",
        "answer": "Try clearing your browser cache, disabling extensions, or using a different browser."
    },
    {
        "question": "Where can I download my tax invoice?",
        "answer": "Tax invoices can be downloaded from the My Orders section after your order is completed."
    }
]
df = pd.DataFrame(faq_data)
questions = df["question"]
answers = df["answer"]
stop_words = set(stopwords.words("english"))
def preprocess(text):
    text = text.lower()
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )
    tokens = word_tokenize(text)
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]
    return " ".join(tokens)
processed_questions = questions.apply(preprocess)
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(
    processed_questions
)
def get_response(user_query):
    processed_query = preprocess(user_query)
    query_vector = vectorizer.transform(
        [processed_query]
    )
    similarity_scores = cosine_similarity(
        query_vector,
        faq_vectors
    )
    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_index]
    if best_score < 0.20:
        return "Sorry, I couldn't find a matching answer."
    return answers.iloc[best_match_index]
st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖"
)
st.title("🤖 E-Commerce FAQ Chatbot")
st.write(
    "Ask questions related to orders, shipping, payments, returns, refunds, and account management."
)
if "messages" not in st.session_state:
    st.session_state.messages = []
prompt = st.chat_input("Type your question here...")
if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    response = get_response(prompt)
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
