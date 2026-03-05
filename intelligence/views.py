from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import LessonPlanGenerator
from planning.models import LessonPlan

@api_view(['POST'])
def generate_lesson_view(request):
    # Expecting { "substrand_id": 1, "material_id": 5 } in the POST body
    substrand_id = request.data.get('substrand_id')
    material_id = request.data.get('material_id')

    if not substrand_id:
        return Response({"error": "substrand_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Instantiate the service
        generator = LessonPlanGenerator(substrand_id, material_id)
        result = generator.generate()

        if result['success']:
            # Save to Database
            # Note: We are saving the raw string. In a real app, parse JSON to dict first.
            lesson = LessonPlan.objects.create(
                title=result['title'],
                substrand_id=substrand_id,
                reference_material_id=material_id,
                content={"raw_text": result['data']} # Store as dict
            )
            return Response({
                "message": "Lesson plan generated successfully",
                "lesson_id": lesson.id,
                "content": result['data']
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": result['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)