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
img_width, img_height = 224,224

top_model_weights_path = 'top_model_weights.hdf5'
train_data_dir = 'C:/Users/ragde/Desktop/data/train'
validation_data_dir = 'C:/Users/ragde/Desktop/data/test'
train_datagen = ImageDataGenerator()
#train_datagen = ImageDataGenerator(rescale=1. / 255)
traindata = train_datagen.flow_from_directory(directory=train_data_dir, target_size=(img_width, img_height))
#test_datagen = ImageDataGenerator(rescale=1. / 255)
test_datagen = ImageDataGenerator()
testdata = test_datagen.flow_from_directory(directory=train_data_dir, target_size=(img_width, img_height))

callbacks = myCallback()

model = tf.keras.applications.VGG16(
    include_top = False,
    input_shape = (img_width, img_height, 3),
    classes = 2,
    classifier_activation = 'softmax',
)
flat = keras.layers.Flatten()(model.layers[-1].output)
class1 = keras.layers.Dense(1024, activation = 'relu')(flat)
output = keras.layers.Dense(10, activation = 'softmax')(class1)
model = Model(inputs = model.inputs, outputs = output)
print(model.output_shape)

model.compile(optimizer='adam',
              loss = 'cross_entropy',
              metrics=['accuracy'])

model.summary()
model.fit(traindata, epochs=10000, callbacks=[callbacks])
model.save("C:/Users/ragde/Desktop/model/")

