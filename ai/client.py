import os
import time
from abc import ABC

from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient

from models import SystemOnePrompt


class SystemOneClient(ABC):
    """
    A client for interacting with a Typesafe Compatible API, specifically designed to handle System One style prompts and questions.
    """

    def __init__(self) -> None:
        """
        Initializes the SystemOneClient with a TypeSafeClient instance.
        """
        print("Connecting to model server...")
        load_dotenv()
        server_connection_time = time.perf_counter_ns()
        self.client = TypeSafeClient(
            api_key=os.environ["TYPESAFE_API_KEY"],
            model=os.environ["MODEL_NAME"],
            timeout=120.0)

        print("Server Connection Time (ms):", (time.perf_counter_ns() - server_connection_time) / 1000000)
        self._warm_up_model()


    def system_one(self, prompt: SystemOnePrompt) -> dict:
        """
        Sends a request to the System One API with the provided state and questions.
        :param prompt: The SystemOnePrompt containing the state and questions.
        :return: The response from the System One API as a dictionary.
        """
        return self.client.system_one(state=prompt.state, questions=prompt.questions)

    def _warm_up_model(self):
        """
        Warms up the model by sending a dummy request.
        """
        print("Warming up the model...")
        warmup_timer = time.perf_counter_ns()
        self.system_one(SystemOnePrompt("prompts/prompt.yml"))
        print("Model Warmup Time (ms):", (time.perf_counter_ns() - warmup_timer) / 1000000)