from __future__ import annotations
from typing import Any
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected

from init import load_pet_data
from pet_system_agent import pet_system_agent


def main(inputs: str) -> str:
    load_pet_data()

    try:
        return pet_system_agent.run_sync(inputs).output

    except Exception as e:
        raise NotImplementedError("")


# Evaluation dataset
pet_agent_dataset = Dataset[str, str, Any](
    cases=[
        Case(
            name="the_name_of_the_pet_for_rong",
            inputs="What is Rong's pet name?",
            expected_output="April",
            metadata={"type": "pet", "scope": "auth"},
            evaluators=(EqualsExpected(),),
        ),
        Case(
            name="the_color_of_the_pet_april",
            inputs="The color of the pet April?",
            expected_output="Orange, white, black",
            metadata={"type": "pet", "scope": "auth"},
            evaluators=(EqualsExpected(),),
        ),
        Case(
            name="the_name_of_the_pet_for_lan",
            inputs="What is Lan's pet name?",
            expected_output="711",
            metadata={"type": "pet", "scope": "auth"},
            evaluators=(EqualsExpected(),),
        ),
        Case(
            name="the_name_of_the_pet_for_nini",
            inputs="What is Nini's pet name?",
            expected_output="I don't know.",
            metadata={"type": "pet", "scope": "auth"},
            evaluators=(EqualsExpected(),),
        ),
    ],
)

if __name__ == "__main__":
    report = pet_agent_dataset.evaluate_sync(main)
    report.print()
