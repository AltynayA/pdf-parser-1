import tensorflow as tf
from tensorflow.keras import layers, models
from tqdm.keras import TqdmCallback


def build_pdf_model(input_shape, num_classes):
    inputs = layers.Input(shape=input_shape)

    x = layers.Conv2D(32, 3, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Conv2D(128, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D(2)(x)

    x = layers.Flatten()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs, outputs)
    return model

model = build_pdf_model(input_shape=(224, 224, 3), num_classes=10)

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "data/train",
    image_size=(224, 224),
    batch_size=32
)

val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "data/val",
    image_size=(224, 224),
    batch_size=32
)


history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=10,
    callbacks=[TqdmCallback(verbose=1)]
)

