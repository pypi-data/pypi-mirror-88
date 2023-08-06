from abc import ABC
import numpy as np
import mne
from sklearn.model_selection import train_test_split
from bci_lib import *
from bci_lib.DataTypes import *


class BandPassFilter(Stage):
	"""
    DESCRIPTION
    -----------
    Filter a subset of channels.

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
	in_out = {RawData: RawData, EpochsData: EpochsData}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
        DESCRIPTION
        -----------
        The Constructor for BandPassFilter

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
		super(BandPassFilter, self).__init__(id, database, inputs, outputs)

		if inputs[0].get_type() is RawData:
			self.set_params = self._set_params_raw

		elif inputs[0].get_type() is EpochsData:
			self.set_params = self._set_params_epoch

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
		input_data = input_datas_list[0]
		if isinstance(input_data, RawData):
			params = self.get_params()
			filtered_data = input_data.get_data().filter(**params)
			output = RawData(input_data.get_id(), filtered_data)
			self._set_output(output, self._outputs[0])
			del filtered_data, output
		elif isinstance(input_data, EpochsData):
			params = self.get_params()
			filtered_data = input_data.get_data().filter(**params)
			output = EpochsData(input_data.get_id(), filtered_data)
			self._set_output(output, self._outputs[0])
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))
		self._finish()

	def _set_params_raw(self, l_freq, h_freq, picks=None, filter_length='auto', l_trans_bandwidth='auto',
	                    h_trans_bandwidth='auto', n_jobs=1, method='fir', iir_params=None, phase='zero',
	                    fir_window='hamming', fir_design='firwin', skip_by_annotation='edge', pad='edge',
	                    verbose=None):
		"""
        DESCRIPTION
        -----------
        Filter a subset of channels.

        Parameters
        -----------
        l_freq : float | None

            For FIR filters, the lower pass-band edge; for IIR filters, the lower  
            cutoff frequency. If None the data are only low-passed. 

        h_freq : float | None

            For FIR filters, the upper pass-band edge; for IIR filters, the upper  
            cutoff frequency. If None the data are only high-passed. 

        picks : str | list | slice | None

            Channels to include. Slices and lists of integers will be  
            interpreted as channel indices. In lists, channel *type* strings  
            (e.g., `['meg', 'eeg']`) will pick channels of those  
            types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`  
            will pick the given channels. Can also be the string values  
            "all" to pick all channels, or "data" to pick :term:`data channels`.  
            None (default) will pick all data channels.  

        filter_length : str | int

            Length of the FIR filter to use (if applicable):  

            * **'auto' (default)**: The filter length is chosen based  
            on the size of the transition regions (6.6 times the reciprocal  
            of the shortest transition band for fir_window='hamming'  
            and fir_design="firwin2", and half that for "firwin").  
            * **str**: A human-readable time in  
            units of "s" or "ms" (e.g., "10s" or "5500ms") will be  
            converted to that number of samples if `phase="zero"`, or  
            the shortest power-of-two length at least that duration for  
            `phase="zero-double"`.  
            * **int**: Specified length in samples. For fir_design="firwin",  
            this should not be used.  

        l_trans_bandwidth : float | str

            Width of the transition band at the low cut-off frequency in Hz  
            (high pass or cutoff 1 in bandpass). Can be "auto"  
            (default) to use a multiple of `l_freq`::  

                min(max(l_freq * 0.25, 2), l_freq)  

            Only used for `method='fir'`.  

        h_trans_bandwidth : float | str

            Width of the transition band at the high cut-off frequency in Hz  
            (low pass or cutoff 2 in bandpass). Can be "auto"  
            (default in 0.14) to use a multiple of `h_freq`::  

                min(max(h_freq * 0.25, 2.), info['sfreq'] / 2. - h_freq)  

            Only used for `method='fir'`.  

        n_jobs : int | str

            Number of jobs to run in parallel. Can be 'cuda' if `cupy`  
            is installed properly and method='fir'.  
        method : str

                'fir' will use overlap-add FIR filtering, 'iir' will use IIR  
                forward-backward filtering (via filtfilt).  

        iir_params : dict | None

            Dictionary of parameters to use for IIR filtering.  
            If iir_params is None and method="iir", 4th order Butterworth will be used.  
            For more information, see :func:`mne.filter.construct_iir_filter`.  

        phase : str

            Phase of the filter, only used if `method='fir'`.  
            Symmetric linear-phase FIR filters are constructed, and if `phase='zero'`  
            (default), the delay of this filter is compensated for, making it  
            non-causal. If `phase=='zero-double'`,  
            then this filter is applied twice, once forward, and once backward  
            (also making it non-causal). If 'minimum', then a minimum-phase filter will  
            be constricted and applied, which is causal but has weaker stop-band  
            suppression.  

        fir_window : str

            The window to use in FIR design, can be "hamming" (default),  
            "hann" (default in 0.13), or "blackman".  

        fir_design : str

            Can be "firwin" (default) to use :func:`scipy.signal.firwin`,  
            or "firwin2" to use :func:`scipy.signal.firwin2`. "firwin" uses  
            a time-domain design technique that generally gives improved  
            attenuation using fewer samples than "firwin2".  

        skip_by_annotation : str | list of str

            If a string (or list of str), any annotation segment that begins  
            with the given string will not be included in filtering, and  
            segments on either side of the given excluded annotated segment  
            will be filtered separately (i.e., as independent signals).  
            The default (`('edge', 'bad_acq_skip')` will separately filter  
            any segments that were concatenated by :func:`mne.concatenate_raws`  
            or :meth:`mne.io.Raw.append`, or separated during acquisition.  
            To disable, provide an empty list. Only used if `inst` is raw.  

        pad : str

            The type of padding to use. Supports all :func:`numpy.pad` `mode`  
            options. Can also be "reflect_limited", which pads with a  
            reflected version of each vector mirrored on the first and last  
            values of the vector, followed by zeros. Only used for `method='fir'`.

        verbose : bool, str, int, or None

            If not None, override default verbose level (see :func:`mne.verbose`  
            and :ref:`Logging documentation  tut_logging ` for more). Defaults to self.verbose.  

        Example
        -----------

        -----------
        """
		temp_params = {'l_freq': l_freq, 'h_freq': h_freq, 'picks': picks, 'filter_length': filter_length,
		               'l_trans_bandwidth': l_trans_bandwidth, 'h_trans_bandwidth': h_trans_bandwidth,
		               'n_jobs': n_jobs, 'method': method, 'iir_params': iir_params, 'phase': phase,
		               'fir_window': fir_window, 'fir_design': fir_design,
		               'skip_by_annotation': skip_by_annotation, 'pad': pad, 'verbose': verbose}
		for k, v in temp_params.items():
			self._params[k] = v

	def _set_params_epoch(self, l_freq, h_freq, picks=None, filter_length='auto', l_trans_bandwidth='auto',
	                      h_trans_bandwidth='auto', n_jobs=1, method='fir', iir_params=None, phase='zero',
	                      fir_window='hamming', fir_design='firwin', skip_by_annotation='edge', pad='edge',
	                      verbose=None):
		"""
        DESCRIPTION
        -----------
        Filter a subset of channels.

        Parameters
        -----------
        l_freq : float | None

            For FIR filters, the lower pass-band edge; for IIR filters, the lower  
            cutoff frequency. If None the data are only low-passed. 

        h_freq : float | None

            For FIR filters, the upper pass-band edge; for IIR filters, the upper  
            cutoff frequency. If None the data are only high-passed. 

        picks : str | list | slice | None

            Channels to include. Slices and lists of integers will be  
            interpreted as channel indices. In lists, channel *type* strings  
            (e.g., `['meg', 'eeg']`) will pick channels of those  
            types, channel *name* strings (e.g., `['MEG0111', 'MEG2623']`  
            will pick the given channels. Can also be the string values  
            "all" to pick all channels, or "data" to pick :term:`data channels`.  
            None (default) will pick all data channels.  

        filter_length : str | int

            Length of the FIR filter to use (if applicable):  

            * **'auto' (default)**: The filter length is chosen based  
            on the size of the transition regions (6.6 times the reciprocal  
            of the shortest transition band for fir_window='hamming'  
            and fir_design="firwin2", and half that for "firwin").  
            * **str**: A human-readable time in  
            units of "s" or "ms" (e.g., "10s" or "5500ms") will be  
            converted to that number of samples if `phase="zero"`, or  
            the shortest power-of-two length at least that duration for  
            `phase="zero-double"`.  
            * **int**: Specified length in samples. For fir_design="firwin",  
            this should not be used.  

        l_trans_bandwidth : float | str

            Width of the transition band at the low cut-off frequency in Hz  
            (high pass or cutoff 1 in bandpass). Can be "auto"  
            (default) to use a multiple of `l_freq`::  

                min(max(l_freq * 0.25, 2), l_freq)  

            Only used for `method='fir'`.  

        h_trans_bandwidth : float | str

            Width of the transition band at the high cut-off frequency in Hz  
            (low pass or cutoff 2 in bandpass). Can be "auto"  
            (default in 0.14) to use a multiple of `h_freq`::  

                min(max(h_freq * 0.25, 2.), info['sfreq'] / 2. - h_freq)  

            Only used for `method='fir'`.  

        n_jobs : int | str

            Number of jobs to run in parallel. Can be 'cuda' if `cupy`  
            is installed properly and method='fir'.  
        method : str

                'fir' will use overlap-add FIR filtering, 'iir' will use IIR  
                forward-backward filtering (via filtfilt).  

        iir_params : dict | None

            Dictionary of parameters to use for IIR filtering.  
            If iir_params is None and method="iir", 4th order Butterworth will be used.  
            For more information, see :func:`mne.filter.construct_iir_filter`.  

        phase : str

            Phase of the filter, only used if `method='fir'`.  
            Symmetric linear-phase FIR filters are constructed, and if `phase='zero'`  
            (default), the delay of this filter is compensated for, making it  
            non-causal. If `phase=='zero-double'`,  
            then this filter is applied twice, once forward, and once backward  
            (also making it non-causal). If 'minimum', then a minimum-phase filter will  
            be constricted and applied, which is causal but has weaker stop-band  
            suppression.  

        fir_window : str

            The window to use in FIR design, can be "hamming" (default),  
            "hann" (default in 0.13), or "blackman".  

        fir_design : str

            Can be "firwin" (default) to use :func:`scipy.signal.firwin`,  
            or "firwin2" to use :func:`scipy.signal.firwin2`. "firwin" uses  
            a time-domain design technique that generally gives improved  
            attenuation using fewer samples than "firwin2".  

        skip_by_annotation : str | list of str

            If a string (or list of str), any annotation segment that begins  
            with the given string will not be included in filtering, and  
            segments on either side of the given excluded annotated segment  
            will be filtered separately (i.e., as independent signals).  
            The default (`('edge', 'bad_acq_skip')` will separately filter  
            any segments that were concatenated by :func:`mne.concatenate_raws`  
            or :meth:`mne.io.Raw.append`, or separated during acquisition.  
            To disable, provide an empty list. Only used if `inst` is raw.  

        pad : str

            The type of padding to use. Supports all :func:`numpy.pad` `mode`  
            options. Can also be "reflect_limited", which pads with a  
            reflected version of each vector mirrored on the first and last  
            values of the vector, followed by zeros. Only used for `method='fir'`.

        verbose : bool, str, int, or None

            If not None, override default verbose level (see :func:`mne.verbose`  
            and :ref:`Logging documentation  tut_logging ` for more). Defaults to self.verbose.  

        Example
        -----------

        -----------
        """
		temp_params = {'l_freq': l_freq, 'h_freq': h_freq, 'picks': picks, 'filter_length': filter_length,
		               'l_trans_bandwidth': l_trans_bandwidth, 'h_trans_bandwidth': h_trans_bandwidth,
		               'n_jobs': n_jobs, 'method': method, 'iir_params': iir_params, 'phase': phase,
		               'fir_window': fir_window, 'fir_design': fir_design,
		               'skip_by_annotation': skip_by_annotation, 'pad': pad, 'verbose': verbose}
		for k, v in temp_params.items():
			self._params[k] = v


class RawDataToEpochsData(Stage):
	"""
    DESCRIPTION
    -----------
    Epochs extracted from a Raw instance.

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
	in_out = {RawData: EpochsData}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
        DESCRIPTION
        -----------
        The Constructor for RawToEpochsData

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
		super(RawDataToEpochsData, self).__init__(
			id, database, inputs, outputs)

		if inputs[0].get_type() is RawData:
			self.set_params = self._set_params_raw

		else:
			raise Exception('Input Data type is not RawData\n'
			                'input type={}'.format(inputs[0].get_type()))

	def _set_params_raw(self, tmin: float = -0.1, tmax: float = 0.3):
		"""
        DESCRIPTION
        -----------
        Epochs extracted from a Raw instance.

        Parameters
        -----------
        tmin : float

                Start time before event. If nothing is provided, defaults to -0.2.  

        tmax : float

                End time after event. If nothing is provided, defaults to 0.5.  

        Example
        -----------

        -----------
        """
		temp_params = {"tmin": tmin, "tmax": tmax}
		for k, v in temp_params.items():
			self._params[k] = v

	def do_task(self):
		"""
        DESCRIPTION
        -----------
        Imports input from database and performs the task on it and saves output to database
        -----------
        """
		input_datas_list = self._get_input()
		raw_data = input_datas_list[0]
		raw = raw_data.get_data()
		event = mne.find_events(raw=raw, stim_channel="Stim", shortest_event=1)
		epochs = mne.Epochs(raw=raw, events=event, baseline=(None, None), tmin=self._params["tmin"],
		                    tmax=self._params["tmax"])
		epochs.load_data()
		epochs.drop_channels(ch_names=["Stim"])
		epoch_data = EpochsData(id=raw_data.get_id(), data=epochs)

		self._set_output(epoch_data, self._outputs[0])
		del epochs, epoch_data, event, raw, raw_data, input_datas_list
		self._finish()


class TestTrainSplit(Stage):
	"""
    DESCRIPTION
    -----------
    Split arrays or matrices into random train and test subsets

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
	in_out = {EpochsData: EpochsData}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
        DESCRIPTION
        -----------
        The Constructor for TestTrainSplit 

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
		super(TestTrainSplit, self).__init__(id, database, inputs, outputs)

		if inputs[0].get_type() is not EpochsData:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(inputs[0].get_type()))

	def set_params(self, test_size=None, train_size=None, random_state=None, shuffle=True, stratify=None):
		"""
        DESCRIPTION
        -----------
        Split arrays or matrices into random train and test subsets

        Quick utility that wraps input validation and next(ShuffleSplit().split(X, y)) and application to input data into a single call for splitting (and optionally subsampling) data in a oneliner.

        Parameters
        -----------
        *arrays : sequence of indexables with same length / shape[0]  
                Allowed inputs are lists, numpy arrays, scipy-sparse  
                matrices or pandas dataframes.  

        test_size : float, int or None, optional (default=None)

                If float, should be between 0.0 and 1.0 and represent the proportion  
                of the dataset to include in the test split. If int, represents the  
                absolute number of test samples. If None, the value is set to the  
                complement of the train size. If `train_size` is also None, it will  
                be set to 0.25.  

        train_size : float, int, or None, (default=None)

                If float, should be between 0.0 and 1.0 and represent the  
                proportion of the dataset to include in the train split. If  
                int, represents the absolute number of train samples. If None,  
                the value is automatically set to the complement of the test size.  

        random_state : int, RandomState instance or None, optional (default=None)

                If int, random_state is the seed used by the random number generator;  
                If RandomState instance, random_state is the random number generator;  
                If None, the random number generator is the RandomState instance used  
                by `np.random`.  

        shuffle : boolean, optional (default=True)

                Whether or not to shuffle the data before splitting. If shuffle=False  
                then stratify must be None.  

        stratify : array-like or None (default=None)

                If not None, data is split in a stratified fashion, using this as  
                the class labels.  

        Examples
        -----------

        -----------
        """
		self._params = {'test_size': test_size, 'train_size': train_size, 'random_state': random_state,
		                'shuffle': shuffle,
		                'stratify': stratify}

	def do_task(self):
		"""
        DESCRIPTION
        -----------
        Imports input from database and performs the task on it and saves output to database
        -----------
        """
		input_datas_list = self._get_input()
		input_data = input_datas_list[0]
		if isinstance(input_data, EpochsData):
			params = self.get_params()
			data_epochs = input_data.get_data()
			data_array = data_epochs.get_data()

			idx = np.arange(0, data_array.shape[0])
			idx_train, idx_test = train_test_split(idx, **params)
			indices_train = np.ones(data_array.shape[0])
			indices_train[idx_train] = 0
			indices_train = (indices_train == 1)
			indices_test = np.ones(data_array.shape[0])
			indices_test[idx_test] = 0
			indices_test = (indices_test == 1)

			train_epoch = data_epochs.copy()
			train_epoch.drop(indices_train)
			train_output = EpochsData(id=input_data.get_id(), data=train_epoch)

			test_epoch = data_epochs.copy()
			test_epoch.drop(indices_test)
			test_output = EpochsData(id=input_data.get_id(), data=test_epoch)

			self._set_output(train_output, self._outputs[0])
			self._set_output(test_output, self._outputs[1])

		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))


class LaplacianFilter(Stage):
	"""
    DESCRIPTION
    -----------
    Get the current source density (CSD) transformation.

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
	in_out = {RawData: RawData, EpochsData: EpochsData}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
        DESCRIPTION
        -----------
        The Constructor for LaplacianFilter 

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
		super().__init__(id, database, inputs, outputs)

		if (inputs[0].get_type() is RawData) or (inputs[0].get_type() is EpochsData):
			self.set_params = self.set_params_Laplacian
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
		input_data = input_datas_list[0]
		params = self._params
		if isinstance(input_data, RawData):
			raw_data = input_data.get_data()
			filtered_data = mne.preprocessing.compute_current_source_density(
				raw_data, **params)
			output = RawData(input_data.get_id(), filtered_data)
			self._set_output(output, self._outputs[0])
		elif isinstance(input_data, EpochsData):
			epochs_data = input_data.get_data()
			filtered_data = mne.preprocessing.compute_current_source_density(
				epochs_data, **params)
			output = EpochsData(input_data.get_id(), filtered_data)
			self._set_output(output, self._outputs[0])
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))
		self._finish()

	def set_params_Laplacian(self, sphere='auto', lambda2=1e-05, stiffness=4, n_legendre_terms=50, copy=True):
		"""
        DESCRIPTION
        -----------
        Get the current source density (CSD) transformation.

        Parameters
                -----------
        sphere : array-like, shape (4,) | str

                The sphere, head-model of the form (x, y, z, r) where x, y, z  
                is the center of the sphere and r is the radius in meters.  
                Can also be "auto" to use a digitization-based fit.  

        lambda2 : float

                Regularization parameter, produces smoothness. Defaults to 1e-5.  

        stiffness : float

                Stiffness of the spline.  

        n_legendre_terms : int

                Number of Legendre terms to evaluate.  

        copy : bool

                Whether to overwrite instance data or create a copy.  

        Notes:
        This function applies an average reference to the data if copy is False. Do not transform CSD data to source space.

        Example
        -----------

        -----------
        """
		temp_params = {'sphere': sphere, 'lambda2': lambda2,
		               'stiffness': stiffness, 'n_legendre_terms': n_legendre_terms, 'copy': copy}
		for k, v in temp_params.items():
			self._params[k] = v


class BadTrialAndChannel(Stage):
	"""
	    DESCRIPTION
	    -----------
	    Plots all the trials and channels signals and you can choose bad trials or channels to be removed from data

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
	in_out = {EpochsData: EpochsData}

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		super().__init__(id, database, inputs, outputs)

	"""
	        DESCRIPTION
	        -----------
	        The Constructor for BadTrialAndChannel 

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

	def do_task(self):
		"""
		        DESCRIPTION
		        -----------
		        Imports input from database and performs the task on it and saves output to database
		        -----------
		        """
		input_datas_list = self._get_input()
		input_data = input_datas_list[0]

		if isinstance(input_data, EpochsData):
			epochs_data = input_data.get_data()

			epochs_data.plot(scaling='auto')
			reject_channels_name = input('Channels name (split with ,): ').split(sep=',')
			reject_epochs_idx = map(int, input('Epochs Index (split with ,): ').split(sep=','))

			epochs_data = epochs_data.drop_channels(reject_channels_name)
			epochs_data = epochs_data.drop(reject_epochs_idx)

			output = EpochsData(input_data.get_id(), epochs_data)
			self._set_output(output, self._outputs[0])
		else:
			raise Exception('Input Data type is not RawData nor EpochData\n'
			                'input type={}'.format(type(input_data)))
		self._finish()
