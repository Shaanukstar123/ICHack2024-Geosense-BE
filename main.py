from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# Sample data
articles_data = {
    "US": {"4.5", "Summary of an article related to the US."},
    "CA": {"3.2", "Summary of an article related to Canada."}
}

@app.route('/country_data', methods=['GET'])
def country_data():
    return jsonify(articles_data)
@app.route('/total_index', methods=['GET'])

def total_index():
    total_index = sum(article[0] for article in articles_data.values())
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"totalIndex": total_index, "datetime": current_datetime})

if __name__ == '__main__':
    app.run(debug=True)