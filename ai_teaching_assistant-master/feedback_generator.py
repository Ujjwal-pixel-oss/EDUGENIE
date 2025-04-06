import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from collections import Counter
import string
from typing import List, Dict, Any

# Download NLTK resources (run once)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def generate_feedback(grading_results: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """
    Generates personalized feedback based on grading results.

    Args:
        grading_results (dict): A dictionary containing students, scores, student_answers, and correct_answers.

    Returns:
        List[Dict[str, Any]]: A list of feedback dictionaries for each student.
    """
    feedback = []

    # Validate input
    if not grading_results or not grading_results.get('students'):
        raise ValueError("Invalid grading results provided.")

    for i in range(len(grading_results['students'])):
        student = grading_results['students'][i]
        score = grading_results['scores'][i]
        student_answer = grading_results['student_answers'][i]
        correct_answer = grading_results['correct_answers'][i]

        # Basic feedback based on score
        if score >= 90:
            assessment = "Excellent work!"
        elif score >= 70:
            assessment = "Good job, but there's room for improvement."
        else:
            assessment = "Let's review this material again."

        # Specific feedback by comparing answers
        specific_feedback = compare_answers(student_answer, correct_answer)

        # Construct full feedback
        full_feedback = {
            'student': student,
            'score': score,
            'assessment': assessment,
            'specific_feedback': specific_feedback,
            'suggestions': get_suggestions(score)
        }

        feedback.append(full_feedback)

    return feedback

def compare_answers(student_answer: str, correct_answer: str) -> str:
    """
    Generates specific feedback by comparing student and correct answers.

    Args:
        student_answer (str): The student's answer.
        correct_answer (str): The correct answer.

    Returns:
        str: Feedback on missing concepts or confirmation of completeness.
    """
    # Tokenize and clean both answers
    student_words = clean_text(student_answer)
    correct_words = clean_text(correct_answer)

    # Find missing concepts
    missing = set(correct_words) - set(student_words)

    if not missing:
        return "Your answer covered all the key points."
    else:
        return f"Consider including these concepts: {', '.join(missing)}"

def clean_text(text: str) -> List[str]:
    """
    Cleans and tokenizes text for comparison.

    Args:
        text (str): The input text.

    Returns:
        List[str]: A list of cleaned and tokenized words.
    """
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    return [word for word in tokens if word not in stop_words and word.isalpha()]

def get_suggestions(score: float) -> List[str]:
    """
    Provides learning suggestions based on the score.

    Args:
        score (float): The student's score.

    Returns:
        List[str]: A list of suggestions for improvement.
    """
    if score >= 90:
        return ["Challenge yourself with advanced materials on this topic."]
    elif score >= 70:
        return ["Review the main concepts.", "Practice with additional examples."]
    else:
        return [
            "Revisit the core materials on this topic.",
            "Schedule a meeting with your instructor for clarification.",
            "Try some practice exercises before moving on."
        ]