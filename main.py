from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
import openai
import os
import config
import pandas as pd
import datetime
import re

# Set up config
openai.api_key = config.open_ai_api_key

# Create a connection to the database
database_path = 'mydatabase.db'
engine = create_engine(f'sqlite:///{database_path}')


def generate_oai_query(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.6,
        n=1,
        stop=None
    )

    # Extract the generated GA format from the API response
    response = response.choices[0].text.strip()

    return response


app = Flask(__name__)
CORS(app)


@app.route('/query', methods=['GET', 'POST'])
def execute_query():
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    elif request.method == 'POST':
        user_input = request.json.get('user_input')
    else:
        return jsonify({'error': 'Method not allowed'}), 405

    try:
        # Generate SQL query
        prompt = f"Convert the following '{user_input}' to a SQL query and take the first word after from the '{user_input}' for the 'SELECT' and also always include the 'date' in the 'SELECT', the table is is named 'mytable' and use only this syntax Date BETWEEN CURDATE() - INTERVAL x DAY AND CURDATE() and do not 'SELECT *'"

        sql_auto = generate_oai_query(prompt)
        iteration = 1

        while (('SELECT *' in sql_auto) or ('SUM' in sql_auto and not ('SUM' in user_input or 'sum' in user_input))) or sql_auto.strip() == 'SELECT date FROM mytable':
            print(f"Iteration {iteration}: {sql_auto}")
            sql_auto = generate_oai_query(prompt)
            iteration += 1

        print(f"Final SQL query: {sql_auto}")

        # Extract the value of x from the SQL query
        x = re.search(r"INTERVAL (\d+) DAY", sql_auto)
        if x:
            x = int(x.group(1))
        else:
            # Handle the case where the value of x couldn't be extracted
            x = 5  # Default value

        # Get the datetime values for the date range
        now = datetime.datetime.now()
        end_date = now.date()
        start_date = now - datetime.timedelta(days=x)
        start_date = start_date.date()

        # Replace the date condition in the generated SQL query with the appropriate date range
        if "BETWEEN CURDATE() - INTERVAL" in sql_auto:
            sql_query = sql_auto.replace(f"CURDATE() - INTERVAL {x} DAY", f"date('{start_date}')")
            sql_query = sql_query.replace("CURDATE()", f"date('{end_date}')")

        # Query the table
        query = sql_query
        df_query = pd.read_sql_query(query, engine)
        # Convert the 'date' column to datetime and extract the date component
        df_query['date'] = pd.to_datetime(df_query['date']).dt.date
        print(df_query)

        # Convert the dataframe to JSON
        result = df_query.to_dict(orient='records')

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
