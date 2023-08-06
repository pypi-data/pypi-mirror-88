from abc import ABC

from bci_lib import *
from bci_lib.DataTypes import Stage, Database

from typing import Any, Tuple, List
import numpy as np
import mne
from sklearn import decomposition


class PSD(Stage):
	"""
	DESCRIPTION
	-----------
	Compute the power spectral density (PSD) using multitapers.

	Attributes
	-----------
	id : bci_lib.ID

		id of the stage

	database : bci_lib.Database

		The dictionary which we held all our data in and it's accessible from all stages

	inputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of input datas

	outputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of output datas

	"""
	in_out = {RawData: TwoDFeature, EpochsData: TwoDFeature}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
		DESCRIPTION
		-----------
		The Constructor for PSD

		Parameters
		-----------
		id : bci_lib.ID

			id of the stage

		database : bci_lib.Database

			The dictionary which we held all our data in and it's accessible from all stages

		inputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of input datas

		outputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of output datas
		-----------
		"""
		super(PSD, self).__init__(id, database, inputs, outputs)

		if inputs[0].get_type() is RawData:
			self.set_params = self._set_params_raw

		elif inputs[0].get_type() is EpochsData:
			self.set_params = self._set_params_epoch

		else:
			raise Exception('Input Data type is not RawData nor EpochData')

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database
		-----------
		"""
		labels = []
		features = []
		input_datas_list = self._get_input()
		input_data = input_datas_list[0]
		freq_set = self._params.pop('freq_set')
		if isinstance(input_data, RawData):
			# maybe using 'eeg' in picks in get_data
			input_raw_array = input_data.get_data().get_data(
				picks=self._params['picks'])
			features = np.zeros((input_raw_array.shape[0], len(freq_set)))
			for i in range(len(freq_set)):
				psd_data, freqs = mne.time_frequency.psd_multitaper(inst=input_data.get_data(), fmin=freq_set[i][0],
				                                                    fmax=freq_set[i][1], **self._params)
				features[:, i] = psd_data.sum(axis=2)

			labels = input_data.get_labels("Stim")

		elif isinstance(input_data, EpochsData):
			input_epoch_array = input_data.get_data().get_data(
				picks=self._params['picks'])
			features = np.zeros(
				(input_epoch_array.shape[0], input_epoch_array.shape[1], len(freq_set)))
			for i in range(len(freq_set)):
				psd_data, freqs = mne.time_frequency.psd_multitaper(inst=input_data.get_data(), fmin=freq_set[i][0],
				                                                    fmax=freq_set[i][1], **self._params)
				features[:, :, i] = psd_data.sum(axis=2)

			for i in range(features.shape[0]):
				_, label = input_data.get_data().next(return_event_id=True)
				labels.append(label)
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))
		feature_data = TwoDFeature(id=input_data.get_id(),
		                           data=np.array(features), label=np.array(labels))

		self._set_output(feature_data, self._outputs[0])
		self._params['freq_set'] = freq_set
		self._finish()

	def _set_params_epoch(self, freq_set, tmin=None, tmax=None, bandwidth=None, adaptive=False, low_bias=True,
	                      normalization='length', picks='data', proj=False, n_jobs=1, verbose=None):
		"""
		DESCRIPTION
		-----------
		Compute the power spectral density (PSD) using multitapers.

		Calculates spectral density for orthogonal tapers, then averages them together for each channel/epoch.

		Parameters
		-----------
		inst : instance of Epochs or Raw or Evoked

			The data for PSD calculation.

		fmin : float

			Min frequency of interest.

		fmax : float

			Max frequency of interest.

		tmin : float | None

			Min time of interest.

		tmax : float | None

			Max time of interest.

		bandwidth : float

			The bandwidth of the multi taper windowing function in Hz. The default
			value is a window half-bandwidth of 4.

		adaptive : bool

			Use adaptive weights to combine the tapered spectra into PSD
			(slow, use n_jobs    1 to speed up computation).

		low_bias : bool

			Only use tapers with more than 90% spectral concentration within
			bandwidth.

		normalization : str

			Either "full" or "length" (default). If "full", the PSD will
			be normalized by the sampling rate as well as the length of
			the signal (as in nitime).

		picks : str | list | slice | None

			Channels to include. Slices and lists of integers will be
			interpreted as channel indices. In lists, channel *type* strings
			(e.g., `['meg', 'eeg']`) will pick channels of those
			types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`
			will pick the given channels. Can also be the string values
			"all" to pick all channels, or "data" to pick :term:`data channels`.
			None (default) will pick good data channels(excluding reference MEG channels).

		proj : bool

			Apply SSP projection vectors. If inst is ndarray this is not used.

		n_jobs : int

			The number of jobs to run in parallel (default 1).
			Requires the joblib package.

		verbose : bool, str, int, or None

			If not None, override default verbose level (see :func:`mne.verbose`
			and :ref:`Logging documentation  tut_logging ` for more).

		Example
		-----------

		-----------
		"""
		params_dict = {'freq_set': freq_set, 'tmin': tmin, 'tmax': tmax, 'bandwidth': bandwidth,
		               'adaptive': adaptive, 'low_bias': low_bias, 'normalization': normalization,
		               'picks': picks, 'proj': proj, 'n_jobs': n_jobs, 'verbose': verbose}
		for k, v in params_dict.items():
			self._params[k] = v

	def _set_params_raw(self, freq_set, tmin=None, tmax=None, bandwidth=None, adaptive=False, low_bias=True,
	                    normalization='length', picks='data', proj=False, n_jobs=1, verbose=None):
		"""
		DESCRIPTION
		-----------
		Compute the power spectral density (PSD) using multitapers.

		Calculates spectral density for orthogonal tapers, then averages them together for each channel/epoch.

		Parameters
		-----------
		inst : instance of Epochs or Raw or Evoked

			The data for PSD calculation.

		fmin : float

			Min frequency of interest.

		fmax : float

			Max frequency of interest.

		tmin : float | None

			Min time of interest.

		tmax : float | None

			Max time of interest.

		bandwidth : float

			The bandwidth of the multi taper windowing function in Hz. The default
			value is a window half-bandwidth of 4.

		adaptive : bool

			Use adaptive weights to combine the tapered spectra into PSD
			(slow, use n_jobs    1 to speed up computation).

		low_bias : bool

			Only use tapers with more than 90% spectral concentration within
			bandwidth.

		normalization : str

			Either "full" or "length" (default). If "full", the PSD will
			be normalized by the sampling rate as well as the length of
			the signal (as in nitime).

		picks : str | list | slice | None

			Channels to include. Slices and lists of integers will be
			interpreted as channel indices. In lists, channel *type* strings
			(e.g., `['meg', 'eeg']`) will pick channels of those
			types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`
			will pick the given channels. Can also be the string values
			"all" to pick all channels, or "data" to pick :term:`data channels`.
			None (default) will pick good data channels(excluding reference MEG channels).

		proj : bool

			Apply SSP projection vectors. If inst is ndarray this is not used.

		n_jobs : int

			The number of jobs to run in parallel (default 1).
			Requires the joblib package.

		verbose : bool, str, int, or None

			If not None, override default verbose level (see :func:`mne.verbose`
			and :ref:`Logging documentation  tut_logging ` for more).

		Example
		-----------

		-----------
		"""
		params_dict = {'freq_set': freq_set, 'tmin': tmin, 'tmax': tmax, 'bandwidth': bandwidth,
		               'adaptive': adaptive, 'low_bias': low_bias, 'normalization': normalization,
		               'picks': picks, 'proj': proj, 'n_jobs': n_jobs, 'verbose': verbose}
		for k, v in params_dict.items():
			self._params[k] = v


class PCA(Stage):
	"""
	DESCRIPTION
	-----------
	Principal component analysis (PCA).

	Attributes
	-----------
	id : bci_lib.ID

		id of the stage

	database : bci_lib.Database

		The dictionary which we held all our data in and it's accessible from all stages

	inputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of input datas

	outputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of output datas

	mark_as_test : bool | false

		It can determine whether the data labeled as train(false) or test(true)


	"""
	in_out = {RawData: TwoDFeature, EpochsData: TwoDFeature}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...],
	             mark_as_test: bool = False):
		"""
		DESCRIPTION
		-----------
		The Constructor for PCA

		Parameters
		-----------
		id : bci_lib.ID

			id of the stage

		database : bci_lib.Database

			The dictionary which we held all our data in and it's accessible from all stages

		inputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of input datas

		outputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of output datas

		mark_as_test : bool | false

		It can determine whether the data labeled as train(false) or test(true)

		-----------
		"""
		super(PCA, self).__init__(id, database, inputs, outputs)
		if not isinstance(mark_as_test, bool):
			raise TypeError('mark_as_test is not bool type')
		self.cache = dict()
		self.cache['mark_as_test'] = mark_as_test
		if not mark_as_test:
			self.cache['pca_model'] = None
			self.cache['train_data_shape'] = None
			self.cache['train_data_type'] = None

		if inputs[0].get_type() is RawData:
			self.set_params = self.set_params_pca
		elif inputs[0].get_type() is EpochsData:
			self.set_params = self.set_params_pca
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(inputs[0].get_type()))

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database
		-----------
		"""
		input_datas_list = self._get_input()
		picks = self._params.pop('picks')
		if not self.cache['mark_as_test']:
			input_data_train = input_datas_list[0]
			labels_tr = []
			self.cache['pca_model'] = decomposition.PCA(**self._params)
			if isinstance(input_data_train, RawData):
				self.train_data_type = RawData
				input_array_train = input_data_train.get_data().get_data(picks=picks)
				output_train = np.zeros(
					(input_array_train.shape[0], self._params['n_components']))
				input_array_train = input_array_train.reshape(
					input_array_train.shape[0], -1)
				self.train_data_shape = input_array_train.shape

				self.cache['pca_model'].fit(input_array_train)
				output_train = self.cache['pca_model'].transform(
					input_array_train)

				labels_tr = input_data_train.get_labels("Stim")

			elif isinstance(input_data_train, EpochsData):
				self.cache['train_data_type'] = EpochsData
				input_array_train = input_data_train.get_data().get_data(picks=picks)
				output_train = np.zeros(
					(input_array_train.shape[0], self._params['n_components']))
				input_array_train = input_array_train.reshape(
					input_array_train.shape[0], -1)
				self.cache['train_data_shape'] = input_array_train.shape

				self.cache['pca_model'].fit(input_array_train)
				output_train = self.cache['pca_model'].transform(
					input_array_train)

				for i in range(input_array_train.shape[0]):
					_, label = input_data_train.get_data().next(return_event_id=True)
					labels_tr.append(label)
			else:
				raise Exception('Input Data type is not RawData nor EpochData\n'
				                'input type={}'.format(type(input_data_train)))
			feature_tr = TwoDFeature(id=input_data_train.get_id(), data=np.array(output_train),
			                         label=np.array(labels_tr))
			self._set_output(feature_tr, output_id=self._outputs[0])

		else:
			input_data_test = input_datas_list[0]
			labels_te = []
			input_array_test = input_data_test.get_data().get_data(picks='eeg')
			output_test = np.zeros(
				(input_array_test.shape[0], self._params['n_components']))
			input_array_test = input_array_test.reshape(
				input_array_test.shape[0], -1)
			if self.cache['train_data_shape'][0] == input_array_test.shape[0]:
				if self.cache['train_data_type'] == RawData and isinstance(input_data_test, RawData):
					output_test = self.cache['pca_model'].transform(
						input_array_test)

					labels_te = input_data_test.get_labels("Stim")

				elif self.cache['train_data_type'] == RawData and isinstance(input_data_test, EpochsData):
					input_array_test = input_data_test.get_data().get_data(picks='eeg')
					output_test = np.zeros(
						(input_array_test.shape[0], self._params['n_components']))
					input_array_test = input_array_test.reshape(
						input_array_test.shape[0], -1)

					output_test = self.cache['pca_model'].transform(
						input_array_test)

					for i in range(input_array_test.shape[0]):
						_, label = input_data_test.get_data().next(return_event_id=True)
						labels_te.append(label)
				else:
					raise Exception('Input Data type is not RawData nor EpochData\n'
					                'input type={}'.format(type(input_data_test)))
			else:
				raise Exception('test and train datas shape does not match\n'
				                'test datas shape={}\ntrain datas shape={}'.format(type(input_data_test),
				                                                                   self.cache['train_data_shape']))
			feature_te = TwoDFeature(id=input_data_test.get_id(), data=np.array(output_test),
			                         label=np.array(labels_te))

			self._set_output(feature_te, output_id=self._outputs[0])
		self._params['picks'] = picks
		self._finish()

	def set_params_pca(self, picks='eeg,csd', copy=True, iterated_power='auto', n_compoonents=3, random_state=None,
	                   svd_solver='auto', tol=0.0, whiten=False):
		"""
		DESCRIPTION
		-----------
		Principal component analysis (PCA).

		Linear dimensionality reduction using Singular Value Decomposition of the data to project it to a lower dimensional space. The input data is centered but not scaled for each feature before applying the SVD.

		It uses the LAPACK implementation of the full SVD or a randomized truncated SVD by the method of Halko et al. 2009, depending on the shape of the input data and the number of components to extract.

		It can also use the scipy.sparse.linalg ARPACK implementation of the truncated SVD.

		Notice that this class does not support sparse input. See :class:TruncatedSVD for an alternative with sparse data.

		Parameters
		-----------
		picks : str | list | slice | None

					Channels to include. Slices and lists of integers will be
					interpreted as channel indices. In lists, channel *type* strings
					(e.g., `['meg', 'eeg']`) will pick channels of those
					types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`
					will pick the given channels. Can also be the string values
					"all" to pick all channels, or "data" to pick :term:`data channels`.
					None (default) will pick good data channels(excluding reference MEG channels).

		n_components : int, float, None or str

			Number of components to keep.
			if n_components is not set all components are kept::

				n_components == min(n_samples, n_features)

			If `n_components == 'mle'` and `svd_solver == 'full'`, Minka's
			MLE is used to guess the dimension. Use of `n_components == 'mle'`
			will interpret `svd_solver == 'auto'` as `svd_solver == 'full'`.

			If `0   n_components   1` and `svd_solver == 'full'`, select the
			number of components such that the amount of variance that needs to be
			explained is greater than the percentage specified by n_components.

			If `svd_solver == 'arpack'`, the number of components must be
			strictly less than the minimum of n_features and n_samples.

			Hence, the None case results in::

				n_components == min(n_samples, n_features) - 1

		copy : bool, default=True

			If False, data passed to fit are overwritten and running
			fit(X).transform(X) will not yield the expected results,
			use fit_transform(X) instead.

		whiten : bool, optional (default False)

			When True (False by default) the `components_` vectors are multiplied
			by the square root of n_samples and then divided by the singular values
			to ensure uncorrelated outputs with unit component-wise variances.

			Whitening will remove some information from the transformed signal
			(the relative variance scales of the components) but can sometime
			improve the predictive accuracy of the downstream estimators by
			making their data respect some hard-wired assumptions.

		svd_solver : str {'auto', 'full', 'arpack', 'randomized'}

			If auto :
				The solver is selected by a default policy based on `X.shape` and
				`n_components`: if the input data is larger than 500x500 and the
				number of components to extract is lower than 80% of the smallest
				dimension of the data, then the more efficient 'randomized'
				method is enabled. Otherwise the exact full SVD is computed and
				optionally truncated afterwards.
			If full :
				run exact full SVD calling the standard LAPACK solver via
				`scipy.linalg.svd` and select the components by postprocessing
			If arpack :
				run SVD truncated to n_components calling ARPACK solver via
				`scipy.sparse.linalg.svds`. It requires strictly
				0   n_components   min(X.shape)
			If randomized :
				run randomized SVD by the method of Halko et al.

		tol : float >= 0, optional (default .0)

						Tolerance for singular values computed by svd_solver == 'arpack'.

		iterated_power : int >= 0, or 'auto', (default 'auto')

			Number of iterations for the power method computed by
			svd_solver == 'randomized'.

		random_state : int, RandomState instance or None, optional (default None)

			If int, random_state is the seed used by the random number generator;
			If RandomState instance, random_state is the random number generator;
			If None, the random number generator is the RandomState instance used
			by `np.random`. Used when `svd_solver` == 'arpack' or 'randomized'.

		Examples
		-----------

		-----------
		"""
		if picks == 'eeg,csd':
			picks = ['eeg', 'csd']
		params_dict = {'picks': picks, 'copy': copy, 'iterated_power': iterated_power, 'n_components': n_compoonents,
		               'random_state': random_state, 'svd_solver': svd_solver, 'tol': tol, 'whiten': whiten}
		for k, v in params_dict.items():
			self._params[k] = v


class PowerOnWindows(Stage):
	"""
	DESCRIPTION
	-----------
	Compute the power of signals in given windows.

	Attributes
	-----------
	id : bci_lib.ID

		id of the stage

	database : bci_lib.Database

		The dictionary which we held all our data in and it's accessible from all stages

	inputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of input datas

	outputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of output datas

	"""
	in_out = {RawData: TwoDFeature, EpochsData: TwoDFeature}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
		DESCRIPTION
		-----------
		The Constructor for PowerOnWindows

		Parameters
		-----------
		id : bci_lib.ID

			id of the stage

		database : bci_lib.Database

			The dictionary which we held all our data in and it's accessible from all stages

		inputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of input datas

		outputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of output datas
		-----------
		"""
		super(PowerOnWindows, self).__init__(id, database, inputs, outputs)

		if inputs[0].get_type() is RawData:
			self.set_params = self._set_params_power

		elif inputs[0].get_type() is EpochsData:
			self.set_params = self._set_params_power

		else:
			raise Exception('Input Data type is not RawData nor EpochData')

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database
		-----------
		"""
		labels = []
		features = []
		input_datas_list = self._get_input()
		input_data = input_datas_list[0]
		power_windows = np.arange(self._params['start'], self._params['max_len'] - self._params['windows_length'],
		                          self._params['windows_step'])
		if isinstance(input_data, RawData):
			# maybe using 'eeg' in picks in get_data
			input_raw_array = input_data.get_data().get_data(
				picks=self._params['picks'])
			features = np.zeros((input_raw_array.shape[0], power_windows.shape[0]))
			for num_trial in range(input_raw_array.shape[0]):
				for n in range(power_windows.shape[0]):
					features[num_trial, n] = (np.sum(np.power(
						np.abs(input_raw_array[num_trial,
						       power_windows[n]:power_windows[n] + self._params['windows_length']]),
						2), axis=1)) / (self._params['windows_length'] + 1)

			temp_labels = input_data.get_labels("Stim")
			for l in temp_labels:
				for w in range(len(power_windows.shape[0])):
					labels.append(l)

		elif isinstance(input_data, EpochsData):
			input_epoch_array = input_data.get_data().get_data(
				picks=self._params['picks'])
			features = np.zeros((input_epoch_array.shape[0], input_epoch_array.shape[1], power_windows.shape[0]))
			for num_trial in range(input_epoch_array.shape[0]):
				for n in range(power_windows.shape[0]):
					features[num_trial, :, n] = (np.sum(np.power(
						np.abs(input_epoch_array[num_trial, :,
						       power_windows[n]:power_windows[n] + self._params['windows_length']]),
						2), axis=1)) / (self._params['windows_length'] + 1)
			temp_labels = []
			for i in range(features.shape[0]):
				_, label = input_data.get_data().next(return_event_id=True)
				temp_labels.append(label)
			for l in temp_labels:
				for w in range(len(power_windows.shape[0])):
					labels.append(l)
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))
		feature_data = TwoDFeature(id=input_data.get_id(),
		                           data=np.array(features), label=np.array(labels))

		self._set_output(feature_data, self._outputs[0])
		self._finish()

	def _set_params_power(self, max_len, window_length, window_step, picks=None, start=0):
		"""
				DESCRIPTION
				-----------
				sets set_params for PowerOnWindows

				Parameters
				-----------
				max_len : int

					The length to compute powers on

				window_length : int

					The length of the windows in which we compute total power of signals

				window_step : int

					The step of the moving window

				picks : str | list | slice | None

					Channels to include. Slices and lists of integers will be
					interpreted as channel indices. In lists, channel *type* strings
					(e.g., `['meg', 'eeg']`) will pick channels of those
					types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`
					will pick the given channels. Can also be the string values
					"all" to pick all channels, or "data" to pick :term:`data channels`.
					None (default) will pick good data channels(excluding reference MEG channels).

				start : int

					starting index of moving windows
				-----------
				"""
		params_dict = {'picks': picks, 'max_len': max_len, 'window_length': window_length, 'window_step': window_step,
		               'start': start}
		for k, v in params_dict.items():
			self._params[k] = v


class ICA(Stage):
	"""
	DESCRIPTION
	-----------
	Independent component analysis (ICA).

	Attributes
	-----------
	id : bci_lib.ID

		id of the stage

	database : bci_lib.Database

		The dictionary which we held all our data in and it's accessible from all stages

	inputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of input datas

	outputs : Tuple[ID, ...]

		It's the tuple of some ids(bci_lib.ID) of output datas

	mark_as_test : bool | false

		It can determine whether the data labeled as train(false) or test(true)


	"""
	in_out = {RawData: TwoDFeature, EpochsData: TwoDFeature}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...],
	             mark_as_test: bool = False):
		"""
		DESCRIPTION
		-----------
		The Constructor for ICA

		Parameters
		-----------
		id : bci_lib.ID

			id of the stage

		database : bci_lib.Database

			The dictionary which we held all our data in and it's accessible from all stages

		inputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of input datas

		outputs : Tuple[ID, ...]

			It's the tuple of some ids(bci_lib.ID) of output datas

		mark_as_test : bool | false

		It can determine whether the data labeled as train(false) or test(true)

		-----------
		"""
		super(ICA, self).__init__(id, database, inputs, outputs)
		if not isinstance(mark_as_test, bool):
			raise TypeError('mark_as_test is not bool type')
		self.cache = dict()
		self.cache['mark_as_test'] = mark_as_test
		if not mark_as_test:
			self.cache['ica_model'] = None
			self.cache['train_data_shape'] = None
			self.cache['train_data_type'] = None

		if inputs[0].get_type() is RawData:
			self.set_params = self.set_params_ica
		elif inputs[0].get_type() is EpochsData:
			self.set_params = self.set_params_ica
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(inputs[0].get_type()))

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database
		-----------
		"""
		input_datas_list = self._get_input()
		picks = self._params.pop('picks')
		if not self.cache['mark_as_test']:
			input_data_train = input_datas_list[0]
			labels_tr = []
			self.cache['ica_model'] = decomposition.FastICA(**self._params)
			if isinstance(input_data_train, RawData):
				self.train_data_type = RawData
				input_array_train = input_data_train.get_data().get_data(picks=picks)
				output_train = np.zeros(
					(input_array_train.shape[0], self._params['n_components']))
				input_array_train = input_array_train.reshape(
					input_array_train.shape[0], -1)
				self.train_data_shape = input_array_train.shape

				self.cache['ica_model'].fit(input_array_train)
				output_train = self.cache['ica_model'].transform(
					input_array_train)

				labels_tr = input_data_train.get_labels("Stim")

			elif isinstance(input_data_train, EpochsData):
				self.cache['train_data_type'] = EpochsData
				input_array_train = input_data_train.get_data().get_data(picks=picks)
				output_train = np.zeros(
					(input_array_train.shape[0], self._params['n_components']))
				input_array_train = input_array_train.reshape(
					input_array_train.shape[0], -1)
				self.cache['train_data_shape'] = input_array_train.shape

				self.cache['ica_model'].fit(input_array_train)
				output_train = self.cache['ica_model'].transform(
					input_array_train)

				for i in range(input_array_train.shape[0]):
					_, label = input_data_train.get_data().next(return_event_id=True)
					labels_tr.append(label)
			else:
				raise Exception('Input Data type is not RawData nor EpochData\n'
				                'input type={}'.format(type(input_data_train)))
			feature_tr = TwoDFeature(id=input_data_train.get_id(), data=np.array(output_train),
			                         label=np.array(labels_tr))
			self._set_output(feature_tr, output_id=self._outputs[0])

		else:
			input_data_test = input_datas_list[0]
			labels_te = []
			input_array_test = input_data_test.get_data().get_data(picks='eeg')
			output_test = np.zeros(
				(input_array_test.shape[0], self._params['n_components']))
			input_array_test = input_array_test.reshape(
				input_array_test.shape[0], -1)
			if self.cache['train_data_shape'][0] == input_array_test.shape[0]:
				if self.cache['train_data_type'] == RawData and isinstance(input_data_test, RawData):
					output_test = self.cache['ica_model'].transform(
						input_array_test)

					labels_te = input_data_test.get_labels("Stim")

				elif self.cache['train_data_type'] == RawData and isinstance(input_data_test, EpochsData):
					input_array_test = input_data_test.get_data().get_data(picks='eeg')
					output_test = np.zeros(
						(input_array_test.shape[0], self._params['n_components']))
					input_array_test = input_array_test.reshape(
						input_array_test.shape[0], -1)

					output_test = self.cache['ica_model'].transform(
						input_array_test)

					for i in range(input_array_test.shape[0]):
						_, label = input_data_test.get_data().next(return_event_id=True)
						labels_te.append(label)
				else:
					raise Exception('Input Data type is not RawData nor EpochData\n'
					                'input type={}'.format(type(input_data_test)))
			else:
				raise Exception('test and train datas shape does not match\n'
				                'test datas shape={}\ntrain datas shape={}'.format(type(input_data_test),
				                                                                   self.cache['train_data_shape']))
			feature_te = TwoDFeature(id=input_data_test.get_id(), data=np.array(output_test),
			                         label=np.array(labels_te))

			self._set_output(feature_te, output_id=self._outputs[0])
		self._params['picks'] = picks
		self._finish()

	def set_params_ica(self, picks='eeg,csd', n_components=None, algorithm='parallel', whiten=True,
	                   fun='logcosh', fun_args=None, max_iter=200, tol=0.0001, w_init=None, random_state=None):
		"""FastICA: a fast algorithm for Independent Component Analysis.

		Parameters
		----------
		n_components : int, optional
		Number of components to use. If none is passed, all are used.
		algorithm : {'parallel', 'deflation'}
		Apply parallel or deflational algorithm for FastICA.
		whiten : boolean, optional
		If whiten is false, the data is already considered to be
		whitened, and no whitening is performed.
		fun : string or function, optional. Default: 'logcosh'
		The functional form of the G function used in the
		approximation to neg-entropy. Could be either 'logcosh', 'exp',
		or 'cube'.
		You can also provide your own function. It should return a tuple
		containing the value of the function, and of its derivative, in the
		point. Example:
		def my_g(x):
		    return x ** 3, (3 * x ** 2).mean(axis=-1)
		fun_args : dictionary, optional
		Arguments to send to the functional form.
		If empty and if fun='logcosh', fun_args will take value
		{'alpha' : 1.0}.
		max_iter : int, optional
		Maximum number of iterations during fit.
		tol : float, optional
		Tolerance on update at each iteration.
		w_init : None of an (n_components, n_components) ndarray
		The mixing matrix to be used to initialize the algorithm.
		random_state : int, RandomState instance, default=None
		Used to initialize ``w_init`` when not specified, with a
		normal distribution. Pass an int, for reproducible results
		across multiple function calls.

		Examples
		--------
		 from sklearn.datasets import load_digits
		 from sklearn.decomposition import FastICA
		 X, _ = load_digits(return_X_y=True)
		 transformer = FastICA(n_components=7,
		...         random_state=0)
		 X_transformed = transformer.fit_transform(X)
		 X_transformed.shape
		(1797, 7)
		Notes
		-----
		Implementation based on
		*A. Hyvarinen and E. Oja, Independent Component Analysis:
		Algorithms and Applications, Neural Networks, 13(4-5), 2000,
		pp. 411-430*
		"""
		if picks == 'eeg,csd':
			picks = ['eeg', 'csd']
		params_dict = {'picks': picks,
		               'n_components': n_components, 'algorithm': algorithm, 'whiten': whiten, 'fun': fun,
		               'fun_args': fun_args,
		               'max_iter': max_iter, 'tol': tol, 'w_init': w_init, 'random_state': random_state}
		for k, v in params_dict.items():
			self._params[k] = v
