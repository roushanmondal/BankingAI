from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .ml_engine import BankingIntentClassifier


class PredictIntentView(APIView):
    def post(self, request):
        #* Extract the user text from the Json body
        user_text = request.data.get('text', None)
        
        #* Validation: Did they actually send something ?
        if not user_text:
            return Response(
                {"error": "No text provided. Please send JSON with a 'text' key"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            #* Get the loaded model (this is instant because it's already in memory)
            classifier = BankingIntentClassifier.get_instance()

            #* Get prediction
            result = classifier.predict(user_text)

            #* Return JSON response
            return Response({
                "success": True,
                "input": user_text,
                "prediction": result #* Contains category, confidence, category_id
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Prediction Error: {str(e)}")
            return Response(
                {"error": "Internal Server Error processing request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )