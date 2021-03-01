import keras
import tensorflow as tf
from keras.models import Model
from keras.layers import Dense
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.callbacks import ModelCheckpoint, EarlyStopping
from myCallback import *



#this can be played around with, but the original size (640 x 480) is too large!
img_width, img_height = 320,320

top_model_weights_path = 'top_model_weights.hdf5'
train_data_dir = 'C:/Users/ragde/Desktop/data/train'
validation_data_dir = 'C:/Users/ragde/Desktop/data/test'

train_datagen = ImageDataGenerator(rescale=1. / 255)
traindata = train_datagen.flow_from_directory(directory=train_data_dir, target_size=(img_width, img_height))
test_datagen = ImageDataGenerator(rescale=1. / 255)
testdata = test_datagen.flow_from_directory(directory=train_data_dir, target_size=(img_width, img_height))

callbacks = myCallback()

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(img_width, img_height, 3)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])
print(model.output_shape)
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()
model.fit(traindata, epochs=10000, callbacks=[callbacks])
model.save("C:/Users/ragde/Desktop/model/")

