from __future__ import annotations

from init import create_and_update_memory, DataType
from pet_agent import load_pet_data
from pet_system_agent import pet_system_agent

def main():
    load_pet_data()
    print("Please input.\n")
    loop()

def loop():
    history = []
    while True:
        try:
            prompt = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.strip().lower() in ("quit", "exit"):
            break

        result = pet_system_agent.run_sync(prompt, message_history=history)

        print("\n======================== Answer =======================")
        print(result.output)
        print("==========================End==========================\n")
        create_and_update_memory(
            collection_name="ai-collection",
            update_data=[f"Question: {prompt}, Answer: {result.output}"],
            data_type=DataType.AI
        )

        # print(result.all_messages_json())


if __name__ == "__main__":
    main()
