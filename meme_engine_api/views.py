from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Meme
from .serializers import MemeSerializer
from datetime import datetime

class MemeListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the meme items for given requested user
        '''
        memes = Meme.objects.filter(user = request.user.id)
        serializer = MemeSerializer(memes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given meme data
        '''
        data = {
            'memeName': request.data.get('meme'),
            'tags': request.data.get('tags'),
            'user': request.user.id,
            'status': True,
            'timestamp': datetime.now().time(),
        }
        serializer = MemeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MemeDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, meme_id, user_id):
        '''
        Helper method to get the object with given meme_id, and user_id
        '''
        try:
            return Meme.objects.get(memeId =meme_id, user = user_id)
        except Meme.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, meme_id, *args, **kwargs):
        '''
        Retrieves the Todo with given meme_id
        '''
        meme_instance = self.get_object(meme_id, request.user.id)
        if not meme_instance:
            return Response(
                {"res": "Object with meme id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MemeSerializer(meme_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, meme_id, *args, **kwargs):
        '''
        Updates the meme item with given meme_id if exists
        '''
        meme_instance = self.get_object(meme_id, request.user.id)
        if not meme_instance:
            return Response(
                {"res": "Object with meme id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'),
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = MemeSerializer(instance = meme_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, meme_id, *args, **kwargs):
        '''
        Deletes the meme item with given meme_id if exists
        '''
        meme_instance = self.get_object(meme_id, request.user.id)
        if not meme_instance:
            return Response(
                {"res": "Object with meme id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        meme_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
