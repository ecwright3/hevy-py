#!/usr/bin/env python3
"""
Test runner script for the Hevy SDK
"""
import subprocess
import sys
import os
from pathlib import Path


def run_tests(test_type="all", coverage=False):
    """Run tests with specified configuration"""
    cmd = ["python", "-m", "pytest"]

    if test_type == "unit":
        cmd.append("tests/unit/")
    elif test_type == "integration":
        cmd.append("tests/integration/")
    else:
        cmd.append("tests/")

    if coverage:
        cmd.extend([
            "--cov=hevy_py",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml",
            "--cov-fail-under=80"
        ])

    # Add additional pytest options
    cmd.extend([
        "-v",
        "--tb=short"
    ])

    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)

    return result.returncode


def install_test_deps():
    """Install test dependencies"""
    print("Installing test dependencies...")
    cmd = [sys.executable, "-m", "pip", "install", "-e", ".[test]"]
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode == 0


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Run tests for Hevy SDK")
    parser.add_argument(
        "test_type",
        choices=["all", "unit", "integration"],
        default="all",
        nargs="?",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install test dependencies first"
    )

    args = parser.parse_args()

    if args.install_deps:
        if not install_test_deps():
            print("Failed to install test dependencies")
            sys.exit(1)

    # Check if HEVY_API_KEY is set for integration tests
    if args.test_type in ["all", "integration"]:
        if not os.getenv("HEVY_API_KEY"):
            print("Warning: HEVY_API_KEY environment variable not set.")
            print("Integration tests will be skipped.")
            if args.test_type == "integration":
                print("Set HEVY_API_KEY to run integration tests.")
                sys.exit(1)

    # Run tests
    exit_code = run_tests(args.test_type, args.coverage)

    if exit_code == 0:
        print("\n✅ All tests passed!")
        if args.coverage:
            print("Coverage report generated in htmlcov/ directory")
    else:
        print(f"\n❌ Tests failed with exit code: {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()