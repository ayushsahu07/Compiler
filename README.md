### CODEON - Compiler

# Code Execution Web App

This is a Flask-based web application that allows users to execute Python, Java, C++, and C code directly from their browser. It supports input data for the code and provides compilation and execution results.

## Features

- **Multi-language Support**: Execute Python, Java, C++, and C code.
- **Input Handling**: Provide input data for the code execution.
- **Error Reporting**: Displays detailed compilation and runtime errors.
- **Secure Temporary Files**: Uses temporary files for secure and isolated code execution.
- **Responsive UI**: Comes with a simple and user-friendly web interface.

## Prerequisites

- Python 3.x
- Flask
- GCC (for C and C++ code)
- Java Development Kit (JDK) for Java code execution

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/CodeExecutionWebApp.git
   cd CodeExecutionWebApp
   ```

2. Install dependencies:

   ```bash
   pip install flask
   ```

3. Ensure GCC, G++, and JDK are installed on your system.

   - For Debian/Ubuntu:

     ```bash
     sudo apt update
     sudo apt install gcc g++ openjdk-11-jdk
     ```

   - For Windows, download and install [MinGW](http://www.mingw.org/) for GCC/G++ and [JDK](https://www.oracle.com/java/technologies/javase-downloads.html).

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`.

3. Choose the programming language tab and enter your code and optional input data.

4. Click "Run" to execute the code and view the output or errors.

## File Structure

- `app.py`: Main application logic.
- `templates/index.html`: Frontend HTML file for the user interface.
- `static/`: Static assets like CSS or JavaScript files.

## API Endpoints

- `GET /`: Renders the main web interface.
- `POST /runcode`: Executes Python code.
- `POST /runjava`: Compiles and executes Java code.
- `POST /runcpp`: Compiles and executes C++ code.
- `POST /runc`: Compiles and executes C code.

## Security Notes

- The application uses temporary files for code execution, ensuring minimal interference and easy cleanup.
- **Do not deploy this application in a production environment without sandboxing or other security mechanisms** to prevent malicious code execution.

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Thanks to the Python, Flask, GCC, G++, and Java communities for their amazing tools and documentation.
```

Feel free to replace placeholders like `yourusername` and customize sections as needed! Let me know if you want further changes.
