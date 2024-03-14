import tensorflow as tf

# Load the float32 TFLite model
model_path = r'C:\Users\Tom\Downloads\KHKT_2024\app\ei.lite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Convert the model to float16
converter = tf.lite.TFLiteConverter.from_saved_model(r'C:\Users\Tom\Downloads\saved_model')  # Or use converter.from_keras_model() for a Keras model
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
float16_model_content = converter.convert()

# Save the float16 model to a file
float16_model_path = r'C:\Users\Tom\Downloads\KHKT_2024\app\my_model.tflite'
with open(float16_model_path, 'wb') as f:
    f.write(float16_model_content)