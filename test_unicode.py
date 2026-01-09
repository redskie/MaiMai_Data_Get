from flask import Flask, jsonify

# Test Unicode encoding fix
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/test')
def test():
    return jsonify({
        'name': 'ＢＭＣ☆ＭＡＲＸ',
        'trophy': '舞神',
        'test': '日本語テスト'
    })

if __name__ == '__main__':
    with app.test_client() as client:
        response = client.get('/test')
        print("Response with JSON_AS_ASCII=False:")
        print(response.data.decode('utf-8'))
        
        import json
        data = json.loads(response.data)
        print("\nParsed data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
