import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse
# Create your tests here.


class QuestionModelTest(TestCase):
    def setUp(self):
        self.question = Question(
            question_text="Quien es el mejor Course Director de Platzi")

    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)

    def test_was_published_recently_with_present_question(self):
        """was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() - datetime.timedelta(hours=22)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)

    def test_was_published_recently_with_past_question(self):
        """was_published_recently returns False for question whose pub_date is in the future"""
        time = timezone.now() - datetime.timedelta(days=5)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)


def create_question(question_text, days):
    """"
        Create a question with the given "question_text", and published the given
        number of days offset to now (negative for questions, published in the past,
        positive for question that hace yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        """If no questions existe, an appropriate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        # status the response
        self.assertEqual(response.status_code, 200)
        # message for no data
        self.assertContains(response, "No pols are available")
        # verify the data structure empty
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_question(self):
        """
            Questions with a pub_date in the future aren't displayed on the indexpage
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
            Question with a ub_date in the past are displayed pn the index page
        """
        question = create_question("Past question", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [question])

    def test_future_question_and_past_question(self):
        """
            Even of both past and future question exist, only past question are displayed
        """
        past_question = create_question(
            question_text="Past question", days=-30)
        future_question = create_question(
            question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], past_question)

    def test_two_past_question(self):
        """
            The question index page may displayed multipled question
        """
        past_question1 = create_question(
            question_text="Past question 1", days=-30)
        past_question2 = create_question(
            question_text="Past question 2", days=-40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question1, past_question2])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
            The detail view of a question with a pub_date in the future
            returns a 404 error not found
        """
        future_question = create_question(
            question_text="Future question", days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
            The detail view of a question with a pub_date in the past
            displayed the question's text
        """
        past_question = create_question(
            question_text="Past question", days = -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
