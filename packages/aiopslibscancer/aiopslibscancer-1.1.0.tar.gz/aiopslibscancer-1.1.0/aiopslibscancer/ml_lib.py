from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow.keras.backend as K

from PIL import Image, ImageOps
from io import BytesIO
import base64
import numpy as np
import json

# Discriminator: Shared weights between the supervised classifier and standard discriminator 
# as found in GANs
# Reference: Chapter 20, GANs in Python by Jason Brownlee, Chapter 7 of GANs in Action

# Activation function for the discriminator as proposed in https://arxiv.org/abs/1606.03498

def custom_activation(output):
    logexpsum = K.sum(K.exp(output), axis=-1, keepdims=True)
    result = logexpsum / (logexpsum + 1.0)
    return result

def disc_network(in_shape=(50,50,3), n_classes=2):
    
    in_image = Input(shape=in_shape)
 
    fe = Conv2D(32, (3,3), strides=(2,2), padding='same')(in_image)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(64, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(128, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Conv2D(256, (3,3), strides=(2,2), padding='same')(fe)
    fe = BatchNormalization()(fe)
    fe = LeakyReLU(alpha=0.01)(fe)

    fe = Dropout(0.4)(fe)
    fe = Flatten()(fe)

    fe = Dense(n_classes)(fe)

    # Supervised classifier
    c_out_layer = Activation('softmax')(fe)
    c_model = Model(in_image, c_out_layer)

    # Traditional discriminator as found in GANs
    d_out_layer = Lambda(custom_activation)(fe)
    d_model = Model(in_image, d_out_layer)

    return d_model, c_model

# Generator
# Reference: Chapter 20, GANs in Python by Jason Brownlee, Chapter 7 of GANs in Action
def generator_network(latent_dim):
    in_lat = Input(shape=(latent_dim,))

    n_nodes = 256 * 3 * 3
    gen = Dense(n_nodes)(in_lat)
    gen = Reshape((3, 3, 256))(gen)

    gen = Conv2DTranspose(128, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)

    gen = Conv2DTranspose(64, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(32, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(16, (3,3), strides=(1,1), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = Conv2DTranspose(8, (3,3), strides=(2,2), padding='same')(gen)
    # gen = BatchNormalization()(gen)
    gen = LeakyReLU(alpha=0.01)(gen)
    
    gen = ZeroPadding2D()(gen)
    
    out_layer = Conv2DTranspose(3, (3,3), strides=(1, 1), activation='tanh', padding='same')(gen)

    model = Model(in_lat, out_layer)

    return model


class Predictor(object):
    def predict(self, model, images_base64, image_shape, labels):
        responses = []
        #for base64Img in images_base64:
        for img_file_key, base64Img in images_base64.items():
            decoded_img = base64.b64decode(base64Img)
            img_buffer = BytesIO(decoded_img)
            imageData = Image.open(img_buffer).convert("RGB")
            
            img = ImageOps.fit(imageData, image_shape, Image.ANTIALIAS)
            img_conv = np.array(img)

            x_test = img_conv / 255.0
            x_test = np.expand_dims(x_test, 0)

            y_pred = model.predict(x_test)
            y_pred_prob = np.max(y_pred, axis=-1)
            y_pred = np.argmax(y_pred, axis=-1)
            
            resp = {img_file_key: [str(labels[y_pred[0]]), str(y_pred_prob[0])]}
            responses.append(resp)
        return json.dumps(responses)
