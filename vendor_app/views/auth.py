from vendor_app.Serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.create(validated_data=serializer.validated_data)
    return Response(user)