"""
app.py
Flask application template for the warm-up assignment

Students need to implement the API endpoints as specified in the assignment.
"""

from flask import Flask, request, jsonify, render_template
from starter_preprocess import TextPreprocessor
# import traceback
# from preprocess import TextPreprocessor


app = Flask(__name__)
preprocessor = TextPreprocessor()


@app.route('/')
def home():
    """Render a simple HTML form for URL input"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Text preprocessing service is running"
    })


@app.route('/api/clean', methods=['POST'])
def clean_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts a URL and returns cleaned text

    Expected JSON input:
        {"url": "https://www.gutenberg.org/files/1342/1342-0.txt"}

    Returns JSON:
        {
            "success": true/false,
            "cleaned_text": "...",
            "statistics": {...},
            "summary": "...",
            "error": "..." (if applicable)
        }
    """
    try:
        # TODO: Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        # TODO: Extract URL from the JSON
        url = data.get('url')
        if not url:
            return jsonify({
                "success": False,
                "error": "No URL provided in request"
            }), 400
        # TODO: Validate URL (should be .txt)
        if url.split(".")[-1] != "txt":
            return jsonify({
                "success": False,
                "error": "URL must point to a .txt file"
            }), 400

        # TODO: Use preprocessor.fetch_from_url()
        raw_text = preprocessor.fetch_from_url(url)

        # TODO: Clean the text with preprocessor.clean_gutenberg_text()
        cleaned_text = preprocessor.clean_gutenberg_text(raw_text)

        # TODO: Normalize with preprocessor.normalize_text()
        normalized_text = preprocessor.normalize_text(cleaned_text)

        # TODO: Get statistics with preprocessor.get_text_statistics()
        statistics = preprocessor.get_text_statistics(normalized_text)

        # TODO: Create summary with preprocessor.create_summary()
        summary = preprocessor.create_summary(normalized_text, num_sentences=3)

        # TODO: Return JSON response
        return jsonify({
            "success": True,
            "cleaned_text": normalized_text,
            "statistics": statistics,
            "summary": summary
        }), 200

        # return jsonify({
        #     "success": False,
        #     "error": "Not implemented yet - complete this for Part 3!"
        # }), 501
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    TODO: Implement this endpoint for Part 3

    API endpoint that accepts raw text and returns statistics only

    Expected JSON input:
        {"text": "Your raw text here..."}

    Returns JSON:
        {
            "success": true/false,
            "statistics": {...},
            "error": "..." (if applicable)
        }
    """
    try:
        # TODO: Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        # TODO: Extract text from the JSON
        text = data.get('text')
        if not text:
            return jsonify({
                "success": False,
                "error": "No text provided in request"
            }), 400

        # TODO: Get statistics with preprocessor.get_text_statistics()
        statistics = preprocessor.get_text_statistics(text)

        # TODO: Return JSON response
        return jsonify({
            "success": True,
            "statistics": statistics
        }), 200

        return jsonify({
            "success": False,
            "error": "Not implemented yet - complete this for Part 3!"
        }), 501

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

# Error handlers


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("🚀 Starting Text Preprocessing Web Service...")
    print("📖 Available endpoints:")
    print("   GET  /           - Web interface")
    print("   GET  /health     - Health check")
    print("   POST /api/clean  - Clean text from URL")
    print("   POST /api/analyze - Analyze raw text")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")

    app.run(debug=True, port=5000, host='0.0.0.0')
