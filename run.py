from __future__ import annotations

from init import create_and_update_memory, DataType, load_pet_data
from pet_system_agent import pet_system_agent


def main():
    load_pet_data()
    print("\n********** Please ask any question about pet. ********** \n")
    loop()


def loop():
    history = []
    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip().lower() in ("quit", "exit"):
            break

        result = pet_system_agent.run_sync(user_input, message_history=history)

        print(f"""\n======================== Answer =======================\n{result.output}\n==========================End==========================\n""")
        create_and_update_memory(
            collection_name="ai-collection",
            update_data=[f"Question: {user_input}, Answer: {result.output}"],
            data_type=DataType.AI
        )


if __name__ == "__main__":
    main()
