from abc import ABC
from typing import Tuple
import mne
from bci_lib.DataTypes import Stage, Database, ID, RawData, EpochsData
from bci_lib.Dataset import Dataset


class LoadFromDataset(Stage):
	"""
	DESCRIPTION
	-----------
	Load data from prepared datasets

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

	def __init__(self, id: ID, database: Database, outputs: Tuple[ID], mark_as_test: bool = False):
		"""
		DESCRIPTION
		-----------
		The Constructor for LoadFromDataset

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
		super().__init__(id, database, (), outputs)
		self.mark_as_test = mark_as_test

	def set_params(self, dataset: dict, save_in_cache: bool = True):
		"""
		DESCRIPTION
		-----------
		Load From Dataset

		Parameter
		-----------
		dataset : dict or list

		save_in_cache: bool | True

		Example
		-----------

		-----------
		"""
		self._params = {'data_info': dataset, 'save_in_cache': save_in_cache}
		return self._params

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Import the data from datasets and save it on database
		-----------
		"""
		params = self.get_params()
		outputs = self._outputs

		data = Dataset.load(**params)

		self._set_output(data, outputs[0])
		self._finish()


class LoadRaw(Stage):
	"""
	DESCRIPTION
	-----------
	Load raw data from user

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

	def __init__(self, id: ID, database: Database, outputs: Tuple[ID], mark_as_test: bool = False):
		"""
		DESCRIPTION
		-----------
		The Constructor for LoadRaw

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
		super().__init__(id, database, (), outputs)
		self.mark_as_test = mark_as_test

	def set_params(self, rawdata: mne.io.Raw):
		"""
		DESCRIPTION
		-----------
		Load raw data

		Parameter
		-----------
		rawdata : Instance of mne.io.Raw

		Example
		-----------

		-----------
		"""
		self._params = {'data': rawdata}
		return self._params

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Import the raw data from user and save it on database
		-----------
		"""
		raw = self._params.pop('data')
		output = RawData(self._outputs[0], raw)
		self._set_output(output, self._outputs[0])


class LoadEpochs(Stage):
	"""
	DESCRIPTION
	-----------
	Load epochs data from user

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

	def __init__(self, id: ID, database: Database, outputs: Tuple[ID], mark_as_test: bool = False):
		"""
		DESCRIPTION
		-----------
		The Constructor for LoadEpochs

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
		super().__init__(id, database, (), outputs)
		self.mark_as_test = mark_as_test

	def set_params(self, epochsdata: mne.Epochs):
		"""
		DESCRIPTION
		-----------
		Load Epochs data

		Parameter
		-----------
		epochsdata: Instance of mne.Epochs

		Example
		-----------

		-----------
		"""
		self._params = {'data': epochsdata}
		return self._params

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Import the epochs data from user and save it on database
		-----------
		"""
		epochs = self._params.pop('data')
		output = EpochsData(self._outputs[0], epochs)
		self._set_output(output, self._outputs[0])
