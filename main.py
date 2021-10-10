import os
import numpy as np  # numpy для вычислений
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist         # библиотека базы выборок Mnist
from tensorflow import keras  # машинное зрение
from tensorflow.keras.layers import Dense, Flatten
from PIL import Image
import PIL.ImageOps
from keras import models
from keras import layers
from tensorflow.keras.utils import to_categorical

os.system("python draw.py")
os.system("python resize.py")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

directory = open('path.txt')
directory_path = directory.read()
# image = imread(directory_path)

model = models.Sequential()
model.add(layers.Conv2D(32,
                        (3, 3),
                        activation='relu',
                        input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64,
                        (3, 3),
                        activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64,
                        (3, 3),
                        activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64,
                       activation='relu'))
model.add(layers.Dense(10,
                       activation='softmax'))

print(model.summary())      # вывод структуры НС в консоль

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])


model.fit(train_images,
          train_labels,
          epochs=5,
          batch_size=64)

model.evaluate(train_images, train_labels)

image = Image.open(directory_path)
image = image.convert("L")
image = PIL.ImageOps.invert(image)

data = image.getdata()
data = np.array(data)

data = data.reshape((1, 28, 28, 1))
data = data.astype('float32') / 255

plt.imshow(data[0], cmap=plt.cm.binary)
plt.show()

x = np.expand_dims(data[0], axis=0)
res = model.predict(x)
print(res)
print( f"Распознанная цифра: {np.argmax(res)}" )

