# Import necessary libraries and modules
import json
import sqlite3
from printer import ColorPrinter as Printer  # For colored console output
from utils_database import Database                 # Database utilities
from apis_chat_gpt import gpt_3_5_turbo_0613        # ChatGPT API call
# from prompt_database import database_query_bot_setup       # Bot setup string
from prompt_ecommerceDB import database_query_bot_setup       # Bot setup
from func_descr_database_ecom import describe_get_info_from_database

# Establish a connection to the SQLite database
# database_connection = sqlite3.connect("./database.sqlite")
database_connection = sqlite3.connect("./ecommerce.db")
print("Database connection successful.")

# Instantiate a Database object with the established connection
database_handler = Database(database_connection)

# Fetch and print the schema of the database
# db_schema: str = str(database_handler.get_database_info())
db_schema: str = database_handler.get_database_schema()
print(db_schema)


def get_info_from_database(query) -> str:
    try:
        # Execute the query and convert the result to JSON format
        query_result = database_handler.execute(query)
        return json.dumps(query_result)
    except Exception as e:
        # Raise an exception if the query execution fails
        raise Exception(
            f"Error executing query: {e}, please try again, passing in a valid SQL query in string format as only argument."
        )


def ask_company_db(query):

    # Initial messages to send to the bot
    chat_messages = [
        {"role": "system", "content": database_query_bot_setup},
        {"role": "user", "content": query},
    ]

    # Specify the functions available for the bot to call
    bot_functions = [describe_get_info_from_database(db_schema)]

    # Get the bot's initial response
    initial_response = gpt_3_5_turbo_0613(
        chat_messages, bot_functions, function_call={
            "name": "get_info_from_database"}
    )
    initial_message = initial_response["choices"][0]["message"]
    chat_messages.append(initial_message)

    # Check if the bot is calling a function
    if initial_message.get("function_call"):
        # Specify the available function for the bot to call
        available_functions = {
            "get_info_from_database": get_info_from_database,
        }
        # Extract the function name and its arguments from the bot's response
        called_function_name = initial_message["function_call"]["name"]
        actual_function_to_call = available_functions[called_function_name]
        function_arguments = json.loads(
            initial_message["function_call"]["arguments"])

        # Call the function and append the result to the chat_messages list
        response_from_function = actual_function_to_call(**function_arguments)
        chat_messages.append(
            {
                "role": "function",
                "name": called_function_name,
                "content": response_from_function,
            }
        )

        # Get the next response from the bot
        current_response = gpt_3_5_turbo_0613(chat_messages, bot_functions)
        current_message = current_response["choices"][0]["message"]
        chat_messages.append(current_message)

    # Print the entire conversation history using the color printer utility
    Printer.color_print(chat_messages)

    # Return the bot's final message content
    return current_message["content"]


# Test the ask_company_db function with a sample query
# print(ask_company_db("What are the names of the 10 users who wrote the most reviews?"))

# 1. Find the top 5 products with the highest average scores.
# print(ask_company_db("What are the top 5 products with the highest average scores?"))

# 2. Identify reviews that are most frequently found helpful by other users.
# print(ask_company_db("Which reviews are considered most helpful by other users?"))

# 3. List the users who are most active in providing reviews.
# print(ask_company_db(
    # "Who are the top 10 users based on the number of reviews they've written?"))

# 4. For a given product, understand the distribution of scores over time.
# print(ask_company_db("How have scores for a particular product changed over time?"))

# 5. Identify reviews with the highest score given in the most recent month.
# print(ask_company_db("What are the top reviews with a score of 5 from the last month?"))
# 6. (Complex) Determine the names of users who have consistently given low scores (1 or 2 out of 5)
# to products that have an overall average score of 4 or above,
# and have written more than 20 reviews in total.
# print(ask_company_db("Who are the users that frequently rate highly rated products with low scores and have written more than 20 reviews?"))


# ecommerceDB questions:
print(ask_company_db("List of top 5 Clients and Their Total Spending"))
print(ask_company_db("List of top 5 Products with No Sales"))
print(ask_company_db("List of top 5 Employees and Their Total Shipments Handled"))
print(ask_company_db(
    "list of top 5 Clients who have made orders but haven't received any shipments yet"))
print(ask_company_db("list of Top 5 Products by Sales Volume"))

# print(ask_company_db("Which clients have contributed the most revenue in sales?"))
# print(ask_company_db("Which shipping method has the highest rate of on-time deliveries, and which product category is most frequently shipped using this method?"))
