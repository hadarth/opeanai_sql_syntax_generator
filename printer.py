class ColorPrinter:
    """A utility class to print colored messages based on their roles."""

    # A mapping of message roles to their respective colors
    _color_mapping = {
        "system": "\033[33m",       # Yellow
        "user": "\033[32m",         # Green
        "function": "\033[34m",     # Blue
        "assistant": "\033[35m",    # Purple
        "header": "\033[36m",       # Cyan
        "undefined": "\033[37m",    # White
        "closing_tag": "\033[00m",  # Resets color to default
    }

    @staticmethod
    def _color_text_line(message) -> str:
        """Returns a colored message line based on the message role."""

        # Default color tag to close/reset the color
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]

        # Try to extract the role and the corresponding color from the message
        try:
            role = message["role"]
            color_open_tag = ColorPrinter._color_mapping[role]
        except KeyError:
            # Default color and role if not found in the message
            role = "undefined"
            color_open_tag = ColorPrinter._color_mapping[role]

        # Try to extract the content or function details from the message
        try:
            if message["content"]:
                message = message["content"]
            else:
                function_name = message["function_call"]["name"]
                function_args = message["function_call"]["arguments"]
                message = f"{function_name}({function_args})"
        except KeyError:
            # Default message if content or function details aren't present
            message = "undefined"

        return f"{color_open_tag}{role} : {message}{color_closing_tag}"

    @staticmethod
    def color_print(messages) -> None:
        """Prints a list of messages with their respective colors based on roles."""

        # Header and footer color
        cyan_open_tag = ColorPrinter._color_mapping["header"]
        color_closing_tag = ColorPrinter._color_mapping["closing_tag"]

        # Print the conversation history header
        print(
            f"\n{cyan_open_tag}###### Conversation History ######{color_closing_tag}")

        # Print each message in the provided messages list
        for message in messages:
            print(ColorPrinter._color_text_line(message))

        # Print the closing line
        print(f"{cyan_open_tag}##################################{color_closing_tag}\n")
