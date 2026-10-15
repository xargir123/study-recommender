
from django.test import SimpleTestCase

from students.recommender import (
    predict_topic_status,
    get_recommendation,
)


class RecommenderTests(SimpleTestCase):

    def test_low_score_needs_practice(self):
        self.assertEqual(predict_topic_status(25), "Needs Practice")

    def test_middle_score_is_developing(self):
        self.assertEqual(predict_topic_status(60), "Developing")

    def test_high_score_is_strong(self):
        self.assertEqual(predict_topic_status(90), "Strong")

    def test_exact_score_boundaries(self):
        self.assertEqual(predict_topic_status(49), "Needs Practice")
        self.assertEqual(predict_topic_status(50), "Developing")
        self.assertEqual(predict_topic_status(74), "Developing")
        self.assertEqual(predict_topic_status(75), "Strong")

    def test_score_is_clamped_to_valid_range(self):
        self.assertEqual(predict_topic_status(-10), predict_topic_status(0))
        self.assertEqual(predict_topic_status(110), predict_topic_status(100))

    def test_unassessed_topic_recommendation(self):
        recommendation = get_recommendation("Not Assessed", "Arrays")
        self.assertIn("quiz", recommendation.lower())

    def test_recommendations_exist_for_all_topics(self):
        topics = ["Arrays", "Linked Lists", "Binary Trees"]
        statuses = ["Needs Practice", "Developing", "Strong"]

        for topic in topics:
            for status in statuses:
                with self.subTest(topic=topic, status=status):
                    recommendation = get_recommendation(status, topic)
                    self.assertTrue(recommendation.strip())

    def test_topic_recommendation_is_not_empty(self):
        recommendation = get_recommendation("Needs Practice", "Arrays")
        self.assertTrue(recommendation.strip())
