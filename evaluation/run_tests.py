
from pathlib import Path
import sys

# ============================================================
# IMPORT PROJECT
# ============================================================

# Allow imports from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))



from agent import agent
from test_cases import TEST_CASES


#use python evaluation/run_tests.py to launch the tests 
# ============================================================
# CONFIGURATION
# ============================================================

# Number of tests to run
# Set to None to run all tests
MAX_TESTS = None


# ============================================================
# TOOL CALL EXTRACTION
# ============================================================

def get_tool_calls(result):
    """
    Extract all tool calls made by the agent.
    """

    tool_calls = []

    for message in result["messages"]:

        if hasattr(message, "tool_calls") and message.tool_calls:

            for call in message.tool_calls:

                tool_calls.append({
                    "name": call["name"],
                    "args": call.get("args", {})
                })

    return tool_calls


# ============================================================
# CHECK EXPECTED TOOLS
# ============================================================

def check_expected_tools(actual_tools, expected_tools):
    """
    Check that all expected tools were called.

    We do not require an exact order because the agent
    may legitimately call tools in a different order.
    """

    actual_names = [tool["name"] for tool in actual_tools]

    missing = []

    for expected in expected_tools:

        if expected not in actual_names:
            missing.append(expected)

    return missing


# ============================================================
# CHECK FORBIDDEN TOOLS
# ============================================================

def check_forbidden_tools(actual_tools, forbidden_tools):
    """
    Check that tools that should NOT be used were not called.
    """

    actual_names = [tool["name"] for tool in actual_tools]

    unexpected = []

    for forbidden in forbidden_tools:

        if forbidden in actual_names:
            unexpected.append(forbidden)

    return unexpected


# ============================================================
# CHECK EXPECTED METRIC
# ============================================================

def check_expected_metric(actual_tools, expected_metric):
    """
    Check that company_metrics was called with the
    expected metric.
    """

    for tool in actual_tools:

        if tool["name"] != "company_metrics":
            continue

        args = tool["args"]

        metric = args.get("metric")

        if metric == expected_metric:
            return True

    return False


# ============================================================
# CHECK EXPECTED TICKERS
# ============================================================

def check_expected_tickers(actual_tools, expected_tickers):
    """
    Check that the expected ticker symbols were used.

    This allows multiple calls to get_company_stock_info,
    which is useful when the user asks for multiple companies.
    """

    actual_tickers = []

    for tool in actual_tools:

        if tool["name"] != "get_company_stock_info":
            continue

        ticker = tool["args"].get("ticker")

        if ticker:
            actual_tickers.append(ticker.upper())

    missing = []

    for ticker in expected_tickers:

        if ticker.upper() not in actual_tickers:
            missing.append(ticker)

    return missing


# ============================================================
# GET FINAL RESPONSE
# ============================================================

def get_final_response(result):
    """
    Get the final AI response from the agent.
    """

    messages = result["messages"]

    for message in reversed(messages):

        # AIMessage normally has type == "ai"
        if getattr(message, "type", None) == "ai":

            content = getattr(message, "content", "")

            if content:
                return content

    return ""


# ============================================================
# RUN SINGLE TEST
# ============================================================

def run_test(test):
    """
    Run one evaluation test.
    """

    test_id = test["id"]
    scenario = test["scenario"]

    print("\n" + "=" * 70)
    print(f"TEST {test_id}: {scenario}")
    print("=" * 70)

    # --------------------------------------------------------
    # Get question
    # --------------------------------------------------------

    if "question" in test:

        questions = [test["question"]]

    elif "conversation" in test:

        questions = test["conversation"]

    else:

        print("ERROR: Test has no question or conversation.")
        return False

    # --------------------------------------------------------
    # Unique thread ID
    # --------------------------------------------------------

    # Each test gets its own thread so tests do not
    # accidentally share conversation state.
    thread_id = f"evaluation_test_{test_id}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    all_tool_calls = []
    final_response = ""

    # --------------------------------------------------------
    # Run conversation
    # --------------------------------------------------------

    try:

        for question in questions:

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                },
                config=config
            )

            # Collect tool calls from this turn
            tool_calls = get_tool_calls(result)

            all_tool_calls.extend(tool_calls)

            # Save latest final response
            final_response = get_final_response(result)

    except Exception as e:

        print(f"\nRUNTIME ERROR:")
        print(f"{type(e).__name__}: {e}")

        return False

    # --------------------------------------------------------
    # Get expected values
    # --------------------------------------------------------

    expected_tools = test.get("expected_tools", [])
    forbidden_tools = test.get("must_not_use", [])

    expected_metric = test.get("expected_metric")
    expected_tickers = test.get("expected_tickers")

    # --------------------------------------------------------
    # Check expected tools
    # --------------------------------------------------------

    missing_tools = check_expected_tools(
        all_tool_calls,
        expected_tools
    )

    # --------------------------------------------------------
    # Check forbidden tools
    # --------------------------------------------------------

    unexpected_tools = check_forbidden_tools(
        all_tool_calls,
        forbidden_tools
    )

    # --------------------------------------------------------
    # Check metric
    # --------------------------------------------------------

    metric_ok = True

    if expected_metric:

        metric_ok = check_expected_metric(
            all_tool_calls,
            expected_metric
        )

    # --------------------------------------------------------
    # Check tickers
    # --------------------------------------------------------

    missing_tickers = []

    if expected_tickers:

        missing_tickers = check_expected_tickers(
            all_tool_calls,
            expected_tickers
        )

    # --------------------------------------------------------
    # Determine result
    # --------------------------------------------------------

    passed = True

    if missing_tools:
        passed = False

    if unexpected_tools:
        passed = False

    if not metric_ok:
        passed = False

    if missing_tickers:
        passed = False

    # --------------------------------------------------------
    # Print details
    # --------------------------------------------------------

    print("\nQUESTION:")

    for question in questions:
        print(f"  {question}")

    print("\nEXPECTED TOOLS:")
    print(f"  {expected_tools}")

    print("\nACTUAL TOOL CALLS:")

    if all_tool_calls:

        for call in all_tool_calls:

            print(f"  {call['name']}")

            if call["args"]:
                print(f"    args: {call['args']}")

    else:

        print("  None")

    # --------------------------------------------------------
    # Tool validation results
    # --------------------------------------------------------

    if missing_tools:

        print("\nMISSING TOOLS:")
        print(f"  {missing_tools}")

    if unexpected_tools:

        print("\nUNEXPECTED TOOLS:")
        print(f"  {unexpected_tools}")

    if expected_metric:

        print("\nEXPECTED METRIC:")
        print(f"  {expected_metric}")

        if metric_ok:
            print("  Metric: PASS")
        else:
            print("  Metric: FAIL")

    if expected_tickers:

        print("\nEXPECTED TICKERS:")
        print(f"  {expected_tickers}")

        if missing_tickers:
            print(f"  Missing: {missing_tickers}")
        else:
            print("  Tickers: PASS")

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    print("\nFINAL RESPONSE:")
    print(final_response)

    # --------------------------------------------------------
    # Final status
    # --------------------------------------------------------

    print("\nRESULT:")

    if passed:

        print("  PASS")

    else:

        print("  FAIL")

    return passed


# ============================================================
# RUN ALL TESTS
# ============================================================

def main():

    tests = TEST_CASES

    if MAX_TESTS is not None:
        tests = tests[:MAX_TESTS]

    total = len(tests)
    passed = 0
    failed = 0

    print("=" * 70)
    print("AGENT EVALUATION")
    print("=" * 70)

    print(f"\nTests to run: {total}")

    # --------------------------------------------------------
    # Run tests
    # --------------------------------------------------------

    for test in tests:

        success = run_test(test)

        if success:
            passed += 1
        else:
            failed += 1

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"\nTotal:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if total > 0:

        score = (passed / total) * 100

        print(f"Score:  {score:.1f}%")

    # --------------------------------------------------------
    # Exit status
    # --------------------------------------------------------

    if failed > 0:

        print("\nSome tests failed.")

        return 1

    print("\nAll tests passed.")

    return 0


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    raise SystemExit(main())