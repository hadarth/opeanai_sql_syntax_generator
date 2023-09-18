# "Id" INTEGER: A column named "Id" of data type INTEGER. This will hold integer values.

# "ProductId" TEXT: A column named "ProductId" of data type TEXT. This will hold textual data representing product IDs.

# "UserId" TEXT: A column named "UserId" of data type TEXT. This will hold textual data representing user IDs.

# "ProfileName" TEXT: A column named "ProfileName" of data type TEXT. This might store the profile names or usernames of the users.

# "HelpfulnessNumerator" INTEGER: A column of INTEGER data type that probably represents the number of people who found the review helpful.

# "HelpfulnessDenominator" INTEGER: A column of INTEGER data type that likely represents the total number of people who indicated whether they found the review helpful or not (including both helpful and not helpful).

# "Score" INTEGER: A column of INTEGER data type. This might indicate the rating or score given by the user to the product.

# "Time" INTEGER: A column of INTEGER type. This might represent the timestamp when the review was posted, often in UNIX epoch time format (seconds since January 1, 1970).

# "Summary" TEXT: A column of TEXT data type. This might hold a short summary or title of the review.

# "Text" TEXT: A column named "Text" of data type TEXT. This will likely store the detailed text content of the review.


def describe_get_info_from_database(schema):
    return {
        "name": "get_info_from_database",
        "description": """Use this function to retrieve data from the ecommerce platform about orders, products, shipments, employees, clients, and sales.
        Reference entities using their unique identifiers from respective tables.
        Ensure accurate cross-referencing for comprehensive answers.
        Craft queries that provide clear and detailed information from the relevant tables.""",
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
