import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question, Choice



class QuestionModelTests(TestCase):

    def test_str_method(self):
        """
        Test the __str__ method to ensure it returns the question text.
        """
        question = Question(question_text="What's new?")
        self.assertEqual(str(question), "What's new?")

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose pub_date is in the future.
        """
        future_date = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=future_date)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose pub_date is older than 1 day.
        """
        old_date = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=old_date)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose pub_date is within the last day.
        """
        recent_date = timezone.now() - datetime.timedelta(hours=23)
        recent_question = Question(pub_date=recent_date)
        self.assertIs(recent_question.was_published_recently(), True)




class ChoiceModelTests(TestCase):

    def setUp(self):
        """
        Set up a Question instance and associated Choice instance for testing.
        """
        # Create a sample Question
        self.question = Question.objects.create(
            question_text="What's new?",
            pub_date=timezone.now()
        )
        
        # Create a Choice linked to the Question
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Nothing much",
            votes=0
        )

    def test_choice_creation(self):
        """
        Test that a Choice instance can be created and is linked to the correct Question.
        """
        self.assertEqual(self.choice.choice_text, "Nothing much")
        self.assertEqual(self.choice.votes, 0)
        self.assertEqual(self.choice.question, self.question)

    def test_choice_string_representation(self):
        """
        Test the string representation of a Choice instance.
        """
        self.assertEqual(str(self.choice), "Nothing much")

    def test_choice_votes_default_to_zero(self):
        """
        Test that the default value for votes is zero.
        """
        new_choice = Choice.objects.create(
            question=self.question,
            choice_text="Another choice"
        )
        self.assertEqual(new_choice.votes, 0)

    def test_choice_related_to_question(self):
        """
        Test that a Choice is correctly linked to its Question and can be accessed via question.choice_set.
        """
        # Check that the question's choice_set includes the created choice
        self.assertIn(self.choice, self.question.choice_set.all())
        # Count choices related to this question
        self.assertEqual(self.question.choice_set.count(), 1)

    def test_votes_can_be_updated(self):
        """
        Test that the votes field can be updated correctly.
        """
        self.choice.votes += 1
        self.choice.save()
        updated_choice = Choice.objects.get(id=self.choice.id)
        self.assertEqual(updated_choice.votes, 1)
