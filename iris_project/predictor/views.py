import joblib
import numpy as np
from django.shortcuts import render
from django.conf import settings

from .forms import IrisPredictionForm


# Mapping từ số sang tên loài hoa
SPECIES_MAP = {
    0: 'Iris-setosa',
    1: 'Iris-versicolor', 
    2: 'Iris-virginica'
}

# Load model một lần khi khởi động server
_model = None


def get_model():
    """Load model từ file, chỉ load một lần."""
    global _model
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)
    return _model


def predict_view(request):
    """View xử lý form input và dự đoán loài hoa Iris."""
    prediction = None
    
    if request.method == 'POST':
        form = IrisPredictionForm(request.POST)
        if form.is_valid():
            # Lấy dữ liệu từ form
            sepal_length = form.cleaned_data['sepal_length']
            sepal_width = form.cleaned_data['sepal_width']
            petal_length = form.cleaned_data['petal_length']
            petal_width = form.cleaned_data['petal_width']
            
            # Tạo array features
            features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
            
            # Load model và predict
            model = get_model()
            prediction_idx = model.predict(features)[0]
            
            # Map kết quả sang tên loài
            prediction = SPECIES_MAP[prediction_idx]
    else:
        form = IrisPredictionForm()
    
    return render(request, 'predictor/predict.html', {
        'form': form,
        'prediction': prediction,
    })
