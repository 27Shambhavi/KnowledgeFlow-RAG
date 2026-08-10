from app.pipeline.rag_pipeline import run_rag


# ============================================================
# CONFIGURATION
# ============================================================

NOT_FOUND_MESSAGE = (
    "Information not found in the uploaded documents."
)


# ============================================================
# IN-DOCUMENT TEST CASES
# ============================================================
#
# These questions MUST match information that exists
# in the documents currently uploaded to the knowledge base.
#

TEST_CASES = [
    {
        "question": "What is the closing balance?",
        "expected": "$4,250.00",
    },
    {
        "question": "What was the opening balance?",
        "expected": "$5,000.00",
    },
    {
        "question": "How much was the salary deposit?",
        "expected": "$1,000.00",
    },
]


# ============================================================
# OUT-OF-SCOPE TEST CASES
# ============================================================
#
# These questions should NOT be answerable from the
# uploaded documents.
#

OUT_OF_SCOPE_TESTS = [
    "What is the capital of France?",
    "Who is the president of the United States?",
    "What is the population of Japan?",
]


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):
    """
    Normalize text for simple answer comparison.
    """

    return (
        str(text)
        .lower()
        .replace(",", "")
        .replace("$", "")
        .strip()
    )


# ============================================================
# IN-DOCUMENT QUALITY TEST
# ============================================================

def run_quality_tests():

    print("\n")
    print("=" * 60)
    print("RAG QUALITY EVALUATION")
    print("=" * 60)

    passed = 0
    failed = 0

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        question = test_case["question"]
        expected = test_case["expected"]

        print("\n" + "-" * 60)
        print(f"Test     : {index}")
        print(f"Question : {question}")
        print(f"Expected : {expected}")

        try:

            result = run_rag(
                question
            )

            answer = result.get(
                "answer",
                "",
            )

            print(
                f"Actual   : {answer}"
            )

            # ------------------------------------------------
            # SIMPLE CONTAINMENT CHECK
            # ------------------------------------------------

            if normalize(expected) in normalize(answer):

                print(
                    "STATUS   : PASS"
                )

                passed += 1

            else:

                print(
                    "STATUS   : FAIL"
                )

                failed += 1

        except Exception as error:

            print(
                "STATUS   : ERROR"
            )

            print(
                f"Error    : {error}"
            )

            failed += 1


    # ========================================================
    # SUMMARY
    # ========================================================

    total = passed + failed

    print("\n")
    print("=" * 60)
    print("RAG QUALITY SUMMARY")
    print("=" * 60)

    print(
        f"Total    : {total}"
    )

    print(
        f"Passed   : {passed}"
    )

    print(
        f"Failed   : {failed}"
    )

    if total > 0:

        accuracy = (
            passed / total
        ) * 100

        print(
            f"Accuracy : {accuracy:.2f}%"
        )

    print("=" * 60)


# ============================================================
# OUT-OF-SCOPE TEST
# ============================================================

def run_out_of_scope_tests():

    print("\n")
    print("=" * 60)
    print("OUT-OF-SCOPE EVALUATION")
    print("=" * 60)

    passed = 0
    failed = 0

    for index, question in enumerate(
        OUT_OF_SCOPE_TESTS,
        start=1,
    ):

        print("\n" + "-" * 60)

        print(
            f"Test     : {index}"
        )

        print(
            f"Question : {question}"
        )

        try:

            result = run_rag(
                question
            )

            answer = result.get(
                "answer",
                "",
            )

            print(
                f"Actual   : {answer}"
            )

            # ------------------------------------------------
            # EXPECT NOT FOUND
            # ------------------------------------------------

            if normalize(
                NOT_FOUND_MESSAGE
            ) in normalize(answer):

                print(
                    "STATUS   : PASS"
                )

                passed += 1

            else:

                print(
                    "STATUS   : FAIL"
                )

                failed += 1

        except Exception as error:

            print(
                "STATUS   : ERROR"
            )

            print(
                f"Error    : {error}"
            )

            failed += 1


    # ========================================================
    # SUMMARY
    # ========================================================

    total = passed + failed

    print("\n")
    print("=" * 60)
    print("OUT-OF-SCOPE SUMMARY")
    print("=" * 60)

    print(
        f"Total    : {total}"
    )

    print(
        f"Passed   : {passed}"
    )

    print(
        f"Failed   : {failed}"
    )

    if total > 0:

        accuracy = (
            passed / total
        ) * 100

        print(
            f"Accuracy : {accuracy:.2f}%"
        )

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_quality_tests()

    run_out_of_scope_tests()