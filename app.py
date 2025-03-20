from flask import Flask, jsonify, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_test.html')

@app.route('/run_script')
def run_script():
    user_input = request.args.get('input', '')
    
    try:
        result = subprocess.run(['python', 'your_script.py', user_input], capture_output=True, text=True, check=True)
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500
    except FileNotFoundError:
        return jsonify({'error': 'Python script not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)