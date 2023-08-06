import logging
import os
import tempfile
import zipfile

import requests
import tensorflow as tf

import baseten
from baseten.baseten_deployed_model import BasetenDeployedModel

MNIST_PRETRAINED_URL = 'https://baseten-public.s3-us-west-2.amazonaws.com/models/mnist.zip'
logger = logging.getLogger(__name__)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def build_model() -> tf.keras.Model:
    """Constructs the ML model used to predict handwritten digits."""

    image = tf.keras.layers.Input(shape=(28, 28, 1))

    y = tf.keras.layers.Conv2D(filters=32,
                               kernel_size=5,
                               padding='same',
                               activation='relu')(image)
    y = tf.keras.layers.MaxPooling2D(pool_size=(2, 2),
                                     strides=(2, 2),
                                     padding='same')(y)
    y = tf.keras.layers.Conv2D(filters=32,
                               kernel_size=5,
                               padding='same',
                               activation='relu')(y)
    y = tf.keras.layers.MaxPooling2D(pool_size=(2, 2),
                                     strides=(2, 2),
                                     padding='same')(y)
    y = tf.keras.layers.Flatten()(y)
    y = tf.keras.layers.Dense(1024, activation='relu')(y)
    y = tf.keras.layers.Dropout(0.4)(y)

    probs = tf.keras.layers.Dense(10, activation='softmax')(y)

    model = tf.keras.models.Model(inputs=image, outputs=probs, name='mnist')

    return model


def scale_inputs(input_images):
    return input_images / 255.


def get_test_data():
    _, (X_test, Y_test) = get_training_data()
    return X_test, Y_test


def get_training_data():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    train_images = train_images.reshape((-1, 28, 28, 1))
    test_images = test_images.reshape((-1, 28, 28, 1))
    train_images = scale_inputs(train_images)
    test_images = scale_inputs(test_images)
    return (train_images, train_labels), (test_images, test_labels)


def train_mnist(train_epochs=10) -> tf.keras.Model:
    """Trains the MNIST tensorflow model from scratch.

    Args:
        train_epochs (int, optional): Number of epochs to train for. Defaults to 10.

    Returns:
        tf.keras.Model: A trained model.
    """
    (train_images, train_labels), (test_images, test_labels) = get_training_data()
    model = build_model()
    model.compile(loss=tf.keras.losses.sparse_categorical_crossentropy,
                  optimizer=tf.keras.optimizers.Adadelta(),
                  metrics=['accuracy', 'sparse_categorical_crossentropy'])
    model.fit(train_images,
              train_labels,
              epochs=train_epochs,
              validation_data=(test_images, test_labels))

    return model


def deploy_pretrained_model() -> BasetenDeployedModel:
    """Fetches and deploys a pretrained MNIST handwritten digit classifier.

    Returns:
        BasetenDeployedModel: A deployed BaseTen model.
    """
    logger.info('Fetching MNIST model data from s3.')
    model_request = requests.get(MNIST_PRETRAINED_URL)
    logger.info('Fetched MNIST model data from s3.')
    filename = 'model.zip'
    temp_dir = tempfile.TemporaryDirectory()
    model_filepath = os.path.join(temp_dir.name, filename)
    with open(model_filepath, 'wb') as f:
        f.write(model_request.content)
    logger.info('Extracting model contents.')
    with zipfile.ZipFile(model_filepath, 'r') as zip_file:
        zip_file.extractall(temp_dir.name)
    logger.info('Restoring model.')
    tf_model = tf.keras.models.load_model(temp_dir.name)
    logger.info('Deploying model to BaseTen.')
    model = baseten.deploy(tf_model, 'mnist-tensorflow')
    logger.info('Deployed model to BaseTen.')
    return model
