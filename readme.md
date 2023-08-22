# AI-Powered SQL Query Generator with Flask

This is a Python Flask web application that leverages OpenAI's text generation capabilities to automatically generate SQL queries based on user prompts. The application takes a user input as a prompt, converts it into a SQL query, executes the query on a SQLite database, and returns the query results in JSON format.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- `virtualenv` (recommended)


Configuration
Create a config.py file in the project directory with your OpenAI API key:

# config.py
open_ai_api_key = "your_openai_api_key_here"


Running the Application
Make sure you are in the project directory and your virtual environment is activated.

Run the Flask application:

python main.py

The application will start locally and can be accessed at http://127.0.0.1:5000

How the Application Operates
The user supplies a prompt through the /query endpoint. This can be achieved either by submitting a GET request along with the user_input parameter or by employing a POST request which encompasses a JSON payload containing the user_input key.

The provided prompt serves as the basis for generating an SQL query via OpenAI's text generation API.

The produced SQL query undergoes refinement to ensure alignment with specific criteria and to exclude undesirable components.

The application establishes a connection with a SQLite database named mydatabase.db.

Execution of the generated SQL query occurs within the database, leading to the retrieval of query results.

The application processes the query results, converting the 'date' column into a datetime format and extracting the date component.

Processed outcomes are then transformed into JSON format prior to being delivered back to the user.

API Endpoint
Endpoint: /query
Methods: GET, POST
Parameters:

user_input: The prompt supplied by the user to generate the SQL query.
Note: When using the POST method, ensure that the user_input is included within the JSON payload.

Additional Notes
The Flask framework is utilized to craft the API and manage incoming requests.
Cross-Origin Resource Sharing (CORS) is activated using the flask_cors extension.
The generated SQL query undergoes refinement to meet specific criteria and avoid particular patterns.
Database connectivity is achieved through SQLAlchemy.
OpenAI's API is employed for text generation.

Contributors
Contributor: Gustavo Bramao.





