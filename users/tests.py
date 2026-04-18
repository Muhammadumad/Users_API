from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .store import USERS


class UsersApiTests(APITestCase):
	def setUp(self):
		USERS.clear()

	def test_create_user(self):
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

	def test_create_user_rejects_invalid_email(self):
		response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'not-an-email', 'age': 28},
			format='json',
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('email', response.data)

	def test_get_missing_user_returns_404(self):
		response = self.client.get(reverse('user-detail', args=['550e8400-e29b-41d4-a716-446655440000']))

		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_user_allows_partial_payload(self):
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
		create_response = self.client.post(
			reverse('user-list'),
			{'name': 'John Doe', 'email': 'john@example.com', 'age': 28},
			format='json',
		)
		user_id = create_response.data['id']

		delete_response = self.client.delete(reverse('user-detail', args=[user_id]))

		self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(len(USERS), 0)
