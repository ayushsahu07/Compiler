from flask import Flask, render_template, request, jsonify
import subprocess
import traceback
import os
import re
from pathlib import Path
import tempfile
import signal

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
        error_traceback = traceback.format_exc()
        return jsonify({
            'error': str(e),
            'traceback': error_traceback
        })

def compile_and_execute(code, input_data):
    # First try to compile the code to catch syntax errors
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        raise Exception(f"Compilation Error: {str(e)}")

    # Use tempfile module to handle temporary files cross-platform
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(code)

    try:
        # Determine python executable name based on platform
        python_exe = 'python' if os.name == 'nt' else 'python3'
        
        if input_data:
            # Create temporary input file
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as input_file:
                input_file_path = input_file.name
                input_file.write(input_data)

            # Use a unified approach for both Windows and Linux
            with open(input_file_path, 'r') as input_file:
                process = subprocess.Popen(
                    [python_exe, temp_file_path],
                    stdin=input_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
        else:
            # No input data case
            process = subprocess.Popen(
                [python_exe, temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        # Get output and error streams
        output, error = process.communicate()

        # Cleanup temporary files
        os.unlink(temp_file_path)
        if input_data:
            os.unlink(input_file_path)

        # Check for execution errors
        if error:
            return f"\n{output}\n\nError Output:\n{error}"
        return output

    except Exception as e:
        # Ensure cleanup even if an error occurs
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        if input_data and 'input_file_path' in locals() and os.path.exists(input_file_path):
            os.unlink(input_file_path)
        raise Exception(f"Execution Error: {str(e)}")


@app.route('/java')
def java():
    return render_template('index.html')

@app.route('/runjava', methods=['POST'])
def run_java_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        
        # Validate if code is provided
        if not code.strip():
            return jsonify({
                'error': 'No code provided',
                'traceback': 'Please provide Java code to execute'
            })
        
        output = compile_and_execute_java(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        error_traceback = traceback.format_exc()
        return jsonify({
            'error': str(e),
            'traceback': error_traceback
        })

def compile_and_execute_java(code, input_data):
    temp_dir = '/tmp/javatemp'
    temp_file_path = f'{temp_dir}/Main.java'
    
    # Create temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Extract class name or default to Main
        class_name_match = re.search(r'class\s+(\w+)', code)
        if class_name_match:
            class_name = class_name_match.group(1)
            # Rename the file to match the class name
            temp_file_path = f'{temp_dir}/{class_name}.java'
        else:
            class_name = 'Main'
            # Wrap code in a Main class if no class is defined
            code = f'public class Main {{ public static void main(String[] args) {{ {code} }} }}'
        
        # Write code to file
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(code)
        
        # Compile the code
        compile_process = subprocess.Popen(
            ['javac', temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        _, compile_error = compile_process.communicate()
        
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_error}"
        
        # Execute the compiled code
        java_command = ['java', '-classpath', temp_dir, class_name]
        
        execute_process = subprocess.Popen(
            java_command,
            stdin=subprocess.PIPE if input_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Provide input if available
        output, runtime_error = execute_process.communicate(input=input_data)
        
        # Clean up temporary files
        try:
            os.remove(temp_file_path)
            os.remove(f'{temp_dir}/{class_name}.class')
        except:
            pass
        
        # Combine output and errors
        result = ""
        if output:
            result += f"\n{output}\n"
        if runtime_error:
            result += f"\nRuntime Error:\n{runtime_error}"
        
        return result.strip() if result else "No output generated"
        
    except Exception as e:
        raise Exception(f"Error during execution: {str(e)}\n{traceback.format_exc()}")



@app.route('/cpp')
def cpp():
    return render_template('index.html')


@app.route('/runcpp', methods=['POST'])
def run_cpp_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        
        # Validate if code is provided
        if not code.strip():
            return jsonify({
                'error': 'No code provided',
                'traceback': 'Please provide C++ code to execute'
            })
        
        output = compile_and_execute_cpp(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        error_traceback = traceback.format_exc()
        return jsonify({
            'error': str(e),
            'traceback': error_traceback
        })

def compile_and_execute_cpp(code, input_data):
    # Create a temporary directory for compilation
    temp_dir = tempfile.mkdtemp(prefix='cpp_')
    source_file = Path(temp_dir) / 'program.cpp'
    executable = Path(temp_dir) / 'program'
    
    try:
        # Write code to file
        with open(source_file, 'w') as temp_file:
            temp_file.write(code)
        
        # Compile with all warnings and debug info
        compile_command = [
            'g++',
            str(source_file),
            '-o', str(executable),
            '-Wall',  # Enable all warnings
            '-Wextra',  # Enable extra warnings
            '-std=c++17'  # Use C++17 standard
        ]
        
        compile_process = subprocess.Popen(
            compile_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        _, compile_error = compile_process.communicate(timeout=10)  # 10 second compile timeout
        
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_error}"
        
        # Prepare execution environment
        env = os.environ.copy()
        env['LANG'] = 'en_US.UTF-8'  # Ensure consistent encoding
        
        # Execute the compiled program
        if input_data:
            execute_process = subprocess.Popen(
                str(executable),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            try:
                output, runtime_error = execute_process.communicate(input=input_data, timeout=5)  # 5 second runtime timeout
            except subprocess.TimeoutExpired:
                execute_process.kill()
                return "Execution Error: Program timed out after 5 seconds"
        else:
            execute_process = subprocess.Popen(
                str(executable),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            try:
                output, runtime_error = execute_process.communicate(timeout=5)  # 5 second runtime timeout
            except subprocess.TimeoutExpired:
                execute_process.kill()
                return "Execution Error: Program timed out after 5 seconds"
        
        # Prepare the result
        result = ""
        if output:
            result += f"\n{output}\n"
        if runtime_error:
            result += f"\nRuntime Error:\n{runtime_error}"
        
        if execute_process.returncode != 0:
            result += f"\nProgram exited with code {execute_process.returncode}"
            
        return result.strip() if result else "No output generated"
        
    except Exception as e:
        raise Exception(f"Error during execution: {str(e)}\n{traceback.format_exc()}")
    
    finally:
        # Cleanup temporary files
        try:
            if source_file.exists():
                source_file.unlink()
            if executable.exists():
                executable.unlink()
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Cleanup error: {str(e)}")





@app.route('/c')
def c():
    return render_template('index.html')


@app.route('/runc', methods=['POST'])
def run_c_code():
    try:
        code = request.json.get('code', '')
        input_data = request.json.get('input', None)
        
        # Validate if code is provided
        if not code.strip():
            return jsonify({
                'error': 'No code provided',
                'traceback': 'Please provide C code to execute'
            })
        
        output = compile_and_execute_c(code, input_data)
        return jsonify({'output': output})
    except Exception as e:
        error_traceback = traceback.format_exc()
        return jsonify({
            'error': str(e),
            'traceback': error_traceback
        })

def compile_and_execute_c(code, input_data):
    # Create a temporary directory for compilation
    temp_dir = tempfile.mkdtemp(prefix='c_')
    source_file = Path(temp_dir) / 'program.c'
    executable = Path(temp_dir) / 'program'
    
    try:
        # Write code to file
        with open(source_file, 'w') as temp_file:
            temp_file.write(code)
        
        # Compile with all warnings and debug info
        compile_command = [
            'gcc',
            str(source_file),
            '-o', str(executable),
            '-Wall',  # Enable all warnings
            '-Wextra',  # Enable extra warnings
            '-std=c11',  # Use C11 standard
            '-pedantic',  # Issue warnings for strict ISO C
            '-fstack-protector-all'  # Stack protection against buffer overflows
        ]
        
        compile_process = subprocess.Popen(
            compile_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        _, compile_error = compile_process.communicate(timeout=10)  # 10 second compile timeout
        
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_error}"
        
        # Prepare execution environment
        env = os.environ.copy()
        env['LANG'] = 'en_US.UTF-8'  # Ensure consistent encoding
        
        # Execute the compiled program
        if input_data:
            execute_process = subprocess.Popen(
                str(executable),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            try:
                output, runtime_error = execute_process.communicate(input=input_data, timeout=5)  # 5 second runtime timeout
            except subprocess.TimeoutExpired:
                execute_process.kill()
                return "Execution Error: Program timed out after 5 seconds"
        else:
            execute_process = subprocess.Popen(
                str(executable),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env
            )
            try:
                output, runtime_error = execute_process.communicate(timeout=5)  # 5 second runtime timeout
            except subprocess.TimeoutExpired:
                execute_process.kill()
                return "Execution Error: Program timed out after 5 seconds"
        
        # Check for common runtime errors
        if execute_process.returncode < 0:
            signal_num = -execute_process.returncode
            signal_name = signal.Signals(signal_num).name
            return f"Runtime Error: Program terminated by signal {signal_name} ({signal_num})"
        
        # Prepare the result
        result = ""
        if output:
            result += f"\n{output}\n"
        if runtime_error:
            result += f"\nRuntime Error:\n{runtime_error}"
        
        if execute_process.returncode != 0:
            result += f"\nProgram exited with code {execute_process.returncode}"
            
        return result.strip() if result else "No output generated"
        
    except Exception as e:
        raise Exception(f"Error during execution: {str(e)}\n{traceback.format_exc()}")
    
    finally:
        # Cleanup temporary files
        try:
            if source_file.exists():
                source_file.unlink()
            if executable.exists():
                executable.unlink()
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Cleanup error: {str(e)}")





# Add more routes and view functions for other HTML pages as needed

if __name__ == '__main__':
    app.run(debug=True)