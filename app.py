from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/analyze_reviews', methods=['POST'])  # Ensure this line includes 'POST'
def analyze_reviews():
    data = request.json
    product_link = data.get('link')

    if not product_link:
        return jsonify({'review': 'No product link provided.'}), 400  # Bad Request if no link is provided

    try:
        # Make a request to the product link
        response = requests.get(product_link)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Simulating the review extraction (customize as per the product page)
        reviews = []
        for review in soup.find_all('span', {'class': 'review-text'}):
            reviews.append(review.get_text())

        # Example logic for analysis (this can be more complex)
        if reviews:
            analyzed_review = " ".join(reviews[:3])  # Sample: Take first 3 reviews
            return jsonify({'review': analyzed_review})
        else:
            return jsonify({'review': 'No reviews found.'}), 404  # Not Found if no reviews

    except requests.exceptions.HTTPError as http_err:
        return jsonify({'review': f'HTTP error occurred: {http_err}'}), 500  # Internal Server Error
    except Exception as e:
        return jsonify({'review': f'Error fetching reviews: {str(e)}'}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True)
