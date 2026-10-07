import argparse
import time

from ai import SystemOneClient
from models import SystemOnePrompt
from reporting import report_responses


def get_prompt_file():
    """
    Parses command line arguments to get the prompt file path.
    :return: The path to the prompt file.
    """
    print('Loading Prompt....')
    parser = argparse.ArgumentParser(description="Process a single target file.")

    # Add the filename positional argument
    parser.add_argument("--promptfile",
                    type=str,
                    help="The path to the prompt you want to run",
                    required=False,
                    default="prompts/prompt.yml")

    # Parse the arguments
    args = parser.parse_args()

    return args.promptfile

def main():

    # Create a connection to the model server
    client = SystemOneClient()

    # Retrieve and transform the prompt file into a SystemOnePrompt object
    prompt_file = get_prompt_file()
    prompt = SystemOnePrompt(prompt_file)

    # Run the prompt against the model
    query_response = time.perf_counter_ns()
    response = client.system_one(prompt)
    query_response_time = (time.perf_counter_ns() - query_response) / 1000000

    # Report the responses and query timer
    report_responses(prompt.questions, response)
    print("Query response time (ms):", query_response_time)

if __name__ == "__main__":
    main()
