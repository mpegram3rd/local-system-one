import argparse
import os
import time

import yaml
from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient, Score, Noul, Choice, SystemOneResponse, NoulAnswer, ChoiceAnswer, ScoreAnswer


def read_prompt(file_name: str = 'prompts/prompt.yml') -> dict:
    """
    Reads the prompt from a YAML file and returns it as a dictionary.
    :param file_name: The name of the YAML file to read.
    :return: A dictionary containing the contents of the YAML file.
    """
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)


def parse_questions(question_map: dict) -> dict:
    """
    Parses a dictionary of questions and returns a dictionary of question objects.
    :param question_map: A dictionary containing the questions to parse.
    :return: A dictionary of question objects keyed by question name to use in a System One API call
    """
    questions = {}
    for question in question_map:
        for key, value in question.items():
            if value['type'] == 'choice':
                questions[key] = Choice(
                    instructions=value['question'],
                    criteria=value['criteria']
                )
            elif value['type'] == 'noul':
                questions[key] = Noul(
                    instructions=value['question']
                )
            elif value['type'] == 'score':
                questions[key] = Score(
                    instructions=value['question'],
                    criteria=value['criteria']
                )
    return questions


def report_noul(answer: NoulAnswer):
    """
    Reports the answer to a noul question.
    :param answer: The answer to report.
    :return: None
    """
    score = answer.noul
    print(f"Answer: {score < 0.5 and 'No' or 'Yes'} - Score: {score}")

def report_choice(answer: ChoiceAnswer):
    """
    Reports the answer to a choice question.
    :param answer: The answer to report.
    :return: None
    """
    print("Options:")
    for prob_key, score in answer.probabilities.items():
        print(f" - Choice: {prob_key}, Probability: {score}")
    print(f"Answer: {answer.choice}")
    print(f"Confidence: {answer.confidence}")


def report_score(answer: ScoreAnswer):
    """
    Reports the answer to a score question.
    :param answer: The answer to report.
    :return: None
    """
    print("Value Range")
    score = answer.score
    closest_answer = ""
    smallest_diff = len(answer.legend)
    for legend_key, label in answer.legend.items():
        if abs(score - legend_key) < smallest_diff:
            closest_answer = label
            smallest_diff = abs(score - legend_key)
        print(f"- Key: {legend_key} - Label: {label}, ")
    print(f"Score: {score} - Closest Answer: {closest_answer}")
    print(f"Confidence: {answer.confidence}")


def report_responses(questions: dict, response: SystemOneResponse):
    """
    Reports the results for all the questions asked in the System One API call.
    :param questions: A dictionary of question objects keyed by question name.
    :param response: The System One response containing the answers.
    :return: None
    """
    print("=== SYSTEM ONE RESPONSE ===")
    print(f"Model: {response.model}")
    print(f"Token Usage - Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")
    print("=== ANSWERS ===")
    for name, answer in response.answers.items():
        print(f"Question: {questions[name].instructions}")
        print(f"Type: {answer.type}")
        if answer.type == 'noul':
            report_noul(answer)
        elif answer.type == 'choice':
            report_choice(answer)
        elif answer.type == 'score':
            report_score(answer)
        print("---------------------------")


def get_prompt_file():
    parser = argparse.ArgumentParser(description="Process a single target file.")

    # Add the filename positional argument
    parser.add_argument("--prompt",
                    type=str,
                    help="The path to the prompt you want to run",
                    required=False,
                    default="prompts/prompt.yml")

    # Parse the arguments
    args = parser.parse_args()

    return args.prompt

def main():
    load_dotenv()
    print('Loading Prompt....')
    prompt_file = get_prompt_file()
    prompt = read_prompt(prompt_file)
    state = prompt['state']
    questions = parse_questions(prompt['questions'])

    server_connection_time = time.perf_counter_ns()
    client = TypeSafeClient(
        api_key=os.environ["TYPESAFE_API_KEY"],
        model=os.environ["MODEL_NAME"],
        timeout=120.0)

    print("Server Connection Time (ms):", (time.perf_counter_ns() - server_connection_time) / 1000000)

    query_response = time.perf_counter_ns()
    response = client.system_one(
        state=state,
        questions=questions
    )
    query_response_time = (time.perf_counter_ns() - query_response) / 1000000

    report_responses(questions, response)
    print("Query response time (ms):", query_response_time)

if __name__ == "__main__":
    main()
