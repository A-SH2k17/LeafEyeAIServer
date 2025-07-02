import tensorflow as tf
model_out = tf.keras.models.load_model("MobileNetV2.keras")
print("Model loaded")
print(model_out.summary())

model_out.save('MobileNetV2.h5')