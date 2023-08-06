import numpy as np
from keras import models
import matplotlib.pyplot as plt


class IntermediateActivations:
    def __init__(self, model):
        self.model = model
        self.layer_name = None

    def plot_intermediate_activations(self, img, images_per_row=8, layer_name=None):
        img_tensor = np.expand_dims(img, axis=0)

        if layer_name is None:
            layers_output = [layer.output for layer in self.model.layers if 'conv2d' in layer.name]
            layer_names = [layer.name for layer in self.model.layers if 'conv2d' in layer.name]
        else:
            self.layer_name = layer_name
            layers_output = [self.model.get_layer(layer_name).output]
            layer_names = [layer_name]

        activation_model = models.Model(inputs=self.model.input, outputs=layers_output)
        activations = activation_model.predict(img_tensor)

        for layer_name, layer_activation in zip(layer_names, activations):
            # (1, size, size, nr_of_features)
            nr_of_features = layer_activation.shape[-1]
            size = layer_activation.shape[1]
            nr_of_rows = nr_of_features // images_per_row
            margin = 1
            grid = np.zeros(((size + margin) * nr_of_rows, (size + margin) * images_per_row))

            for row in range(nr_of_rows):
                for col in range(images_per_row):
                    if self.layer_name is None:
                        channel_img = layer_activation[0, :, :, row * images_per_row + col]
                    else:
                        channel_img = layer_activation[:, :, row * images_per_row + col]
                    channel_img -= channel_img.mean()
                    channel_img /= channel_img.std()
                    channel_img *= 64
                    channel_img += 128
                    channel_img = np.clip(channel_img, 0, 255).astype('uint8')
                    horizontal_start = row * size + row * margin
                    horizontal_end = horizontal_start + size
                    vertical_start = col * size + col * margin
                    vertical_end = vertical_start + size
                    grid[horizontal_start: horizontal_end, vertical_start: vertical_end] = channel_img

            scale = 1 / size
            plt.figure(figsize=(2 * scale * grid.shape[1], 2 * scale * grid.shape[0]))
            plt.title(layer_name)
            plt.imshow(grid, aspect='auto')
        plt.show()
