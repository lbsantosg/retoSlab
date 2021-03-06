from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@mail.com', password='testpass'):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        """
        Test creating a new user with an email is sucessfull
        """
        email = "test@email.co"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test the email from a new user is normalized"""
        email = 'test@EMAIL.coM'
        user = get_user_model().objects.create_user(email, 'test124')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@mail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string respresentation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """
            Test that image is saved in the correct location
            Mock a value = any time we call the uuid for a function
            that is triggered from within our test it will change
            the value override the default behavior and just
            return the value ('test-uuid') instead. This allow us
            to reliably test how our function works.
        """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        # recipe image file path is the name of the function that
        # we'll create and then ist's going to accepto 2 params
        # 1. instance - not used
        # 2. image original name (we need to remove the prior .jpg
        #    and replace it with the uuid)
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        # f --> String interpolation, insert variables inside a string
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
