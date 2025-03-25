from flask import Flask, jsonify, request, render_template, send_from_directory
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/<filename>')
def get_data(filename):
    return send_from_directory('data', filename)

@app.route('/run_script')
def run_script():
    center_node = request.args.get('center_node', '')
    
    try:
        print(f"Running script with center_node: {center_node}")
        result = subprocess.run(['python', './scripts/similarity.py', center_node], capture_output=True, text=True, check=True)
        print(repr(result.stdout))
        return result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500
    except FileNotFoundError:
        return jsonify({'error': 'Python script not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)