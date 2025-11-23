import os
import torch
import json
from transformers import BertTokenizer, BertForSequenceClassification
from django.conf import settings

class BankingIntentClassifier:
    _instance = None

    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure model loads only once."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        print("Loading AI model... (This takes a few seconds)")
        #* path of the model folder
        base_dir = settings.BASE_DIR
        model_path = os.path.join(base_dir, 'model_assets')

        #* Load tokenizer and model
        try:
            self.tokenizer = BertTokenizer.from_pretrained(model_path)
            self.model = BertForSequenceClassification.from_pretrained(model_path)
            self.model.eval() #set to inference mode (faster, no training)

            #* Load the label map (JSON)
            with open(os.path.join(model_path, 'label_map.json'), 'r') as f:
                #* JSON keys are always string, convert back to int for lookup
                self.label_map = {int(k): v for k, v in json.load(f).items()}
            
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Critical error loading model: {e}")
            raise e
    
    def predict(self, text):
        """
        Takes a string text, returns the predicted category name and confidence
        """
        #* Preprocess
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=64,
            padding=True
        )

        #* Inference
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        #* Post-process
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
        confidence, predicted_class_id = torch.max(probabilities, dim=1)

        #* Decode label
        prediction_id = predicted_class_id.item()
        cateory_name = self.label_map.get(prediction_id, "Unknown")

        return {
            "category": cateory_name,
            "confidence": round(confidence.item(), 4),
            "category_id": prediction_id
        }