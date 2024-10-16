from query_data import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_monopoly_rules():
    assert query_and_validate(
        question="What are Breadcrumbs?",
        expected_response="""he navigation bar's breadcrumbs menu, located on the left side, provides users with a clear indication of their location within the
application. In figure 1.1, the content displayed on the left side consists of a home icon, "Helium Tank" (the package name), and "Confined
Spaces Hazard Assessment and Controls" (the form name). Clicking on the home icon will redirect the user to the dashboard page featuring
the package table. Selecting "Helium Tanks" will lead users to the package page. This enhances their awareness of their position within the
Confined Spaces application.""",
    )


def test_ticket_to_ride_rules():
    assert query_and_validate(
        question="Where can i find Important links drop down?)",
        expected_response="""The important links that used be located on the sidebar of the old app is now moved to the
top right of the application, only on form pages. This dropdown actives when a user
hovers or clicks on the “Important Links” text. It contains the same links that users are
familiar with""",
    )


def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="llama3.1:70b")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )
