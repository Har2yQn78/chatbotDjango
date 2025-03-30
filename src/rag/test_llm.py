from settings import init, Settings

init()

# Test 1: Check LLM response
def test_llm():
    try:
        response = Settings.llm.complete("What is 1+1? Answer in one word.")
        print("LLM Response:", response.text)
    except Exception as e:
        print(f"LLM Error: {str(e)}")


if __name__ == "__main__":
    test_llm()
