from . import сегментация, повышение_размерности, датасет
from tensorflow.keras.layers import *
from tensorflow.keras.models import load_model, Sequential # Подключаем модель типа Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tensorflow.keras.utils import to_categorical, plot_model # Полкючаем методы .to_categorical() и .plot_model()
sns.set_style('darkgrid')
from tensorflow.keras.utils import to_categorical, plot_model # Полкючаем методы .to_categorical() и .plot_model()
from tensorflow.keras import backend as K # Импортируем модуль backend keras'а
from tensorflow.keras.optimizers import Nadam, RMSprop, Adadelta,Adam # Импортируем оптимизатор Adam
from tensorflow.keras.callbacks import ModelCheckpoint, LambdaCallback
from tensorflow.keras.models import Model # Импортируем модели keras: Model
from tensorflow.keras.layers import Input, RepeatVector, Conv2DTranspose, concatenate, Activation, Embedding, Input, MaxPooling2D, Conv2D, BatchNormalization # Импортируем стандартные слои keras
import importlib.util, sys, gdown,os
import tensorflow as tf
from PIL import Image
import time
from IPython.display import clear_output
from tensorflow.keras.preprocessing import image
import termcolor
from termcolor import colored
from google.colab import files

def создать_слой(данные, **kwargs):
  args={}
  if 'входной_размер' in kwargs:
    args['input_shape'] = kwargs['входной_размер']  
  
  параметры = [данные]
  act = 'relu'
  if '-' in данные:
    параметры = данные.split('-')  
  if параметры[0] == 'Полносвязный':    
    if len(параметры)>2:
      act = параметры[2]
    return Dense(int(параметры[1]), activation=act, **args)
  if параметры[0] == 'Повтор':
    return RepeatVector(int(параметры[1]))
  if параметры[0] == 'Эмбеддинг':
    return Embedding(int(параметры[2]), int(параметры[1]), input_length=int(параметры[3]))
  elif параметры[0] == 'Сверточный2D':
    if len(параметры)<5:
      act = 'linear'
      pad='same'
    else:
      act = параметры[4]
      pad = параметры[3]
    return Conv2D(int(параметры[1]), (int(параметры[2][1]),int(параметры[2][3])), padding=pad,activation=act, **args)
  elif параметры[0] == 'Сверточный1D':
    if len(параметры)>4:
      act = параметры[4]
      pad = параметры[3]
    else:
      act = 'relu'
      pad = 'same'
    return Conv1D(int(параметры[1]), int(параметры[2]), padding=pad,activation=act, **args)
  elif параметры[0] == 'Выравнивающий':
    if 'input_shape' in args:
      return Flatten(input_shape=args['input_shape'])
    else:
      return Flatten() 
  elif параметры[0] == 'Нормализация':
    return BatchNormalization()
  elif параметры[0] == 'Нормализация_01':
    return Lambda(normalize_01)
  elif параметры[0] == 'Нормализация_11':
    return Lambda(normalize_m11)
  elif параметры[0] == 'Денормализация':
    return Lambda(denormalize_m11)
  elif параметры[0] == 'Активация':
    return Activation(параметры[1])
  elif параметры[0] == 'ЛСТМ':    
    return LSTM(int(параметры[1]), return_sequences=параметры[2]=='True', **args)
  elif параметры[0] == 'МаксПуллинг2D':
    return MaxPooling2D((int(параметры[1][1]),int(параметры[1][3])))
  elif параметры[0] == 'МаксПуллинг1D':
    return MaxPooling1D(int(параметры[1][1]))
  elif параметры[0] == 'Дропаут':
    return Dropout(float(параметры[1]))
  elif параметры[0] == 'PReLU':
    return PReLU(shared_axes=[1, 2])
  elif параметры[0] == 'LeakyReLU':
    return LeakyReLU(alpha=float(параметры[1]))
  else:
    assert False, 'Невозможно добавить указанный слой: '+layers[0]

def upsample(x_in, num_filters):
    x = Conv2D(num_filters, kernel_size=3, padding='same')(x_in)
    x = Lambda(pixel_shuffle(scale=2))(x)
    return PReLU(shared_axes=[1, 2])(x)

def normalize_01(x):
    return x / 255.0

# Нормализует RGB изображения к промежутку [-1, 1]
def normalize_m11(x):
    return x / 127.5 - 1

# Обратная нормализация
def denormalize_m11(x):
    return (x + 1) * 127.5

#Метрика
def psnr(x1, x2):
    return tf.image.psnr(x1, x2, max_val=255)

def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)

def создать_сеть_для_классификации(слои, вход, параметры_модели):
  layers = слои.split()
  model = Sequential()
  layer = создать_слой(layers[0], входной_размер=вход)
  model.add(layer)   
  for i in range(1, len(layers)):
    layer = создать_слой(layers[i])
    model.add(layer)
  print('Создана модель нейронной сети!')
  параметры = параметры_модели.split()  
  loss = параметры[0].split(':')[1]
  opt = параметры[1].split(':')[1]
  metrica = ''
  if (len(параметры)>2):
    metrica = параметры[2].split(':')[1]
  if metrica=='':
    model.compile(loss=loss, optimizer = opt)
  else:
    model.compile(loss=loss, optimizer = opt, metrics=[metrica])
  return model

def создать_сеть_для_сегментации(слои, вход, параметры_модели):
  def точность(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
  layers = слои.split()
  model = Sequential()
  layer = создать_слой(layers[0], входной_размер=вход)
  model.add(layer) 
  for i in range(1, len(layers)):
    layer = создать_слой(layers[i])
    model.add(layer)
  print('Создана модель нейронной сети!')
  параметры = параметры_модели.split()  
  loss = параметры[0].split(':')[1]
  opt = параметры[1].split(':')[1]
  metrica = ''  
  if (len(параметры)>2):
    if параметры[2].split(':')[1] == 'dice_coef':
      metrica = точность
  model.compile(loss=loss, optimizer = opt, metrics =[metrica])
  return model

def создать_дискриминатор_повышения_размерности(блок_дискриминатора,количество_блоков, финальный_блок):
  x_in = Input(shape=(96, 96, 3))
  x = Lambda(normalize_m11)(x_in)
  blocks = блок_дискриминатора.split()
  for i in range(количество_блоков):
    for b in blocks:
      x = создать_слой(b) (x)      
  x = Flatten() (x)
  blocks = финальный_блок.split()
  for b in blocks:
    x = создать_слой(b) (x)  
  return Model(x_in, x)

 


def создать_генератор_повышения_размерности(стартовый_блок, основной_блок, финальный_блок):
  x_in = Input(shape=(None, None, 3))
  layers = стартовый_блок.split()
  x = создать_слой(layers[0]) (x_in)
  for i in range(1, len(layers)):
    x = создать_слой(layers[i]) (x)
  layers = основной_блок.split()
  x2 = создать_слой(layers[0]) (x)
  for i in range(1, len(layers)-1):
    x2 = создать_слой(layers[i]) (x2)
  x2 = Add()([x2, x2]) 
  x2 = создать_слой(layers[-1]) (x2)
  x = Add()([x, x2])
  x = upsample(x, 64 * 4)
  x = upsample(x, 64 * 4)
  layers = финальный_блок.split()
  x = создать_слой(layers[0]) (x)
  for i in range(1, len(layers)):
    x = создать_слой(layers[i]) (x)
  return Model(x_in, x)



def создать_UNET(**kwargs):
  def isConv2D(layer):
    return layer.split('-')[0]=='Сверточный2D'
      
  def точность(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
  block1 = kwargs['блок_вниз'].split()
  block2 = kwargs['блок_вверх'].split()
  if 'количество_выходных_классов' in kwargs:
    n_classes = kwargs['количество_выходных_классов']
  else:
    n_classes = 2
  img_input = Input(kwargs['входной_размер'])
  фильтры_вниз = kwargs['фильтры_вниз'].split()
  фильтры_вверх = kwargs['фильтры_вверх'].split()
  nBlock = len(фильтры_вниз)
  текущий_блок = 0
  b_o = []
  # DOWN
  layer = block1[0]
  if isConv2D(layer):
    layer = layer[:12]+'-'+фильтры_вниз[текущий_блок]+layer[12:]
  x = создать_слой(layer, входной_размер=kwargs['входной_размер']) (img_input)
  for i in range(1, len(block1)):
    layer = block1[i]
    if isConv2D(layer):
      layer = layer[:12]+'-'+фильтры_вниз[текущий_блок]+layer[12:]
    x = создать_слой(layer) (x)
  b_o.append(x)
  x = MaxPooling2D()(b_o[-1])    
  for i in range(nBlock-1):
    текущий_блок += 1
    for j in range(len(block1)):
      layer = block1[j]
      if isConv2D(layer):
        layer = layer[:12]+'-'+фильтры_вниз[текущий_блок]+layer[12:]
      x = создать_слой(layer) (x)
    b_o.append(x)
    x = MaxPooling2D()(b_o[-1])
  x = b_o[i+1]   
  # UP
  текущий_блок = 0
  for i in range(nBlock-1):
    текущий_блок += 1
    x = Conv2DTranspose(2**(2*nBlock-i), (2, 2), strides=(2, 2), padding='same')(x)    # Добавляем слой Conv2DTranspose с 256 нейронами
    for j in range(len(block2)):
      layer = block2[j]
      if layer=='Объединение':
        x = concatenate([x, b_o[nBlock-i-2]])
      else:
        if isConv2D(layer):
          layer = layer[:12]+'-'+фильтры_вверх[текущий_блок]+layer[12:]      
        x = создать_слой(layer) (x)
  x = Conv2D(n_classes, (3, 3), activation='softmax', padding='same')(x)  # Добавляем Conv2D-Слой с softmax-активацией на num_classes-нейронов

  мод = Model(img_input, x)
  параметры = kwargs['параметры_модели'].split()  
  loss = параметры[0].split(':')[1]
  opt = параметры[1].split(':')[1]
  metrica = ''  
  if (len(параметры)>2):
    if параметры[2].split(':')[1] == 'dice_coef':
      metrica = точность
  
  print('Создана модель нейронной сети!')
  мод.compile(loss=loss, optimizer = opt, metrics =[metrica])
  return мод
  
def создать_PSP(**kwargs):
  def точность(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.)
    
  img_input = Input(kwargs['входной_размер'])
  nBlock = kwargs['количество_блоков']
  if 'количество_выходных_классов' in kwargs:
    n_classes = kwargs['количество_выходных_классов']
  else:
    n_classes = 2
  start_block = kwargs['стартовый_блок']
  layers = start_block.split()
  layer = создать_слой(layers[0])  
  x = layer(img_input)
  for i in range(1, len(layers)):
    layer = создать_слой(layers[i])
    x = layer(x)
  
  x_mp = []
  conv_size = 32
  block_PSP = kwargs['блок_PSP']
  layers = block_PSP.split()  
  for i in range(nBlock):
    l = MaxPooling2D(2**(i+1))(x)
    for k in range(len(layers)):
      layer = создать_слой(layers[k])      
      l = layer(l)
    l = Conv2DTranspose(32, (2**(i+1), 2**(i+1)), strides=(2**(i+1), 2**(i+1)), activation='relu')(l)
    x_mp.append(l)
  

  fin = concatenate([img_input] + x_mp)

  final_block = kwargs['финальный_блок']
  layers = final_block.split()
  for i in range(len(layers)):
    layer = создать_слой(layers[i])
    fin = layer(fin)

  параметры = kwargs['параметры_модели'].split()  
  loss = параметры[0].split(':')[1]
  opt = параметры[1].split(':')[1]
  metrica = ''  
  if (len(параметры)>2):
    if параметры[2].split(':')[1] == 'dice_coef':
      metrica = точность
  

  мод = Model(img_input, fin)
  print('Создана модель нейронной сети!')
  мод.compile(loss='categorical_crossentropy', optimizer=Adam(lr=3e-4), metrics =[точность])
  return мод
  

def создать_составную_сеть_квартиры(данные, *нейронки):    
    input1 = Input(данные[0].shape[1],)
    input2 = Input(данные[1].shape[1],)
    
    layers = нейронки[0].split()
    x1 = создать_слой(layers[0]) (input1)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!=0, 'Невозможно добавить указанный слой: '+layer
        x1 = создать_слой(layers[i]) (x1)

    layers = нейронки[1].split()
    x2 = создать_слой(layers[0]) (input2)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!=0, 'Невозможно добавить указанный слой: '+layer
        x2 = создать_слой(layers[i]) (x2)
           
    x = concatenate([x1, x2])
    layers = нейронки[2].split()
    x3 = создать_слой(layers[0]) (x)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!='0', 'Невозможно добавить указанный слой: '+layer
        x3 = создать_слой(layers[i]) (x3)    
    model = Model([input1, input2], x3)
    model.compile(loss="mae", optimizer=Nadam(lr=1e-3), metrics=["mae"])
    return model


def создать_составную_сеть(данные, *нейронки):
    img_input1 = Input((50,))
    img_input2 = Input(данные[1].shape[1],)
    img_input3 = Input(данные[2].shape[1],)
    
    layers = нейронки[0].split()
    x1 = создать_слой(layers[0]) (img_input1)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!=0, 'Невозможно добавить указанный слой: '+layer
        x1 = создать_слой(layers[i]) (x1)

    layers = нейронки[1].split()
    x2 = создать_слой(layers[0]) (img_input2)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!=0, 'Невозможно добавить указанный слой: '+layer
        x2 = создать_слой(layers[i]) (x2)
    
    layers = нейронки[2].split()
    x3 = создать_слой(layers[0]) (img_input3)
    for i in range(1, len(layers)):
        layer = создать_слой(layers[i])
        assert layer!=0, 'Невозможно добавить указанный слой: '+layer
        x3 = создать_слой(layers[i]) (x3)
        
    x = concatenate([x1, x2, x3])
    x = Dense(1024, activation="relu")(x)
    x = Dense(10, activation="softmax")(x)
    
    model = Model([img_input1, img_input2, img_input3], x)
    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=5e-5), metrics=["accuracy"])
    return model
    
def создать_сеть_чат_бот(размер_словаря, энкодер, декодер):
  encoderInputs = Input(shape=(None , )) # размеры на входе сетки (здесь будет encoderForInput)
  
  layers = энкодер.split()
  if '-' in layers[0]:
    буква, параметр = layers[0].split('-')
    x = Embedding(размер_словаря, int(параметр), mask_zero=True) (encoderInputs)      
  for i in range(1, len(layers)-1):
    layer = создать_слой(layers[i])
    assert layer!=0, 'Невозможно добавить указанный слой: '+layer
    x = создать_слой(layers[i]) (x)
  if '-' in layers[-1]:
    буква, параметр = layers[-1].split('-')
  encoderOutputs, state_h , state_c = LSTM(int(параметр), return_state=True)(x)
  encoderStates = [state_h, state_c]
    
  decoderInputs = Input(shape=(None, )) # размеры на входе сетки (здесь будет decoderForInput)
  layers = декодер.split()
  if '-' in layers[0]:
    буква, параметр = layers[0].split('-')
    x = Embedding(размер_словаря, int(параметр), mask_zero=True) (decoderInputs) 
  for i in range(1, len(layers)-1):
    layer = создать_слой(layers[i])
    assert layer!=0, 'Невозможно добавить указанный слой: '+layer
    x = создать_слой(layers[i]) (x)
  if '-' in layers[-1]:
    буква, параметр = layers[-1].split('-')
  decoderLSTM = LSTM(int(параметр), return_state=True, return_sequences=True)
  decoderOutputs , _ , _ = decoderLSTM (x, initial_state=encoderStates)
  # И от LSTM'а сигнал decoderOutputs пропускаем через полносвязный слой с софтмаксом на выходе
  decoderDense = Dense(размер_словаря, activation='softmax') 
  output = decoderDense (decoderOutputs)
  ######################
  # Собираем тренировочную модель нейросети
  ######################
  model = Model([encoderInputs, decoderInputs], output)
  model.compile(optimizer=RMSprop(), loss='sparse_categorical_crossentropy', metrics=["accuracy"])
  return model        
    
  
def схема_модели(модель):
  print('Схема модели:')
  return plot_model(модель) # Выводим схему модели

def создать_сеть(слои, входной_размер, параметры_модели, задача):
  layers = слои.split()
  if задача == 'классификация изображений' or задача == 'временной ряд' or задача == 'аудио':
    return создать_сеть_для_классификации(слои, входной_размер, параметры_модели)
  if задача == 'сегментация изображений' or задача == 'сегментация текста':
    return создать_сеть_для_сегментации(слои, входной_размер, параметры_модели)


def обучение_модели_квартиры(модель, x_train, y_train, x_test=None, y_test=None, batch_size=None, epochs=None, коэф_разделения = 0.2, инструменты = None):
  cur_time = time.time()
  global loss, val_loss
  def on_epoch_end(epoch, logs):
    global cur_time, loss, val_loss
    pred = модель.predict(x_test) #Полуаем выход сети на проверочно выборке
    predUnscaled = инструменты[0].inverse_transform(pred).flatten() #Делаем обратное нормирование выхода к изначальным величинам цен квартир
    yTrainUnscaled = инструменты[0].inverse_transform(y_test).flatten() #Делаем такое же обратное нормирование yTrain к базовым ценам
    delta = predUnscaled - yTrainUnscaled #Считаем разность предсказания и правильных цен
    absDelta = abs(delta) #Берём модуль отклонения

    pred2 = модель.predict(x_train) #Полуаем выход сети на проверочно выборке
    predUnscaled2 = инструменты[0].inverse_transform(pred2).flatten() #Делаем обратное нормирование выхода к изначальным величинам цен квартир
    yTrainUnscaled2 = инструменты[0].inverse_transform(y_train).flatten() #Делаем такое же обратное нормирование yTrain к базовым ценам
    delta2 = predUnscaled2 - yTrainUnscaled2 #Считаем разность предсказания и правильных цен
    absDelta2 = abs(delta2) #Берём модуль отклонения
    loss.append(sum(absDelta2) / (1e+6 * len(absDelta2)))
    val_loss.append(sum(absDelta) / (1e+6 * len(absDelta)))
    p1 = 'Эпоха №' + str(epoch+1)
    p2 = p1 + ' '* (10 - len(p1)) + 'Время обучения: ' + str(round(time.time()-cur_time,2)) +'c'
    p3 = p2 + ' '* (33 - len(p2)) + 'Ошибка на обучающей выборке: ' + str(round(sum(absDelta2) / (1e+6 * len(absDelta2)), 3))+'млн'
    p4 = p3 + ' '* (77 - len(p3)) + 'Ошибка на проверочной выборке: ' + str(round(sum(absDelta) / (1e+6 * len(absDelta)), 3))+'млн'
    print(p4)   
    cur_time = time.time()
    # Коллбэки

  filepath="model.h5"
  model_checkpoint_callback = ModelCheckpoint(
    filepath=filepath,
    save_weights_only=True,
    monitor='val_loss',
    mode='min',
    save_best_only=True)

  def on_train_begin(log):
    global cur_time, loss, val_loss
    loss=[]
    val_loss = []

  def on_epoch_begin(epoch, log):
    global cur_time
    cur_time = time.time()
  myCB = LambdaCallback(on_train_begin=on_train_begin, on_epoch_end = on_epoch_end, on_epoch_begin=on_epoch_begin)
  myCB23 = LambdaCallback(on_epoch_end = on_epoch_end, on_epoch_begin=on_epoch_begin)
  модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_test, y_test), callbacks=[model_checkpoint_callback, myCB], verbose = 0)
  модель.load_weights('model.h5')
  модель.compile(optimizer=Nadam(lr=1e-4), loss='mae')
  модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_test, y_test), callbacks=[model_checkpoint_callback, myCB23], verbose = 0)
  модель.load_weights('model.h5')
  модель.compile(optimizer=Nadam(lr=1e-5), loss='mae')
  модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_test, y_test), callbacks=[model_checkpoint_callback, myCB23], verbose = 0)
  модель.load_weights('model.h5')
  модель.save('model_s.h5')
  plt.figure(figsize=(12, 6)) # Создаем полотно для визуализации  
  plt.plot(loss, label ='Обучающая выборка') # Визуализируем график ошибки на обучающей выборке
  plt.plot(val_loss, label ='Проверочная выборка') # Визуализируем график ошибки на проверочной выборке
  plt.legend() # Выводим подписи на графике
  plt.title('График ошибки обучения') # Выводим название графика
  plt.show()
  

def обучение_модели_трафик(мод, ген1, ген2, количество_эпох=None):
  filepath="model.h5"
  model_checkpoint_callback = ModelCheckpoint(
    filepath=filepath,
    save_weights_only=True,
    monitor='val_loss',
    mode='min',
    save_best_only=True)
    
  cur_time = time.time()
  def on_epoch_end(epoch, log):
    k = list(log.keys())
    global cur_time
    p1 = 'Эпоха №' + str(epoch+1)
    p2 = p1 + ' '* (10 - len(p1)) + 'Время обучения: ' + str(round(time.time()-cur_time,2)) +'c'
    p3 = p2 + ' '* (33 - len(p2)) + 'Ошибка на обучающей выборке: ' + str(round(log[k[0]],5))
    p4 = p3 + ' '* (77 - len(p3)) + 'Ошибка на прверочной выборке: ' + str(round(log[k[1]],5))
    print(p4)
    cur_time = time.time()
  def on_epoch_begin(epoch, log):
    global cur_time
    cur_time = time.time()
  myCB = LambdaCallback(on_epoch_end = on_epoch_end, on_epoch_begin=on_epoch_begin)

  history = мод.fit_generator(ген1, epochs=количество_эпох, verbose=0, validation_data=ген2, callbacks=[model_checkpoint_callback, myCB])
  
  plt.plot(history.history['loss'], label='Ошибка на обучающем наборе')
  plt.plot(history.history['val_loss'], label='Ошибка на проверочном наборе')
  plt.ylabel('Средняя ошибка')
  plt.legend()

def обучение_модели(модель, x_train, y_train, x_test=[], y_test=[], batch_size=None, epochs=None, коэф_разделения = 0.2):
  global result, idx_best, best_result
  result = ''
  idx_best = 0
  best_result = 0
  if batch_size == None:
    batch_size = int(x_train.shape[0] * 0.01)
  if epochs == None:
    epochs = 10
  filepath="model.h5"
  model_checkpoint_callback = ModelCheckpoint(
    filepath=filepath,
    save_weights_only=True,
    monitor='val_loss',
    mode='min',
    save_best_only=True)
    
  cur_time = time.time()
  def on_epoch_end(epoch, log):
    k = list(log.keys())
    global cur_time, result, idx_best, best_result   
    p1 = 'Эпоха №' + str(epoch+1)
    p2 = p1 + ' '* (10 - len(p1)) + 'Время обучения: ' + str(round(time.time()-cur_time,2)) +'c'
    p3 = p2 + ' '* (33 - len(p2)) + 'Точность на обучающей выборке: ' + str(round(log[k[1]]*100,2))+'%'
    if len(k)>2:
        p4 = p3 + ' '* (77 - len(p3)) + 'Точность на проверочной выборке: ' + str(round(log[k[3]]*100,2))+'%'
        result += p4 + '\n'
        if log[k[3]]*100 > best_result:
          best_result = log[k[3]]*100
          idx_best = epoch
        print(p4)
    else:
        result += p3 + '\n'
        if log[k[1]]*100 > best_result:
          best_result = log[k[1]]*100
          idx_best = epoch
        print(p3)    
    cur_time = time.time()
  def on_epoch_begin(epoch, log):
    global cur_time
    cur_time = time.time()
  myCB = LambdaCallback(on_epoch_end = on_epoch_end, on_epoch_begin=on_epoch_begin)
  
  if len(x_test)==0:
    model_checkpoint_callback = ModelCheckpoint(
        filepath=filepath,
        save_weights_only=True,
        monitor='loss',
        mode='min',
        save_best_only=True)
    history = модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, callbacks=[model_checkpoint_callback, myCB], verbose = 0)
  else:
    history = модель.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_test, y_test), callbacks=[model_checkpoint_callback, myCB], verbose = 0)
  
  модель.load_weights('model.h5')
  модель.save('model_s.h5')
  clear_output(wait=True)
  result = result.split('\n')
  for i in range(len(result)):
    s = result[i]
    if i == idx_best:
      s = colored(result[i], color='white', on_color='on_green')
    print(s)
  plt.figure(figsize=(12, 6)) # Создаем полотно для визуализации
  keys = list(history.history.keys())
  plt.plot(history.history[keys[0]], label ='Обучающая выборка') # Визуализируем график ошибки на обучающей выборке
  if len(keys)>2:
    plt.plot(history.history['val_'+keys[0]], label ='Проверочная выборка') # Визуализируем график ошибки на проверочной выборке
  plt.legend() # Выводим подписи на графике
  plt.title('График ошибки обучения') # Выводим название графика
  plt.show()
  plt.figure(figsize=(12,6)) # Создаем полотно для визуализации
  plt.plot(history.history[keys[1]], label ='Обучающая выборка') # Визуализируем график точности на обучающей выборке
  if len(keys)>2:
    plt.plot(history.history['val_'+keys[1]], label ='Проверочная выборка') # Визуализируем график точности на проверочной выборке
  plt.legend() # Выводим подписи на графике
  plt.title('График точности обучения') # Выводим название графика
  plt.show()


def тест_модели_классификации(модель=None, тестовый_набор=None, правильные_ответы=[], классы=None, количество=1):
  for i in range(количество):
    number = np.random.randint(тестовый_набор.shape[0]) # Задаем индекс изображения в тестовом наборе
    sample = тестовый_набор[number]
    if sample.shape == (784,):
      sample = sample.reshape((28,28))  
    if sample.shape == (28, 28, 1):
      sample = sample.reshape((28,28))
    print('Тестовое изображение:')
    plt.imshow(sample, cmap='gray') # Выводим изображение из тестового набора с заданным индексом
    plt.axis('off') # Отключаем оси
    plt.show() 

    sample = тестовый_набор[number].reshape((1 + модель.input.shape[1:]))
    pred = модель.predict(sample)[0] # Распознаем изображение с помощью обученной модели
    print()
    print('Результат предсказания модели:')
    for i in range(len(классы)):
      print('Модель распознала модель ',классы[i],' на ',round(100*pred[i],2),'%',sep='')
    print('---------------------------')
    if len(правильные_ответы)>0:
      print('Правильный ответ: ', классы[правильные_ответы[number]])
      print('---------------------------')
      print()
      print()
      print()

def тест_модели_HR(gan_generator):
  def load_image(path):
    return np.array(Image.open(path))
  #Функция для преобразования картинки lr в sr
  def resolve(model, lr_batch):
      lr_batch = tf.cast(lr_batch, tf.float32)
      sr_batch = model(lr_batch)
      sr_batch = tf.clip_by_value(sr_batch, 0, 255)
      sr_batch = tf.round(sr_batch)
      sr_batch = tf.cast(sr_batch, tf.uint8)
      return sr_batch 
  def resolve_single(model, lr):
    return resolve(model, tf.expand_dims(lr, axis=0))[0]
  def resolve_and_plot(lr_image_path):
    lr = load_image(lr_image_path)    
    gan_sr = resolve_single(gan_generator, lr)    
    plt.figure(figsize=(10, 15))
    images = [lr, gan_sr]
    titles = ['Исходное изображение', 'Изображение после обработки']
    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 2, i+1)
        plt.imshow(img)
        plt.title(title, fontsize=10)
        plt.xticks([])
        plt.yticks([])  

  url = 'https://storage.googleapis.com/aiu_bucket/Examples.zip' # Указываем URL-файла
  output = 'Examples.zip' # Указываем имя файла, в который сохраняем файл
  gdown.download(url, output, quiet=True) # Скачиваем файл по указанному URL
  # Скачиваем и распаковываем архив
  датасет.распаковать_архив(
      откуда = "Examples.zip",
      куда = "/content"
  )
  for file in os.listdir('demo1/'):
    resolve_and_plot('demo1/' + file)

def показать_график_обучения(**kwargs):
  keys = list(kwargs['статистика'].history.keys())
  for i in range(len(keys)//2):
    plt.figure(figsize=(12, 6)) # Создаем полотно для визуализации
    plt.plot(kwargs['статистика'].history[keys[i]], label ='Обучающая выборка') # Визуализируем график ошибки на обучающей выборке
    plt.plot(kwargs['статистика'].history['val_'+keys[i]], label ='Проверочная выборка') # Визуализируем график ошибки на проверочной выборке
    plt.legend() # Выводим подписи на графике
    if 'loss' in keys[i]:
      plt.title('График ошибки обучения модели') # Выводим название графика
    else:
      plt.title('График точности обучения модели') # Выводим название графика
    plt.show()

def загрузить_предобученную_модель():
  url = 'https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1QYLIUQWWyqLvn8TCEAZiY7q8umv7lyYw' # Указываем URL-файла
  output = 'model.h5' # Указываем имя файла, в который сохраняем файл
  gdown.download(url, output, quiet=True) 
  model = load_model('model.h5')
  return model

def создать_модель_HighResolution():
  LR_SIZE = 24
  HR_SIZE = 96
    #Коэффициенты для преобразования RGB
  DIV2K_RGB_MEAN = np.array([0.4488, 0.4371, 0.4040]) * 255
  # Нормализует RGB изображения к промежутку [0, 1]
  def normalize_01(x):
    return x / 255.0
  # res_block
  def res_block(x_in, num_filters, momentum=0.8):
      x = Conv2D(num_filters, kernel_size=3, padding='same')(x_in)
      x = BatchNormalization(momentum=momentum)(x)
      x = PReLU(shared_axes=[1, 2])(x)
      x = Conv2D(num_filters, kernel_size=3, padding='same')(x)
      x = BatchNormalization(momentum=momentum)(x)
      x = Add()([x_in, x])
      return x  
  # Блок апсемплинга
  def upsample(x_in, num_filters):
      x = Conv2D(num_filters, kernel_size=3, padding='same')(x_in)
      x = Lambda(pixel_shuffle(scale=2))(x)
      return PReLU(shared_axes=[1, 2])(x)   

  def pixel_shuffle(scale):
    return lambda x: tf.nn.depth_to_space(x, scale)     

  # Обратная нормализация
  def denormalize(x, rgb_mean=DIV2K_RGB_MEAN):
    return x * 127.5 + rgb_mean
  # Обратная нормализация
  def denormalize_m11(x):
      return (x + 1) * 127.5
      
  def sr_resnet(num_filters=64, num_res_blocks=16):
      x_in = Input(shape=(None, None, 3))
      x = Lambda(normalize_01)(x_in)

      x = Conv2D(num_filters, kernel_size=9, padding='same')(x)
      x = x_1 = PReLU(shared_axes=[1, 2])(x)

      for _ in range(num_res_blocks):
          x = res_block(x, num_filters)

      x = Conv2D(num_filters, kernel_size=3, padding='same')(x)
      x = BatchNormalization()(x)
      x = Add()([x_1, x])

      x = upsample(x, num_filters * 4)
      x = upsample(x, num_filters * 4)

      x = Conv2D(3, kernel_size=9, padding='same', activation='tanh')(x)
      x = Lambda(denormalize_m11)(x)

      return Model(x_in, x)
  generator = sr_resnet
  return generator

def тест_на_своем_изображении(нейронка, размер_изображения, классы):
  fname = files.upload()
  fname = list(fname.keys())[0]
  sample = image.load_img('/content/'+ fname, target_size=(размер_изображения[0], размер_изображения[1])) # Загружаем картинку
  img_numpy = np.array(sample)[None,...] # Преобразуем зображение в numpy-массив
  img_numpy = img_numpy/255
  тест_модели_классификации(
    нейронка,
    тестовый_набор = img_numpy,
    классы = классы)



