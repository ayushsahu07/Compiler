from flask import Flask, render_template, request, jsonify
import subprocess, traceback, os, re, tempfile, signal
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runcode', methods=['POST'])
def run_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        output = compile_and_execute(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

def compile_and_execute(code, input_data):
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        raise Exception(f"Compilation Error: {str(e)}")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code)

    try:
        python_exe = 'python' if os.name == 'nt' else 'python3'
        process = subprocess.Popen(
            [python_exe, temp_file_path],
            stdin=subprocess.PIPE if input_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate(input=input_data)
        os.unlink(temp_file_path)
        return f"\n{output}\n\nError Output:\n{error}" if error else output
    except Exception as e:
        os.unlink(temp_file_path)
        raise Exception(f"Execution Error: {str(e)}")

@app.route('/runjava', methods=['POST'])
def run_java_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        if not code.strip():
            return jsonify({'error': 'No code provided', 'traceback': 'Please provide Java code to execute'})
        output = compile_and_execute_java(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

def compile_and_execute_java(code, input_data):
    temp_dir = '/tmp/javatemp'
    os.makedirs(temp_dir, exist_ok=True)
    class_name = re.search(r'class\s+(\w+)', code).group(1) if re.search(r'class\s+(\w+)', code) else 'Main'
    temp_file_path = f'{temp_dir}/{class_name}.java'
    code = f'public class Main {{ public static void main(String[] args) {{ {code} }} }}' if class_name == 'Main' else code

    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(code)

    compile_process = subprocess.Popen(['javac', temp_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    _, compile_error = compile_process.communicate()
    if compile_process.returncode != 0:
        return f"Compilation Error:\n{compile_error}"

    execute_process = subprocess.Popen(
        ['java', '-classpath', temp_dir, class_name],
        stdin=subprocess.PIPE if input_data else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, runtime_error = execute_process.communicate(input=input_data)
    os.remove(temp_file_path)
    os.remove(f'{temp_dir}/{class_name}.class')
    return f"\n{output}\n\nRuntime Error:\n{runtime_error}" if runtime_error else output

@app.route('/runcpp', methods=['POST'])
def run_cpp_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        if not code.strip():
            return jsonify({'error': 'No code provided', 'traceback': 'Please provide C++ code to execute'})
        output = compile_and_execute_cpp(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

def compile_and_execute_cpp(code, input_data):
    temp_dir = tempfile.mkdtemp(prefix='cpp_')
    source_file = Path(temp_dir) / 'program.cpp'
    executable = Path(temp_dir) / 'program'

    with open(source_file, 'w') as temp_file:
        temp_file.write(code)

    compile_process = subprocess.Popen(
        ['g++', str(source_file), '-o', str(executable), '-Wall', '-Wextra', '-std=c++17'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    _, compile_error = compile_process.communicate(timeout=10)
    if compile_process.returncode != 0:
        return f"Compilation Error:\n{compile_error}"

    execute_process = subprocess.Popen(
        str(executable),
        stdin=subprocess.PIPE if input_data else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={'LANG': 'en_US.UTF-8'}
    )
    output, runtime_error = execute_process.communicate(input=input_data, timeout=5)
    os.unlink(source_file)
    os.unlink(executable)
    os.rmdir(temp_dir)
    return f"\n{output}\n\nRuntime Error:\n{runtime_error}" if runtime_error else output

@app.route('/runc', methods=['POST'])
def run_c_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        if not code.strip():
            return jsonify({'error': 'No code provided', 'traceback': 'Please provide C code to execute'})
        output = compile_and_execute_c(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

def compile_and_execute_c(code, input_data):
    temp_dir = tempfile.mkdtemp(prefix='c_')
    source_file = Path(temp_dir) / 'program.c'
    executable = Path(temp_dir) / 'program'

    with open(source_file, 'w') as temp_file:
        temp_file.write(code)

    compile_process = subprocess.Popen(
        ['gcc', str(source_file), '-o', str(executable), '-Wall', '-Wextra', '-std=c11', '-pedantic', '-fstack-protector-all'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    _, compile_error = compile_process.communicate(timeout=10)
    if compile_process.returncode != 0:
        return f"Compilation Error:\n{compile_error}"

    execute_process = subprocess.Popen(
        str(executable),
        stdin=subprocess.PIPE if input_data else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={'LANG': 'en_US.UTF-8'}
    )
    output, runtime_error = execute_process.communicate(input=input_data, timeout=5)
    os.unlink(source_file)
    os.unlink(executable)
    os.rmdir(temp_dir)
    return f"\n{output}\n\nRuntime Error:\n{runtime_error}" if runtime_error else output

if __name__ == '__main__':
    app.run(debug=True)