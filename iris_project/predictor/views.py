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
            proba = model.predict_proba(features)[0] # lấy mảng xác suất cho cả 3 loài
            max_proba = np.max(proba)
            
            prediction_idx = np.argmax(proba)
            
            if max_proba < 0.8:
                prediction = None
                warning_message = f"Dữ liệu ngoại lai hoặc không rõ ràng (Độ tin cậy cao nhất chỉ đạt {max_proba * 100:.1f}%)."
                
                return render(request, 'predictor/predict.html', {
                    'form': form,
                    'warning_message': warning_message
                })
            else:
                prediction = SPECIES_MAP[prediction_idx]
                confidence = f"{max_proba * 100:.2f}%"
                
                return render(request, 'predictor/predict.html', {
                    'form': form,
                    'prediction': prediction,
                    'confidence': confidence,
                })

    else:
        form = IrisPredictionForm()
    
    return render(request, 'predictor/predict.html', {
        'form': form,
    })
