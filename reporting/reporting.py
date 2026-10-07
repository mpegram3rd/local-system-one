from typesafe_sdk import NoulAnswer, ChoiceAnswer, ScoreAnswer, SystemOneResponse


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
