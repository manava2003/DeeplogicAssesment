from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

def get_time_stories():
    try:
        response = requests.get("https://time.com")
        html = response.text

        pattern = re.compile(
            r'<h3[^>]*?>\s*<div[^>]*?>\s*<a[^>]*?href="([^"]+)"[^>]*?>\s*<span[^>]*?>(.*?)</span>',
            re.IGNORECASE
        )

        matches = pattern.findall(html)
        stories = []

        for match in matches[:6]:
            link = match[0].strip()
            title = re.sub(r'\s+', ' ', match[1]).strip()
            if not link.startswith("http"):
                link = "https://time.com" + link
            stories.append({
                "title": title,
                "link": link
            })

        return stories

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

@app.route('/getTimeStories', methods=['GET'])
def time_stories_api():
    stories = get_time_stories()
    if stories:
        return jsonify(stories)
    else:
        return jsonify({"error": "Failed to fetch or parse stories"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
