import subprocess
import sys
import time


TESTS = [

    "tests.approval.test_approval_manager",

    "tests.approval.test_approval_policy",

    "tests.approval.test_approval_request",

    "tests.approval.test_audit_trail",

    "tests.approval.test_manual_override",

    "tests.approval.test_pause_resume"

]


def run(test):

    print("\n" + "=" * 70)

    print(f"Running {test}")

    print("=" * 70)

    start = time.time()

    result = subprocess.run(

        [

            sys.executable,

            "-m",

            test,

        ],

        capture_output=True,

        text=True,

    )

    duration = round(

        time.time() - start,

        2,

    )

    if result.returncode == 0:

        print(result.stdout)

        print(

            f"PASS ({duration}s)"

        )

        return True

    else:

        print(result.stdout)

        print(result.stderr)

        print(

            f"FAIL ({duration}s)"

        )

        return False


def main():

    print()

    print("=" * 70)

    print("Enterprise MCP Platform Offline Test Suite")

    print("=" * 70)

    passed = 0

    failed = 0

    start = time.time()

    for test in TESTS:

        ok = run(test)

        if ok:

            passed += 1

        else:

            failed += 1

    total = passed + failed

    duration = round(

        time.time() - start,

        2,

    )

    print()

    print("=" * 70)

    print("FINAL SUMMARY")

    print("=" * 70)

    print(

        f"Total Tests : {total}"

    )

    print(

        f"Passed      : {passed}"

    )

    print(

        f"Failed      : {failed}"

    )

    print(

        f"Success     : {round((passed/total)*100,2)}%"

    )

    print(

        f"Duration    : {duration}s"

    )

    print("=" * 70)

    if failed == 0:

        print()

        print("ALL TESTS PASSED")

        print()

    else:

        print()

        print("SOME TESTS FAILED")

        print()

        sys.exit(1)


if __name__ == "__main__":

    main()