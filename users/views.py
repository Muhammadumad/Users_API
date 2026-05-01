from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def user_list(request):
    """
    GET: Retrieve all users
    POST: Create a new user
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST: Create a new user
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check for duplicate email (already enforced at DB level, but provide helpful error)
    email = serializer.validated_data['email'].lower().strip()
    if User.objects.filter(email__iexact=email).exists():
        return Response(
            {'email': ['A user with this email already exists.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    """
    GET: Retrieve a specific user
    PUT: Update a specific user (partial updates allowed)
    DELETE: Delete a specific user
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        if not request.data:
            return Response({'error': 'Request body cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate email when updating
        if 'email' in request.data:
            new_email = request.data['email'].lower().strip()
            if User.objects.filter(email__iexact=new_email).exclude(id=user_id).exists():
                return Response(
                    {'email': ['A user with this email already exists.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)