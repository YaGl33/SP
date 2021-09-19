import os
import random
import numpy as np  # numpy для вычислений
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist         # библиотека базы выборок Mnist
from tensorflow import keras # машинное зрение
from tensorflow.keras.layers import Dense, Flatten
from matplotlib.image import imread
from PIL import Image


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


(x_train, y_train), (x_test, y_test) = mnist.load_data()  # загрузка изображений для тестовой и тренировочной выборки

# стандартизация входных данных
x_train = x_train / 255 # тренировочная выборка
x_test = x_test / 255  # тестовая

directory = open('path.txt')
directory_path = directory.read()
# image = imread(directory_path)

image = Image.open(directory_path)
image = image.convert("L")
data = image.getdata()
data = np.matrix(data)

data = data / 255

# image = image.reshape((28, 28, 3))
# image = image.astype('float32') / 255

y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

plt.show()

model = keras.Sequential([  # модель нейронной сети
    Flatten(input_shape=(28, 28, 1)),  # первый слой
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

print(model.summary())      # вывод структуры НС в консоль

model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])


model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)

model.evaluate(x_test, y_test_cat)

n = 1
x = np.expand_dims(data[0], axis=0)
res = model.predict(x)
print( res )
print( np.argmax(res) )
# Распознавание всей тестовой выборки
pred = model.predict(data)
pred = np.argmax(pred, axis=1)

print(pred.shape)

print(pred[:20])
print(y_test[:20])

# Выделение неверных вариантов
mask = pred == y_test
print(mask[:10])

x_false = x_test[~mask]
y_false = x_test[~mask]

print(x_false.shape)


x = np.expand_dims(data[0], axis=0)
res = model.predict(x)
print(res)
print( f"Распознанная цифра: {np.argmax(res)}" )

plt.imshow(image, cmap=plt.cm.binary)
plt.show()