from llm import ask


def summarize(text):
    prompt = "Summarize this in 3 short bullet points:\n\n" + text
    return ask(prompt)


if __name__ == "__main__":
    sample = "Relay tracks tasks and sends a daily digest to the team."
    print(summarize(sample))
