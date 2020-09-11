from ml_tutor.model import BaseModelClustering

import time
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


class KMeans(BaseModelClustering):

	def __init__(self, n_clusters=2, tolerance=0.001, max_iter=300, visual_training=True):
		"""

		:param n_clusters:
		:param tolerance:
		:param max_iter:
		:param visual_training:
		"""
		super(BaseModelClustering, self).__init__()

		self.k_clusters = n_clusters
		self.tol = tolerance
		self.max_iter = max_iter

		# Visualization related parameters
		self.pca = PCA(n_components=2)
		self.visual_training = visual_training
		if not super().__is_visual_on__():
			self.visual_training = False
			print("Visualization is only supported in Jupyter Notebook and Google Colab.")

		# These two lists will be used to store mid steps for centroids and data, so we can visualize each step
		self.clustered_data_history = []
		self.centroids_history = []

	def fit(self, X):
		"""
		Train the model using features (X) as training data.

		:param X: Features from a dataset
		"""

		self.X = X

		if self.X.shape[1] > 2:
			if self.visual_training:
				print("The dataset is sparse for visual training. It will be pre-processed so it can be visualized.")
				print("Current shape of your data: {}".format(self.X.shape))
				self.X = self.pca.fit_transform(self.X)
				print("New shape of your data: {}".format(self.X.shape))

		# Starting clusters will be random members from X set
		self.centroids = []

		for i in range(self.k_clusters):
			# this index is used to acces random element from input set
			index = random.randint(1, len(self.X) - 1)
			self.centroids.append(self.X[index])

		for i in range(self.max_iter):
			# storing previous values of centroids
			prev_centroids = self.centroids
			# This will be dict for plotting data later on
			# with it we can find data points which are in the some cluster

			self.clustered_data = {}
			# Centroids values for this iteration
			cen_temp = []

			diffs = []
			for centroid in self.centroids:
				diffs.append(np.linalg.norm(self.X - centroid, axis=1))

			diffs = np.argmin(np.vstack(diffs).T, axis=1)

			for c in range(len(self.centroids)):
				closer_samples = self.X[diffs == c]
				self.clustered_data[c] = closer_samples
				cen_temp.append(np.average(closer_samples, axis=0))

			# Saving data and centroids for visual training
			if self.visual_training:
				self.clustered_data_history.append(self.clustered_data)
				self.centroids_history.append(self.centroids)

			# Check if it is optimized
			optimized = True
			for c in range(len(self.centroids)):
				original_centroid = prev_centroids[c]
				current_centroid = cen_temp[c]
				if np.abs(np.sum((current_centroid - original_centroid) / original_centroid * 100.0)) > self.tol:
					optimized = False
					self.centroids = cen_temp

			if optimized:
				break

		if self.visual_training:
			self.__visual_training__()

	def __visual_training__(self):
		"""
		Helper function used to crete real time visualization of the training process.
		"""
		# Import only relevant libraries for Jupyter Notebook if needed
		from IPython import display

		for i in range(len(self.centroids_history)):

			data = self.clustered_data_history[i]
			centroids = self.centroids_history[i]

			plt.close()
			plt.clf()
			plt.figure(figsize=(12, 10))

			for k in range(self.k_clusters):
				plt.scatter(np.vstack(data[k])[:, 0], np.vstack(data[k])[:, 1], label="Cluster {} data samples".format(k))

			centroid_vis = False
			for p in range(self.k_clusters):
				if not centroid_vis:
					plt.scatter(centroids[p][0], centroids[p][1], s=150,
					            c='black', marker="s", label="Centroid")
					centroid_vis = True
				else:
					plt.scatter(centroids[p][0], centroids[p][1], s=150,
					            c='black', marker="s")

			plt.title("K-Means - Training process")
			plt.legend(framealpha=1, frameon=True)

			display.display(plt.gcf())
			display.display()
			time.sleep(1)
			display.clear_output(wait=True)

	def predict(self, X):
		"""
		This method performs predictions on the unseen data from your dataset.

		:param X: Data samples used to perform prediction on. (Generally a test set)
		:return: Predicted labels for each data sample
		"""

		if X.shape[1] > 2:
			if self.visual_training:
				X = self.pca.transform(X)

		diffs = []
		for centroid in self.centroids:
			diffs.append(np.linalg.norm(X - centroid, axis=1))

		predictions = np.argmin(np.vstack(diffs).T, axis=1)

		return predictions

	def sklearn_version(self):
		"""
		Auto-generates sklearn code for a selected algorithm.

		NOTE: This function will automatically add one more code cell to your Jupyter Notebook/Google Colab (with the sklearn code inside).
		"""
		if not super().__is_visual_on__():
			print("Supported only in Jupyter Notebook and Google Colab.")
			return NotImplementedError
		if super().__is_google_colab__():
			return "This method is not supported in Google Colab for now :/"

		from IPython.core.getipython import get_ipython
		contents = """
# If you don't have Sklearn installed execute line below
# pip install sklearn

# This is how you can import KMeans using sklearn library
from sklearn.cluster import KMeans

# Define classifier with selected parameters
model = KMeans(n_clusters=3)

# Train the model using dataset you desire
model.fit(X_train)

# Finally, use trained model to make predictions
predictions = model.predict(X_test)
"""
		shell = get_ipython()
		payload = dict(
			source='set_next_input',
			text=contents,
			replace=False,
		)
		shell.payload_manager.write_payload(payload, single=False)

	def how_it_works(self):
		"""
		Generates theory on how the algorithm works right in the Jupyter Notebook/Google colab.
		"""
		if not super().__is_visual_on__():
			print("Supported only in Jupyter Notebook and Google Colab.")
			return NotImplementedError

		from IPython.core.getipython import get_ipython
		if super().__is_google_colab__():
			content = u"""
# K-Means

[TBA] Theory for K-Means will be added here in a few days.		
"""
			get_ipython().run_cell_magic(u'html', u'', content)
		else:
			content = u"""
# K-Means

[TBA] Theory for K-Means will be added here in a few days.		
"""
			get_ipython().run_cell_magic(u'markdown', u'', content)

	def interview_questions(self):
		"""
		Generates commonly asked interview questions about the algorithm in the Jupyter Notebook/Google colab.
		"""
		if not super().__is_visual_on__():
			print("Supported only in Jupyter Notebook and Google Colab.")
			return NotImplementedError

		from IPython.core.getipython import get_ipython

		if super().__is_google_colab__():
			content = u"""
# K-Means Interview Questions

[TBA] Interview questions for K-Means will be added here in a few days.		
"""
			get_ipython().run_cell_magic(u'html', u'', content)
		else:
			content = u"""
# K-Means Interview Questions

[TBA] Interview questions for K-Means will be added here in a few days.		
"""
			get_ipython().run_cell_magic(u'markdown', u'', content)
