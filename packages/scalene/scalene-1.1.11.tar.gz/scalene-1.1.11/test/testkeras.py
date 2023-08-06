import tensorflow.keras as keras

layer_in = keras.Input(shape=(608, 608, 3))
layer_0 = keras.layers.ZeroPadding2D(((1,1),(1,1)))(layer_in)
layer_0 = keras.layers.Conv2D(32, 3, strides=1, use_bias=False, name='conv_0')(layer_0)