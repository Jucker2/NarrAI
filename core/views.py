from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os

from core.domaine.document import Document
from core.services.narration_pipeline import NarrationPipeline

@csrf_exempt
def upload_book(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Method not allowed"
            },
            status=405
        )

    pdf_file = request.FILES.get("pdf")

    if not pdf_file:
        return JsonResponse(
            {
                "error": "No PDF provided"
            },
            status=400
        )

    # Sauvegarde temporaire du PDF
    pdf_path = f"media/{pdf_file.name}"

    with open(pdf_path, "wb+") as destination:

        for chunk in pdf_file.chunks():
            destination.write(chunk)

    document = Document(
        title=pdf_file.name,
        pdf_path=pdf_path
    )

    pipeline = NarrationPipeline()

    document = pipeline.process(document)

    return JsonResponse(
        {
            "uuid": document.uuid,
            "title": document.title,
            "chapters": len(document.chapters),
            "message": "PDF processed successfully"
        }
    )