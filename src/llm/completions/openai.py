from llm.utils.helpers import clean_text, get_azure_openai_client

def openai_completion(question: dict, model: str, context: str = None, chunks: list = None) -> str:
    client = get_azure_openai_client().get("client")
    # question_prompt = question["prompt"] + question["response_format"] + question.get("helper_text", "")
    question_prompt = question["prompt"]

    if chunks:
        completions = []

        for chunk in chunks:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that only uses the provided context to answer questions. If the context does not include the answer, respond with an empty string: """
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Based on the following context, answer the question: \n\n"
                            f"Context: {chunk} \n\n"
                            f"Question: {question_prompt} in the format described, and your response should only contain the answer, without any parts of the question."
                        )
                    }
                ],
                temperature=0.0
            )

            completions.append(clean_text(completion.choices[0].message.content or ""))

        completion_text = " ".join(completions)
        final_completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an assistant that only uses the provided context to answer questions. If the context is empty, respond with an empty string: "". 
                    If you are unable to answer the question, respond with an empty string. Enclose all responses into a list like so: ["answer1", "answer2", ""].
                    Remove "[" and "]" characters in entries inside the list."""
                },
                {
                    "role": "user",
                    "content": """The following context contains answers to the original question:
                    Original Question: {question_prompt} asked to different chunks of a document. Based on the context, answer the final question.
                    Context: {completion_text}
                    Final Question: Compile the context into a single word or few words, without losing the central idea, in the format described in the original question.
                    Respond without any parts of the original question and without empty strings in the response unless the context is empty."""
                }
            ],
            temperature=0.0
        )

        return clean_text(final_completion.choices[0].message.content or "")

    elif context:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an assistant that only uses the provided context to answer questions. If the context does not include the answer, respond with an empty string. 
                    Enclose all responses into a list like so: ["answer1", "answer2", ""]. Remove "[" and "]" characters in entries inside the list."""
                },
                {
                    "role": "user",
                    "content": (
                        f"Based on the following context, answer the question: \n\n"
                        f"Context: {context} \n\n"
                        f"Question: {question_prompt}. Your response should be a single word or few words, "
                        f"in the format described, and your response should only contain the answer, without any parts of the question, "
                        f"and without any nulls in the response unless the context is empty."
                    )
                }
            ],
            temperature=0.0
        )

        return clean_text(completion.choices[0].message.content or "")

    else:
        return 'ERROR: No context or chunks provided'
