import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(BASE_DIR))

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from src.tools.create_study_note import create_study_note

from src.document_processing.extract_text import extract_text

@api_view(["GET"])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "AI Study Assistant API is running!"
    })

@api_view(["POST"])
def generate_note(request):
    material = request.data.get("material")

    if not material or not isinstance(material, str):
        return Response(
            {"error": "Material is required and must be a string."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        note = create_study_note.invoke({"material": material})

        return Response(note, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(["POST"])
def generate_note_from_file(request):
    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return Response(
            {"error": "file is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        material = extract_text(uploaded_file)

        note = create_study_note.invoke({
            "material": material
        })

        return Response(note, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )