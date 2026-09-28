"""Checks for deterministic local exercise retrieval."""

from src.rag import retrieve_exercises
from src.utils import load_exercises


def main():
    exercises = load_exercises()
    assert retrieve_exercises("squat", exercises)[0]["name"] == "Squat"
    assert retrieve_exercises("legs", exercises)[0]["body_part"] == "legs"
    assert retrieve_exercises("unknown", exercises) == []
    print("Passed exercise retrieval checks.")


if __name__ == "__main__":
    main()
