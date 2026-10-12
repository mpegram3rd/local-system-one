import yaml
from typesafe_sdk import Choice, Noul, Score


class SystemOnePrompt():
    """
    A class representing a System One style prompt, including its stat(context)
    and a collection of associated questions.
    """
    state: str
    questions: dict

    def __init__(self, prompt_file: str = "prompts/prompt.yml") -> None:
        """
        Initializes the Prompt object by reading the prompt from a YAML file.
        :param prompt_file: The path to the YAML file containing the prompt.
        """
        with open(prompt_file, 'r') as file:
            prompt_data = yaml.safe_load(file)
            self.state = prompt_data['state']
            self.questions = {}
            self._parse_questions(prompt_data['questions'])


    def _parse_questions(self, question_map: dict):
        """
        Parses a dictionary of questions based on the prompt file data and
        transforms them into a Typesafe API Style question set.
        :param question_map: A dictionary containing the questions to parse.
        :return: A Typesafe API Style question set as a dictionary.
    """
        for question in question_map:
            for key, value in question.items():
                if value['type'] == 'choice':
                    self.questions[key] = Choice(
                        instructions=value['question'],
                        criteria=value['criteria']
                    )
                elif value['type'] == 'noul':
                    self.questions[key] = Noul(
                        instructions=value['question']
                    )
                elif value['type'] == 'score':
                    self.questions[key] = Score(
                        instructions=value['question'],
                        criteria=value['criteria']
                    )
