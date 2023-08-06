# import the necessary packages
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications import imagenet_utils
import tensorflow as tf
import numpy as np
import cv2

class GradCAM:
	def __init__(self, model, layerName=None):
		self.model = model
		self.layerName = layerName

		# if the layer name is None, attempt to automatically find the target output layer
		if self.layerName is None:
			self.layerName = self.find_target_layer()

	def find_target_layer(self):
		# attempt to find the final convolutional layer in the network by looping over the layers of the network
		# in reverse order
		for layer in reversed(self.model.layers):
			# check to see if the layer has a 4D output
			if len(layer.output_shape) == 4:
				return layer.name
		raise ValueError("Could not find 4D layer. Cannot apply GradCAM.")

	def compute_heatmap(self, image, classIdx, eps=1e-8):
		# construct our gradient model by supplying (1) the inputs to our pre-trained model, (2) the output of
		# the (presumably) final 4D layer in the network, and (3) the output of the softmax activations from the model
		gradModel = Model(
			inputs=[self.model.inputs],
			outputs=[self.model.get_layer(self.layerName).output, 
				self.model.output])

		# record operations for automatic differentiation
		with tf.GradientTape() as tape:
			# cast the image tensor to a float-32 data type, pass the image through the gradient model, and grab the loss
			# associated with the specific class index
			inputs = tf.cast(image, tf.float32)
			(convOutputs, predictions) = gradModel(inputs)
			loss = predictions[:, classIdx]

		# use automatic differentiation to compute the gradients
		grads = tape.gradient(loss, convOutputs)

		# compute the guided gradients
		castConvOutputs = tf.cast(convOutputs > 0, "float32")
		castGrads = tf.cast(grads > 0, "float32")
		guidedGrads = castConvOutputs * castGrads * grads

		# the convolution and guided gradients have a batch dimension (which we don't need) so let's grab the volume
		# itself and discard the batch
		convOutputs = convOutputs[0]
		guidedGrads = guidedGrads[0]

		# compute the average of the gradient values, and using them as weights, compute the ponderation of the filters
		# with respect to the weights
		weights = tf.reduce_mean(guidedGrads, axis=(0, 1))
		cam = tf.reduce_sum(tf.multiply(weights, convOutputs), axis=-1)

		# grab the spatial dimensions of the input image and resize the output class activation map to match the input
		# image dimensions
		(w, h) = (image.shape[2], image.shape[1])
		heatmap = cv2.resize(cam.numpy(), (w, h))

		# normalize the heatmap such that all values lie in the range [0, 1], scale the resulting values to the range
		# [0, 255],  and then convert to an unsigned 8-bit integer
		numer = heatmap - np.min(heatmap)
		denom = (heatmap.max() - heatmap.min()) + eps
		heatmap = numer / denom
		heatmap = ((heatmap * -255) + 255).astype("uint8")
		return heatmap

	def overlay_heatmap(self, heatmap, image, alpha, colormap=cv2.COLORMAP_JET):
		# apply the supplied color map to the heatmap and then overlay the heatmap on the input image
		heatmap = cv2.applyColorMap(heatmap, colormap)
		output = cv2.addWeighted(image, alpha, heatmap, 1 - alpha, 0)
		return heatmap, output

	def make_superimposed_img(self, image, img_path, alpha=0.5):
		image = np.expand_dims(image, axis=0)
		preds = self.model.predict(image)
		classIdx = np.argmax(preds[0])
		heatmap = self.compute_heatmap(image, classIdx)

		orig = cv2.imread(img_path)
		heatmap = cv2.resize(heatmap, (orig.shape[1], orig.shape[0]))
		(heatmap, output) = self.overlay_heatmap(heatmap, orig, alpha)
		return heatmap, output