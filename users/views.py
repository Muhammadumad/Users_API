from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .store import USERS, email_in_use, normalize_email


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        serializer = UserSerializer(list(USERS.values()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if email_in_use(serializer.validated_data['email']):
        return Response(
            {'email': ['A user with this email already exists.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = serializer.save()
    user['email'] = normalize_email(user['email'])
    USERS[user['id']] = user
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):
    user = USERS.get(user_id)
    if user is None:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        if not request.data:
            return Response({'error': 'Request body cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updated_email = serializer.validated_data.get('email', user['email'])
        if email_in_use(updated_email, exclude_user_id=user_id):
            return Response(
                {'email': ['A user with this email already exists.']},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated_user = serializer.save()
        updated_user['email'] = normalize_email(updated_user['email'])
        USERS[user_id] = updated_user
        return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)

    del USERS[user_id]
    return Response(status=status.HTTP_204_NO_CONTENT)