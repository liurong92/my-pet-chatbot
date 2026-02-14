from __future__ import annotations

from init import create_and_update_memory, DataType, load_pet_data
from pet_system_agent import pet_system_agent


def test_chatbot():
    """测试聊天机器人功能"""
    # 加载数据
    load_pet_data()

    # 测试问题列表
    test_questions = [
        "April 是谁？",
        "April 喜欢什么？",
        "711 的主人是谁？",
        "有哪些宠物？",
    ]

    history = []

    print("\n" + "="*60)
    print("开始测试宠物聊天机器人")
    print("="*60 + "\n")

    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"问题: {question}")
        print(f"{'='*60}")

        try:
            result = pet_system_agent.run_sync(question, message_history=history)

            print(f"\n回答:\n{result.output}\n")

            # 保存到记忆
            create_and_update_memory(
                collection_name="ai-collection",
                update_data=[f"Question: {question}, Answer: {result.output}"],
                data_type=DataType.AI
            )

        except Exception as e:
            print(f"错误: {e}")

        print(f"{'='*60}\n")

    print("\n测试完成！\n")


if __name__ == "__main__":
    test_chatbot()
