from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import ResearcherSerializer
from .models import CustomUser
from rest_framework import status

@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def welcome(request):
    #Change BBQUDA once name change is finalized
    content = {"message": "Welcome to BBQUDA!"}
    return JsonResponse(content)

#GET Researcher by username
@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_researchers(request):
    user = request.user.id
    reseachers = CustomUser.objects.filter(username=user)
    serializer = ResearcherSerializer(reseachers, many=True)
    return JsonResponse({'researcher info': serializer.data}, safe=False, status=status.HTTP_200_OK)

#DELETE Researcher by ID
@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_researcher(request, researcher_id):
    user = request.user.id
    try:
        researcher_item = CustomUser.objects.get(username=user, id=researcher_id)
        #returns 0 or 1
        researcher_item.update(**payload)
        researcher = CustomUser.objects.get(id=researcher_id)
        serializer = ResearcherSerializer(researcher)
        return JsonResponse({'researcher:' serializer.data}, safe=False, status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error:' srt(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error:': 'Time to Panic!'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
