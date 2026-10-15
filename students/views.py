
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import QuizAttempt, TopicScore
from .recommender import predict_topic_status, get_recommendation


# =========================
# DASHBOARD
# =========================

@login_required(login_url="students:login")
def dashboard(request):
    latest_attempt = QuizAttempt.objects.filter(
        student=request.user
    ).order_by("-created_at").first()

    topics = [
        {"name": "Arrays", "status": "Not Assessed", "score": None},
        {"name": "Linked Lists", "status": "Not Assessed", "score": None},
        {"name": "Binary Trees", "status": "Not Assessed", "score": None},
    ]

    completed_quizzes = QuizAttempt.objects.filter(
        student=request.user
    ).count()

    if latest_attempt:
        latest_topic_scores = {
            item.topic_name: item
            for item in latest_attempt.topic_scores.all()
        }

        for topic in topics:
            saved_score = latest_topic_scores.get(topic["name"])

            if saved_score:
                topic["score"] = saved_score.percentage
                topic["status"] = predict_topic_status(
                    saved_score.percentage
                )

            topic["recommendation"] = get_recommendation(
                topic["status"],
                topic["name"],
            )
    else:
        for topic in topics:
            topic["recommendation"] = get_recommendation(
                topic["status"],
                topic["name"],
            )

    # Calculate the student's actual average across all quiz attempts.
    student_attempts = QuizAttempt.objects.filter(student=request.user)
    average_score = None

    if completed_quizzes:
        total_percentage = sum(
            attempt.percentage for attempt in student_attempts
        )
        average_score = round(total_percentage / completed_quizzes)

    assessed_topics = [topic for topic in topics if topic["score"] is not None]
    weakest_topic = min(assessed_topics, key=lambda item: item["score"]) if assessed_topics else None
    strongest_topic = max(assessed_topics, key=lambda item: item["score"]) if assessed_topics else None

    # Keep a short, chronological score history for the dashboard trend chart.
    chart_attempts = list(reversed(list(
        QuizAttempt.objects.filter(student=request.user).order_by("-created_at")[:10]
    )))
    chart_data = [
        {
            "label": attempt.created_at.strftime("%b %d"),
            "score": attempt.percentage,
        }
        for attempt in chart_attempts
    ]

    student_name = request.user.get_full_name() or request.user.email or request.user.username
    context = {
        "student_name": student_name,
        "topics": topics,
        "total_topics": len(topics),
        "completed_quizzes": completed_quizzes,
        "average_score": average_score,
        "weakest_topic": weakest_topic,
        "strongest_topic": strongest_topic,
        "chart_data": chart_data,
    }

    return render(request, "students/dashboard.html", context)


# =========================
# QUIZ
# =========================

@login_required(login_url="students:login")
def quiz(request):
    questions = [
        # ARRAYS — 5 QUESTIONS
        {
            "id": "q1",
            "topic": "Arrays",
            "text": "What is the index of the first element in a Python list?",
            "options": [
                ("a", "0"),
                ("b", "1"),
                ("c", "-1"),
                ("d", "2"),
            ],
            "answer": "a",
            "explanation": "Python lists use zero-based indexing, so the first element has index 0.",
        },
        {
            "id": "q2",
            "topic": "Arrays",
            "text": "Which operation accesses an element using its position?",
            "options": [
                ("a", "Sorting"),
                ("b", "Indexing"),
                ("c", "Merging"),
                ("d", "Deleting"),
            ],
            "answer": "b",
            "explanation": "Indexing accesses an element at a specified position.",
        },
        {
            "id": "q3",
            "topic": "Arrays",
            "text": "What is the index of the last element in a Python list containing 5 elements?",
            "options": [
                ("a", "5"),
                ("b", "4"),
                ("c", "3"),
                ("d", "0"),
            ],
            "answer": "b",
            "explanation": "A list with 5 elements has indexes 0 through 4.",
        },
        {
            "id": "q4",
            "topic": "Arrays",
            "text": "Which operation arranges array elements in a particular order?",
            "options": [
                ("a", "Traversal"),
                ("b", "Searching"),
                ("c", "Sorting"),
                ("d", "Indexing"),
            ],
            "answer": "c",
            "explanation": "Sorting arranges elements in an order, such as ascending or descending.",
        },
        {
            "id": "q5",
            "topic": "Arrays",
            "text": "What is the typical time complexity of accessing an array element by index?",
            "options": [
                ("a", "O(1)"),
                ("b", "O(n)"),
                ("c", "O(n²)"),
                ("d", "O(log n)"),
            ],
            "answer": "a",
            "explanation": "Direct index access in a typical array takes constant time, O(1).",
        },

        # LINKED LISTS — 5 QUESTIONS
        {
            "id": "q6",
            "topic": "Linked Lists",
            "text": "What does a node in a basic linked list contain?",
            "options": [
                ("a", "Only an index"),
                ("b", "Data and a link"),
                ("c", "Only a sorting algorithm"),
                ("d", "Only a position number"),
            ],
            "answer": "b",
            "explanation": "A basic linked-list node stores data and a link to another node.",
        },
        {
            "id": "q7",
            "topic": "Linked Lists",
            "text": "What is the first node of a linked list commonly called?",
            "options": [
                ("a", "Tail"),
                ("b", "Leaf"),
                ("c", "Head"),
                ("d", "Root"),
            ],
            "answer": "c",
            "explanation": "The head reference identifies the first node in a linked list.",
        },
        {
            "id": "q8",
            "topic": "Linked Lists",
            "text": "Which operation visits the nodes in a linked list?",
            "options": [
                ("a", "Traversal"),
                ("b", "Compilation"),
                ("c", "Encryption"),
                ("d", "Sorting only"),
            ],
            "answer": "a",
            "explanation": "Traversal visits nodes, usually beginning at the head.",
        },
        {
            "id": "q9",
            "topic": "Linked Lists",
            "text": "In a singly linked list, what does the last node usually point to?",
            "options": [
                ("a", "The head in every case"),
                ("b", "The previous node"),
                ("c", "None"),
                ("d", "A random node"),
            ],
            "answer": "c",
            "explanation": "The next reference of the last node in a standard singly linked list is None.",
        },
        {
            "id": "q10",
            "topic": "Linked Lists",
            "text": "Which statement describes a linked list compared with a typical array?",
            "options": [
                ("a", "Every element must be stored next to the others in memory"),
                ("b", "Nodes connect using links or references"),
                ("c", "It cannot store data"),
                ("d", "It never uses memory references"),
            ],
            "answer": "b",
            "explanation": "Linked-list nodes are connected through references and need not occupy consecutive memory locations.",
        },

        # BINARY TREES — 5 QUESTIONS
        {
            "id": "q11",
            "topic": "Binary Trees",
            "text": "What is the topmost node of a binary tree called?",
            "options": [
                ("a", "Leaf"),
                ("b", "Root"),
                ("c", "Sibling"),
                ("d", "Edge"),
            ],
            "answer": "b",
            "explanation": "The root is the topmost node of a tree.",
        },
        {
            "id": "q12",
            "topic": "Binary Trees",
            "text": "What is the maximum number of children a binary-tree node can have?",
            "options": [
                ("a", "One"),
                ("b", "Two"),
                ("c", "Three"),
                ("d", "Four"),
            ],
            "answer": "b",
            "explanation": "A binary-tree node can have at most two children.",
        },
        {
            "id": "q13",
            "topic": "Binary Trees",
            "text": "What is a node with no children commonly called?",
            "options": [
                ("a", "Root"),
                ("b", "Parent"),
                ("c", "Leaf"),
                ("d", "Sibling"),
            ],
            "answer": "c",
            "explanation": "A leaf node has no children.",
        },
        {
            "id": "q14",
            "topic": "Binary Trees",
            "text": "Which traversal visits the root between the left and right subtrees?",
            "options": [
                ("a", "Preorder"),
                ("b", "Inorder"),
                ("c", "Postorder"),
                ("d", "Level-order only"),
            ],
            "answer": "b",
            "explanation": "Inorder traversal visits the left subtree, the root, and then the right subtree.",
        },
        {
            "id": "q15",
            "topic": "Binary Trees",
            "text": "In a binary search tree, values smaller than a node are typically placed in which subtree?",
            "options": [
                ("a", "Left subtree"),
                ("b", "Right subtree"),
                ("c", "Both subtrees in every case"),
                ("d", "Nowhere in the tree"),
            ],
            "answer": "a",
            "explanation": "In a standard binary search tree, smaller values are placed in the left subtree and larger values in the right, subject to the implementation's duplicate-value rule.",
        },
    ]

    if request.method == "POST":
        total_correct = 0
        answers = []
        topic_results = {}

        for question in questions:
            topic = question["topic"]

            if topic not in topic_results:
                topic_results[topic] = {
                    "correct": 0,
                    "total": 0,
                }

            topic_results[topic]["total"] += 1

            selected = request.POST.get(question["id"], "")
            is_correct = selected == question["answer"]

            if is_correct:
                total_correct += 1
                topic_results[topic]["correct"] += 1

            option_labels = dict(question["options"])

            selected_label = option_labels.get(
                selected,
                "No answer selected",
            )
            correct_label = option_labels[question["answer"]]

            answers.append({
                "id": question["id"],
                "topic": topic,
                "text": question["text"],
                "selected_label": selected_label,
                "correct_label": correct_label,
                "is_correct": is_correct,
                "explanation": question["explanation"],
            })

        topic_scores = []

        for topic_name, data in topic_results.items():
            percentage = round(
                data["correct"] / data["total"] * 100
            )

            topic_scores.append({
                "name": topic_name,
                "correct": data["correct"],
                "total": data["total"],
                "percentage": percentage,
            })

        overall_percentage = round(
            total_correct / len(questions) * 100
        )

        # Save this quiz under the currently logged-in student.
        attempt = QuizAttempt.objects.create(
            student=request.user,
            student_name=request.user.username,
            score=total_correct,
            total_questions=len(questions),
            percentage=overall_percentage,
        )

        # Save the scores for each topic.
        for topic_data in topic_scores:
            TopicScore.objects.create(
                attempt=attempt,
                topic_name=topic_data["name"],
                correct_answers=topic_data["correct"],
                total_questions=topic_data["total"],
                percentage=topic_data["percentage"],
            )

        result = {
            "score": total_correct,
            "total": len(questions),
            "percentage": overall_percentage,
            "topic_scores": topic_scores,
            "answers": answers,
        }

        public_questions = [
            {
                "id": question["id"],
                "topic": question["topic"],
                "text": question["text"],
                "options": question["options"],
            }
            for question in questions
        ]

        return render(
            request,
            "students/quiz.html",
            {
                "questions": public_questions,
                "result": result,
            },
        )

    public_questions = [
        {
            "id": question["id"],
            "topic": question["topic"],
            "text": question["text"],
            "options": question["options"],
        }
        for question in questions
    ]

    return render(
        request,
        "students/quiz.html",
        {"questions": public_questions},
    )


# =========================
# PERSONALIZED STUDY PLAN
# =========================

@login_required(login_url="students:login")
def study_plan(request):
    latest_attempt = QuizAttempt.objects.filter(
        student=request.user
    ).order_by("-created_at").first()

    topics = [
        {
            "name": "Arrays",
            "status": "Not Assessed",
            "score": None,
            "resource_title": "Python Lists — Official Tutorial",
            "resource_url": "https://docs.python.org/3/tutorial/introduction.html#lists",
            "recommendation": get_recommendation("Not Assessed", "Arrays"),
        },
        {
            "name": "Linked Lists",
            "status": "Not Assessed",
            "score": None,
            "resource_title": "Linked Lists — GeeksforGeeks",
            "resource_url": "https://www.geeksforgeeks.org/data-structures/linked-list/",
            "recommendation": get_recommendation("Not Assessed", "Linked Lists"),
        },
        {
            "name": "Binary Trees",
            "status": "Not Assessed",
            "score": None,
            "resource_title": "Binary Tree — GeeksforGeeks",
            "resource_url": "https://www.geeksforgeeks.org/binary-tree-data-structure/",
            "recommendation": get_recommendation("Not Assessed", "Binary Trees"),
        },
    ]

    if latest_attempt:
        saved_scores = {
            item.topic_name: item
            for item in latest_attempt.topic_scores.all()
        }

        for topic in topics:
            saved_score = saved_scores.get(topic["name"])

            if saved_score:
                topic["score"] = saved_score.percentage
                topic["status"] = predict_topic_status(
                    saved_score.percentage
                )
                topic["recommendation"] = get_recommendation(
                    topic["status"],
                    topic["name"],
                )

    study_tasks = {
        "Needs Practice": [
            "Review the basic concepts.",
            "Study worked examples.",
            "Answer 5 beginner practice questions.",
        ],
        "Developing": [
            "Review any mistakes from the quiz.",
            "Practice intermediate exercises.",
            "Answer 5 new questions without looking at notes.",
        ],
        "Strong": [
            "Review advanced concepts.",
            "Solve a challenging programming problem.",
            "Explain the topic in your own words.",
        ],
        "Not Assessed": [
            "Review the topic introduction.",
            "Study the basic examples.",
            "Take the quiz to check your understanding.",
        ],
    }

    for topic in topics:
        topic["tasks"] = study_tasks[topic["status"]]

    return render(
        request,
        "students/study_plan.html",
        {
            "topics": topics,
            "latest_attempt": latest_attempt,
        },
    )


# =========================
# PROGRESS TRACKING
# =========================

@login_required(login_url="students:login")
def progress(request):
    attempts = list(
        QuizAttempt.objects.filter(
            student=request.user
        ).order_by("-created_at")[:10]
    )

    # Display chart data from oldest attempt to newest.
    chart_attempts = list(reversed(attempts))

    if attempts:
        latest_score = attempts[0].percentage
        previous_score = (
            attempts[1].percentage if len(attempts) > 1 else None
        )
    else:
        latest_score = None
        previous_score = None

    if previous_score is None or latest_score is None:
        score_change = None
    else:
        score_change = latest_score - previous_score

    return render(
        request,
        "students/progress.html",
        {
            "attempts": attempts,
            "chart_attempts": chart_attempts,
            "latest_score": latest_score,
            "score_change": score_change,
        },
    )


# =========================
# LOGIN
# =========================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("students:dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("students:dashboard")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "students/login.html",
        {"form": form},
    )


# =========================
# REGISTRATION
# =========================

def register(request):
    if request.user.is_authenticated:
        return redirect("students:dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("students:dashboard")
    else:
        form = UserCreationForm()

    return render(
        request,
        "students/register.html",
        {"form": form},
    )


# =========================
# LOGOUT
# =========================

def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("students:login")
