import streamlit as st
import json
import sqlite3
from utils_database import Database
from apis_chat_gpt import gpt_3_5_turbo_0613

from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter


def get_colored_sql(sql: str) -> str:
    # Format the SQL
    formatter = HtmlFormatter(style='colorful')
    return highlight(sql, SqlLexer(), formatter)


def execute_query(query) -> str:
    try:
        query_result = database_handler.execute(query)
        return json.dumps(query_result)
    except Exception as e:
        raise Exception(
            f"Error executing query: {e}, please try again, passing in a valid SQL query in string format as only argument."
        )


def describe_get_info_from_database(fun_desc, schema):
    return {
        "name": "get_info_from_database",
        "description": function_description,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                        SQL query extracting info from the database to answer the user's question.
                        The database schema is as follows:
                        {schema}
                        The query should be returned in string format as a single command.
                        """,
                }
            },
            "required": ["query"],
        },
    }


def ask_a_question(query) -> str:
    chat_messages = [
        {"role": "system", "content": database_query_bot_setup},
        {"role": "user", "content": query},
    ]

    avaiable_bot_functions = [describe_get_info_from_database(
        function_description, db_schema)]

    # pass query to the bot, and get the bot's first response
    first_raw_response = gpt_3_5_turbo_0613(
        chat_messages, avaiable_bot_functions, function_call={
            "name": "get_info_from_database"}
    )

    first_response = first_raw_response["choices"][0]["message"]
    # Convert the "arguments" string to a dictionary
    arguments_dict = json.loads(first_response["function_call"]["arguments"])
    # Extract the SQL query
    sql_query = arguments_dict["query"]

    # Get the styles for our SQL and inject them to Streamlit
    formatter = HtmlFormatter(style='colorful')
    style_str = formatter.get_style_defs('.highlight')
    style_str += ".highlight { background: rgba(255, 255, 255, 0.10); font-size: 25px; }"
    st.markdown(f"<style>{style_str}</style>", unsafe_allow_html=True)
    colored_sql = get_colored_sql(sql_query)
    st.markdown(colored_sql, unsafe_allow_html=True)

    # add the response to the chat_messages list
    chat_messages.append(first_response)

    # check if the bot is calling a function
    if first_response.get("function_call"):
        available_functions = {
            "get_info_from_database": execute_query,
        }
        called_function_name = first_response["function_call"]["name"]
        actual_function_to_call = available_functions[called_function_name]
        function_arguments = json.loads(
            first_response["function_call"]["arguments"])

        # execute the function by the bot
        response_from_function = actual_function_to_call(**function_arguments)

        # add the function execution response to the chat_messages list
        chat_messages.append(
            {
                "role": "function",
                "name": called_function_name,
                "content": response_from_function,
            }
        )

        current_response = gpt_3_5_turbo_0613(
            chat_messages, avaiable_bot_functions)
        current_message = current_response["choices"][0]["message"]
        chat_messages.append(current_message)
    return current_message["content"]


# Streamlit UI
st.title("Database Query Bot")
st.subheader("Select a database to query:")

database_to_use = st.radio(
    "", ["reviews (1 table)", "ecommerce (multiple tables)"])

if database_to_use == "ecommerce (multiple tables)":
    function_description = """Use this function to retrieve data from the ecommerce platform about orders, products, shipments, employees, clients, and sales.
        Reference entities using their unique identifiers from respective tables.
        Ensure accurate cross-referencing for comprehensive answers.
        Craft queries that provide clear and detailed information from the relevant tables."""
    database_query_bot_setup = (
        "You are a bot integrated within an ecommerce platform, holding access to extensive "
        "information about orders, products, shipments, employees, clients, and sales. "
        "Your primary function is to answer user queries accurately using the provided "
        "database, ensuring the user is informed comprehensively about any entity within the platform. "
        "Provide ample information and ensure clarity in your responses, considering the interconnectedness "
        "of data across multiple tables."
    )
    file_path = "./ecommerce.db"

elif database_to_use == "reviews (1 table)":
    function_description = """Use this function to answer questions about amazon customers' reviews and their helpfulness.
        If the user asks for a customer's name, this will refer to their ProfileName specifically.
        The 'HelpfulnessNumerator' is the number of 'helpful' votes the review has received.
        The 'HelpfulnessDenominator' is the total number 'helpful' or 'unhelpful' votes the review has received.
        The 'Score' column indicates the rating between 1 and 5 the user gave the product in their review.
        You are not to use the 'UserId' column in your queries, use the 'ProfileName' as identifier instead.
        Argument should be a fully formed SQL query."""
    database_query_bot_setup = (
        "You are a in company amazon bot providing information on customer "
        "review helpfulness data. You answer the users query in the most helpful "
        "way possible using the database and function provided. Provide plenty of "
        "information."
    )
    file_path = "./database.sqlite"

database_connection = sqlite3.connect(file_path)
database_handler = Database(database_connection)
db_schema: str = database_handler.get_database_schema()

# print the schema of the database
st.subheader(f"The schema of the {database_to_use} database is:")
schema_breakdown = db_schema.split('----------------------------------------')
for table_info in schema_breakdown:
    if "Table Name" in table_info:
        table_name = table_info.split("Table Name:")[
            1].split("Table Columns")[0].strip()
        st.subheader(f"Table Name: {table_name}")

        columns_info = table_info.split("Table Columns:")[1]
        for column_line in columns_info.split('\n'):
            if "field name" in column_line:
                field_name = column_line.split("field name:")[
                    1].split(",")[0].strip()
                field_type = column_line.split("field type:")[1].strip()
                st.write(f"- {field_name} ({field_type})")

query = st.text_input("Enter your question:")
if query:
    st.write(ask_a_question(query))
