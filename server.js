const express = require('express');
const { exec, spawn } = require('child_process');
const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const { v4: uuidv4 } = require('uuid');

const app = express();

// Middleware
app.use(express.json());
app.use(express.static('public')); // Serve static files from 'public' directory

// Root route - serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Helper function to create temp directory
async function createTempDir(prefix) {
    const tempPath = path.join(os.tmpdir(), `${prefix}_${uuidv4()}`);
    await fs.mkdir(tempPath, { recursive: true });
    return tempPath;
}

// Helper function to clean up temp files
async function cleanup(filePaths, dirPath) {
    try {
        for (const file of filePaths) {
            await fs.unlink(file);
        }
        if (dirPath) {
            await fs.rmdir(dirPath);
        }
    } catch (error) {
        console.error('Cleanup error:', error);
    }
}

// Python code execution endpoint
app.post('/runcode', async (req, res) => {
    const { code, input } = req.body;
    if (!code) {
        return res.json({ error: 'No code provided' });
    }

    const tempDir = await createTempDir('python');
    const tempFile = path.join(tempDir, 'program.py');

    try {
        await fs.writeFile(tempFile, code);
        
        const pythonProcess = spawn(os.platform() === 'win32' ? 'python' : 'python3', [tempFile]);
        let output = '';
        let error = '';

        if (input) {
            pythonProcess.stdin.write(input);
            pythonProcess.stdin.end();
        }

        pythonProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
            error += data.toString();
        });

        await new Promise((resolve, reject) => {
            pythonProcess.on('close', (code) => {
                resolve();
            });
            pythonProcess.on('error', reject);
            // Set timeout
            setTimeout(() => {
                pythonProcess.kill();
                reject(new Error('Execution timed out'));
            }, 5000);
        });

        await cleanup([tempFile], tempDir);
        res.json({ output: error ? `${output}\n\nError Output:\n${error}` : output });
    } catch (error) {
        await cleanup([tempFile], tempDir);
        res.json({ error: `Execution Error: ${error.message}` });
    }
});

// Java code execution endpoint
app.post('/runjava', async (req, res) => {
    const { code, input } = req.body;
    if (!code) {
        return res.json({ error: 'No code provided' });
    }

    const tempDir = await createTempDir('java');
    let className = 'Main';
    const match = code.match(/class\s+(\w+)/);
    if (match) {
        className = match[1];
    }

    const javaCode = className === 'Main' 
        ? `public class Main { public static void main(String[] args) { ${code} } }`
        : code;

    const sourceFile = path.join(tempDir, `${className}.java`);
    const classFile = path.join(tempDir, `${className}.class`);

    try {
        await fs.writeFile(sourceFile, javaCode);

        // Compile
        const compileProcess = spawn('javac', [sourceFile]);
        let compileError = '';

        compileProcess.stderr.on('data', (data) => {
            compileError += data.toString();
        });

        await new Promise((resolve, reject) => {
            compileProcess.on('close', (code) => {
                if (code !== 0) reject(new Error(compileError));
                resolve();
            });
        });

        // Execute
        const javaProcess = spawn('java', ['-classpath', tempDir, className]);
        let output = '';
        let runtimeError = '';

        if (input) {
            javaProcess.stdin.write(input);
            javaProcess.stdin.end();
        }

        javaProcess.stdout.on('data', (data) => {
            output += data.toString();
        });

        javaProcess.stderr.on('data', (data) => {
            runtimeError += data.toString();
        });

        await new Promise((resolve, reject) => {
            javaProcess.on('close', resolve);
            javaProcess.on('error', reject);
            setTimeout(() => {
                javaProcess.kill();
                reject(new Error('Execution timed out'));
            }, 5000);
        });

        await cleanup([sourceFile, classFile], tempDir);
        res.json({ output: runtimeError ? `${output}\n\nRuntime Error:\n${runtimeError}` : output });
    } catch (error) {
        await cleanup([sourceFile, classFile], tempDir);
        res.json({ error: `Execution Error: ${error.message}` });
    }
});

// C++ code execution endpoint
app.post('/runcpp', async (req, res) => {
    const { code, input } = req.body;
    if (!code) {
        return res.json({ error: 'No code provided' });
    }

    const tempDir = await createTempDir('cpp');
    const sourceFile = path.join(tempDir, 'program.cpp');
    const executableFile = path.join(tempDir, 'program' + (os.platform() === 'win32' ? '.exe' : ''));

    try {
        await fs.writeFile(sourceFile, code);

        // Compile
        const compileProcess = spawn('g++', [
            sourceFile,
            '-o', executableFile,
            '-Wall',
            '-Wextra',
            '-std=c++17'
        ]);

        let compileError = '';
        compileProcess.stderr.on('data', (data) => {
            compileError += data.toString();
        });

        await new Promise((resolve, reject) => {
            compileProcess.on('close', (code) => {
                if (code !== 0) reject(new Error(compileError));
                resolve();
            });
        });

        // Execute
        const executable = spawn(executableFile, [], {
            env: { ...process.env, LANG: 'en_US.UTF-8' }
        });

        let output = '';
        let runtimeError = '';

        if (input) {
            executable.stdin.write(input);
            executable.stdin.end();
        }

        executable.stdout.on('data', (data) => {
            output += data.toString();
        });

        executable.stderr.on('data', (data) => {
            runtimeError += data.toString();
        });

        await new Promise((resolve, reject) => {
            executable.on('close', resolve);
            executable.on('error', reject);
            setTimeout(() => {
                executable.kill();
                reject(new Error('Execution timed out'));
            }, 5000);
        });

        await cleanup([sourceFile, executableFile], tempDir);
        res.json({ output: runtimeError ? `${output}\n\nRuntime Error:\n${runtimeError}` : output });
    } catch (error) {
        await cleanup([sourceFile, executableFile], tempDir);
        res.json({ error: `Execution Error: ${error.message}` });
    }
});

// C code execution endpoint
app.post('/runc', async (req, res) => {
    const { code, input } = req.body;
    if (!code) {
        return res.json({ error: 'No code provided' });
    }

    const tempDir = await createTempDir('c');
    const sourceFile = path.join(tempDir, 'program.c');
    const executableFile = path.join(tempDir, 'program' + (os.platform() === 'win32' ? '.exe' : ''));

    try {
        await fs.writeFile(sourceFile, code);

        // Compile
        const compileProcess = spawn('gcc', [
            sourceFile,
            '-o', executableFile,
            '-Wall',
            '-Wextra',
            '-std=c11',
            '-pedantic',
            '-fstack-protector-all'
        ]);

        let compileError = '';
        compileProcess.stderr.on('data', (data) => {
            compileError += data.toString();
        });

        await new Promise((resolve, reject) => {
            compileProcess.on('close', (code) => {
                if (code !== 0) reject(new Error(compileError));
                resolve();
            });
        });

        // Execute
        const executable = spawn(executableFile, [], {
            env: { ...process.env, LANG: 'en_US.UTF-8' }
        });

        let output = '';
        let runtimeError = '';

        if (input) {
            executable.stdin.write(input);
            executable.stdin.end();
        }

        executable.stdout.on('data', (data) => {
            output += data.toString();
        });

        executable.stderr.on('data', (data) => {
            runtimeError += data.toString();
        });

        await new Promise((resolve, reject) => {
            executable.on('close', resolve);
            executable.on('error', reject);
            setTimeout(() => {
                executable.kill();
                reject(new Error('Execution timed out'));
            }, 5000);
        });

        await cleanup([sourceFile, executableFile], tempDir);
        res.json({ output: runtimeError ? `${output}\n\nRuntime Error:\n${runtimeError}` : output });
    } catch (error) {
        await cleanup([sourceFile, executableFile], tempDir);
        res.json({ error: `Execution Error: ${error.message}` });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

module.exports = app;