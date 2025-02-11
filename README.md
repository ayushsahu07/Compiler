# Code Execution API Server

This project is a simple Express.js-based API server designed to execute code snippets in various programming languages (Python, Java, C++, and C) with input handling and secure execution features.

## Features
- Execute Python, Java, C++, and C code snippets.
- Handle user-provided input for code execution.
- Timeout mechanism to prevent long-running or hanging processes.
- Secure cleanup of temporary files and directories after execution.

## Getting Started

### Prerequisites
Ensure you have the following installed on your system:

- Node.js (>= 12.x)
- Python (>= 3.x)
- Java Development Kit (JDK)
- GCC (for C/C++ support)
- G++ (for C++ support)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `public/index.html` file for the root route if needed.

### Running the Server

```bash
node server.js
```

The server will start and listen on port `3000` by default.

### API Endpoints

#### 1. **Execute Python Code**
- **Endpoint:** `POST /runcode`
- **Request Body:**
  ```json
  {
    "code": "print('Hello World')",
    "input": "Optional user input"
  }
  ```
- **Response:**
  ```json
  {
    "output": "Hello World"
  }
  ```

#### 2. **Execute Java Code**
- **Endpoint:** `POST /runjava`
- **Request Body:**
  ```json
  {
    "code": "System.out.println('Hello World');",
    "input": "Optional user input"
  }
  ```
- **Response:**
  ```json
  {
    "output": "Hello World"
  }
  ```

#### 3. **Execute C++ Code**
- **Endpoint:** `POST /runcpp`
- **Request Body:**
  ```json
  {
    "code": "#include <iostream>\nint main() { std::cout << 'Hello World'; return 0; }",
    "input": "Optional user input"
  }
  ```
- **Response:**
  ```json
  {
    "output": "Hello World"
  }
  ```

#### 4. **Execute C Code**
- **Endpoint:** `POST /runc`
- **Request Body:**
  ```json
  {
    "code": "#include <stdio.h>\nint main() { printf('Hello World'); return 0; }",
    "input": "Optional user input"
  }
  ```
- **Response:**
  ```json
  {
    "output": "Hello World"
  }
  ```

### Project Structure
```
.
├── server.js  // Main server file
├── package.json
└── public     // Static files directory
```

## Security Considerations
- Temporary files and directories are cleaned up after execution.
- Execution timeout (5 seconds) to prevent resource exhaustion.
- Ensure proper input sanitization for production use.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements
- [Express.js](https://expressjs.com/) for the server framework.
- [Node.js Child Processes](https://nodejs.org/api/child_process.html) for handling code execution.
- [uuid](https://www.npmjs.com/package/uuid) for unique directory naming.

