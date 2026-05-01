from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UsersApiTests(APITestCase):
	"""Test suite for Users CRUD API with database backend"""

	def test_create_user(self):
		"""Test creating a new user"""
		response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'john@example.com', 'age': 28},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('id', response.data)
		self.assertEqual(response.data['name'], 'John Doe')
		self.assertEqual(response.data['email'], 'john@example.com')
		self.assertEqual(response.data['age'], 28)
		
		# Verify user was saved to database
		self.assertTrue(User.objects.filter(email='john@example.com').exists())

	def test_create_user_rejects_invalid_email(self):
		"""Test that invalid email format is rejected"""
		response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'not-an-email', 'age': 28},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data)

	def test_create_user_rejects_duplicate_email(self):
		"""Test that duplicate email is rejected"""
		# Create first user
		self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'john@example.com', 'age': 28},
			format='json',
		)

		# Try to create second user with same email
		response = self.client.post(
			reverse('user-list'),
			{'name': 'Jane Doe', 'email': 'john@example.com', 'age': 26},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data)

	def test_get_missing_user_returns_404(self):
		"""Test that requesting a non-existent user returns 404"""
		response = self.client.get(reverse('user-detail', args=['550e8400-e29b-41d4-a716-446655440000']))

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_user_by_id(self):
		"""Test retrieving a user by ID"""
		# Create a user
		user = User.objects.create(name='John Doe', email='john@example.com', age=28)

		# Retrieve the user
		response = self.client.get(reverse('user-detail', args=[user.id]))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], 'John Doe')
		self.assertEqual(response.data['email'], 'john@example.com')
		self.assertEqual(response.data['age'], 28)

	def test_update_user_allows_partial_payload(self):
		"""Test partial update of user"""
		create_response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'john@example.com', 'age': 28},
			format='json',
		)
		user_id = create_response.data['id']

		update_response = self.client.put(
			reverse('user-detail', args=[user_id]),
			{'name': 'John Updated', 'age': 29},
			format='json',
		)

		self.assertEqual(update_response.status_code, status.HTTP_200_OK)
		self.assertEqual(update_response.data['name'], 'John Updated')
		self.assertEqual(update_response.data['email'], 'john@example.com')
		self.assertEqual(update_response.data['age'], 29)

	def test_delete_user(self):
		"""Test deleting a user"""
		create_response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'john@example.com', 'age': 28},
			format='json',
		)
		user_id = create_response.data['id']

		delete_response = self.client.delete(reverse('user-detail', args=[user_id]))

		self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
		
		# Verify user was deleted from database
		self.assertFalse(User.objects.filter(id=user_id).exists())
