# Local System One AI Demo
This is a simple starter demo of a System One AI model running locally. It is intended to demonstrate the basic concepts 
used by System One models like [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and how you can
run them locally on your own machine. 

## Model Setup
1. Download and install [Ollama](https://ollama.com/) on your machine. (Note: Must be version 0.35 or greater)
2. Pull down the `nimble` model: `ollama pull nimble`
3. Start the Ollama server: `ollama serve`

## Running the Demo
1. Clone the repository
2. Copy `.env-example` to `.env` and fill in the required values.
3. Run `uv sync`
4. Start the app by running `uv run main.py --promptfile prompts/cube-rule-of-food.yml`

Note that the first time the model is called after load is kind of slow, but later calls are very fast.

## Running with Jev
Everything about this demo is 100% [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) compatible. If you have access to 
Jev and would like to try it out:
1. Copy the `.env-example` to `.env`
2. Comment out or remove the active lines for `Ollama`
3. Uncomment the `Jev` lines and fill in your API key.