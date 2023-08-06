import uuid
from abc import ABC, abstractmethod

import mne
from numpy import ndarray
from typing import Any, Tuple, List
from sklearn.base import BaseEstimator
from nptyping import NDArray


class ID:
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, objtype, number=None, name=None, description=None):
		"""
		DESCRIPTION
		-----------
		The Constructor for ID

		"""
		self._type = objtype
		self.classifier = None
		if number is None:
			number = uuid.uuid1().int
		self._number = number
		if name is None:
			name = objtype.__name__
		self._name = name
		if description is None:
			description = ''
		self._description = description

	def __repr__(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return (f'{self.__class__.__name__}('
		        f'{self._number!r}, {self._name!r})')

	def __str__(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return str(self.get_number())

	def __eq__(self, other):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		if isinstance(other, ID):
			return self.get_number() == other.get_number()
		elif isinstance(other, int):
			return self.get_number() == other
		else:
			return super().__eq__(other)

	def __hash__(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self.get_number()

	def get_number(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._number

	def get_name(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._name

	def get_description(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._description

	def set_name(self, name):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self._name = name

	def set_description(self, description):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self._description = description

	def get_type(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._type


class BaseObject(ABC):

	def __init__(self, id: ID):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self._id = id

	def __hash__(self):
		return self.get_id().__hash__()

	def get_id(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._id

	def set_id(self, id: ID):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self._id = id


class Database:

	def __init__(self, database: dict = None):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self._database = database if database is not None else dict()

	def add(self, *objs: BaseObject):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		for obj in objs:
			self._database[obj.get_id()] = obj

	def get(self, *ids: ID or int):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		output = []
		for id in ids:
			output.append(self._database.get(id))
		return output

	def pop(self, *ids: ID or int):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		output = []
		for id in ids:
			output.append(self._database.pop(id))
		return output

	def get_database_dict(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._database


class Stage(BaseObject, ABC):
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...]):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		super().__init__(id)
		self._database = database
		self._inputs = inputs
		self._outputs = outputs
		self._params = dict()
		self.finished = False

	def set_params(self, *args, **kwargs):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		pass

	def get_params(self, *args):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		if len(args) == 0:
			return self._params.copy()
		else:
			return {key: self._params[key] for key in args}

	@abstractmethod
	def do_task(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		pass

	def _get_input(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		from copy import deepcopy
		return deepcopy(self._database.get(*self._inputs))

	def _set_output(self, output, output_id):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		output.set_id(output_id)
		# output.add_process(self)
		self._database.add(output)

	def _finish(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		self.finished = True


class BaseData(BaseObject, ABC):
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, id: ID, data: Any, processes=None):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		super().__init__(id)
		self._data = data

	# self._processes = list() if processes is None else processes

	# def set_processes(self, processes: List[Stage]):
	# 	self._processes = processes

	# def add_process(self, process: Stage):
	# self._processes.append(process)

	# def get_processes(self):
	# 	return self._processes

	def get_data(self):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return self._data

	def get_feature(self, dim: int):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		function_name = "_get_" + str(dim) + "d_feature"
		if hasattr(self, function_name):
			return getattr(self, function_name)()

	def save_obj(self, output: str):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		import pickle
		file_to_store = open(output, "wb")
		pickle.dump(self, file_to_store)
		file_to_store.close()


class EEGData(BaseData, ABC):
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, id: ID, data: Any, processes=None):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		super().__init__(id, data, processes)

	def get_labels(self, stim_channel_name: str = "Stim"):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		stim = self._data.get_data(picks=stim_channel_name)
		return stim[stim != 0]


class FeatureData(BaseData, ABC):
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, id: ID, data: NDArray, label: NDArray[(Any,)], processes=None):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		super().__init__(id, data, processes)
		self._label = label


class RawData(EEGData):
	"""
	DESCRIPTION
	-----------
	ID

	"""

	def __init__(self, id: ID, data: mne.io.RawArray, processes=None):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		super().__init__(id, data, processes)

	def _get_1d_feature(self) -> Tuple[NDArray[(Any, Any)], NDArray[(Any,)]]:
		pass

	def _get_2d_feature(self) -> Tuple[NDArray[(Any, Any, Any)], NDArray[(Any,)]]:
		pass


class EpochsData(EEGData):

	def __init__(self, id: ID, data: mne.Epochs, processes=None):
		super().__init__(id, data, processes)

	def _get_1d_feature(self) -> Tuple[NDArray[(Any, Any)], NDArray[(Any,)]]:
		pass

	def _get_2d_feature(self) -> Tuple[NDArray[(Any, Any, Any)], NDArray[(Any,)]]:
		pass


class OneDFeature(FeatureData):

	def __init__(self, id: ID, data: NDArray[(Any, Any)], label: NDArray[(Any,)], processes=None):
		super().__init__(id, data, label, processes)

	def get_feature(self, dim: int = 1):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return super().get_feature(dim)

	def _get_1d_feature(self) -> Tuple[NDArray[(Any, Any)], NDArray[(Any,)]]:
		return self.get_data(), self._label


class TwoDFeature(FeatureData):

	def __init__(self, id: ID, data: NDArray[(Any, Any, Any)], label: NDArray[(Any,)], processes=None):
		super().__init__(id, data, label, processes)

	def get_feature(self, dim: int = 2):
		"""
		DESCRIPTION
		-----------
		ID

		"""
		return super().get_feature(dim)

	def get_2d_feature(self) -> Tuple[NDArray[(Any, Any, Any)], NDArray[(Any,)]]:
		return self.get_data(), self._label


class BaseModel(BaseObject):

	def __init__(self, id: ID):
		super().__init__(id)


class SKModel(BaseModel):

	def __init__(self, id: ID, model: BaseEstimator, classifier):
		super().__init__(id)
		self._model = model
		self._classifier = classifier


class BaseResult(BaseObject):

	def __init__(self, id: ID):
		super().__init__(id)


class SimpleResult(BaseResult):

	def __init__(self, id: ID, result, classifier):
		super().__init__(id)
		self.result = result
