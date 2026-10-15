
from sklearn.tree import DecisionTreeClassifier


# Sample training data.
# Each score is associated with a performance category.
X = [
    [10],
    [25],
    [40],
    [49],
    [50],
    [60],
    [70],
    [74],
    [75],
    [85],
    [95],
    [100],
]

y = [
    "Needs Practice",
    "Needs Practice",
    "Needs Practice",
    "Needs Practice",
    "Developing",
    "Developing",
    "Developing",
    "Developing",
    "Strong",
    "Strong",
    "Strong",
    "Strong",
]


# Create and train the Decision Tree model.
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)


def predict_topic_status(score):
    """
    Predict topic performance from a score between 0 and 100.
    """
    score = max(0, min(100, float(score)))
    prediction = model.predict([[score]])

    return prediction[0]


def get_recommendation(status, topic_name):
    """
    Generate a recommendation based on topic and performance.
    """

    recommendations = {
        "Arrays": {
            "Needs Practice": (
                "Review array indexing and traversal. "
                "Practice accessing and updating elements."
            ),
            "Developing": (
                "Practice searching, sorting, and solving "
                "basic array problems."
            ),
            "Strong": (
                "Try advanced array problems and compare "
                "different sorting algorithms."
            ),
        },
        "Linked Lists": {
            "Needs Practice": (
                "Review nodes and links. Practice drawing "
                "linked lists and tracing their connections."
            ),
            "Developing": (
                "Practice insertion, deletion, and "
                "traversal operations."
            ),
            "Strong": (
                "Solve advanced linked-list problems and "
                "compare singly and doubly linked lists."
            ),
        },
        "Binary Trees": {
            "Needs Practice": (
                "Review roots, parents, children, and leaf "
                "nodes. Practice identifying tree structures."
            ),
            "Developing": (
                "Practice preorder, inorder, and postorder "
                "tree traversal."
            ),
            "Strong": (
                "Try binary search tree operations and "
                "more challenging tree problems."
            ),
        },
    }

    if status == "Not Assessed":
        return (
            f"Take the {topic_name} quiz to assess "
            "your current understanding."
        )

    topic_recommendations = recommendations.get(topic_name, {})

    return topic_recommendations.get(
        status,
        "Review the lesson and practice more questions."
    )