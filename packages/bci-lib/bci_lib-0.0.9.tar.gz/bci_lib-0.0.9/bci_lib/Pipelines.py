from .Stages.Classification.ML import CreateModel, Train, Test
from .Stages.LoadData import LoadFromDataset, LoadRaw, LoadEpochs
from typing import Tuple
from .DataTypes import BaseObject, Database, ID, Stage, SKModel, BaseResult, RawData, EpochsData
from .Stages.Preprocess import TestTrainSplit
from .Stages.FeatureExtraction import PCA,ICA


class SingleRun(BaseObject):
	"""
	DESCRIPTION
	-----------
	Single run

	"""

	def __init__(self):
		"""
		DESCRIPTION
		-----------
		The Constructor for SingleRun

		"""
		my_id = ID(SingleRun)
		super().__init__(my_id)
		self._database = Database()
		self.pipeline = []
		self.train_ids = []
		self.base_data_ids = []
		self.test_ids = []
		self.model_ids = []
		self.train_pipeline = []
		self.test_pipeline = []

	def _get_stage(self, stage_idx=-1):
		"""
		DESCRIPTION
		-----------
		_get_stage

		Parameters
		-----------
		stage_idx : int | -1

		"""
		return self.pipeline[stage_idx]

	def _add_to_pipeline(self, my_stage):
		"""
		DESCRIPTION
		-----------
		_add_to_pipeline

		Parameters
		-----------
		my_stage : int

		"""
		self.pipeline.append(my_stage)

	def add_stage(self, stage, stage_idx=-1):
		"""
		DESCRIPTION
		-----------
		add_stage

		Parameters
		-----------
		stage_idx : int | -1

		"""
		stage_id = ID(stage)
		if len(self.train_ids) == 0:
			if stage_idx != -1:
				stage_output_id = ID(
					stage.in_out[self._get_stage(stage_idx)._outputs[0].get_type()])
				my_stage = stage(stage_id, self._database, self._get_stage(stage_idx)._outputs,
				                 (stage_output_id,))
			elif stage is CreateModel:
				stage_output_id = ID(SKModel)
				my_stage = stage(stage_id, self._database, (stage_output_id,))
				self.model_ids.append(stage_output_id)
			elif stage is LoadFromDataset:
				stage_output_id = ID(RawData)
				my_stage = stage(stage_id, self._database, (stage_output_id,))
				self.base_data_ids.append(stage_output_id)
			elif stage is LoadRaw:
				def load_info(mark_as_test: bool = False):
					if not isinstance(mark_as_test, bool):
						raise TypeError(
							'mark_as_test parameter should be boolean but it is {}'.format(type(mark_as_test)))
					if mark_as_test:
						stage_output_id_test = ID(EpochsData)
						my_stage_test = stage(
							stage_id, self._database, (stage_output_id_test,))
						self.test_ids.append(stage_output_id_test)
						self.train_ids.append(self.base_data_ids[-1])
						self._add_to_pipeline(my_stage_test)
						return my_stage_test
					else:
						stage_output_id = ID(EpochsData)
						my_stage = stage(
							stage_id, self._database, (stage_output_id,))
						self._add_to_pipeline(my_stage)
						self.base_data_ids.append(stage_output_id)
						return my_stage

				return load_info
			elif stage is LoadEpochs:
				def load_info(mark_as_test: bool = False):
					if not isinstance(mark_as_test, bool):
						raise TypeError('mark_as_test parameter should be boolean but it is {}'.format(
							type(mark_as_test)))
					if mark_as_test:
						stage_output_id_test = ID(EpochsData)
						my_stage_test = stage(
							stage_id, self._database, (stage_output_id_test,))
						self.test_ids.append(stage_output_id_test)
						self.train_ids.append(self.base_data_ids[-1])
						self._add_to_pipeline(my_stage_test)
						return my_stage_test
					else:
						stage_output_id = ID(EpochsData)
						my_stage = stage(
							stage_id, self._database, (stage_output_id,))
						self._add_to_pipeline(my_stage)
						self.base_data_ids.append(stage_output_id)
						return my_stage

				return load_info

			elif stage is Train:
				stage_output_id = ID(SKModel)
				my_stage = stage(stage_id, self._database, (self.base_data_ids[-1],),
				                 (stage_output_id,), self.model_ids[-1])
				self.model_ids.append(stage_output_id)
			elif stage is Test:
				stage_output_id = ID(BaseResult)
				my_stage = stage(stage_id, self._database, (self.base_data_ids[-1],),
				                 (stage_output_id,), self.model_ids[-1])
				self.base_data_ids.append(stage_output_id)
			elif stage is TestTrainSplit:
				stage_output_id_train = ID(EpochsData)
				stage_output_id_test = ID(EpochsData)
				my_stage = stage(stage_id, self._database, (self.base_data_ids[-1],),
				                 (stage_output_id_train, stage_output_id_test))
				self.train_ids.append(stage_output_id_train)
				self.test_ids.append(stage_output_id_test)
			else:
				stage_output_id = ID(
					stage.in_out[self.base_data_ids[-1].get_type()])
				my_stage = stage(stage_id, self._database, (self.base_data_ids[-1],),
				                 (stage_output_id,))
				self.base_data_ids.append(stage_output_id)
			# stage in_out looks like this -> {RawData: RawData, EpochsData:EpochsData}
			self._add_to_pipeline(my_stage)
			return my_stage
		else:
			if stage is CreateModel:
				stage_output_id = ID(SKModel)
				my_stage = stage(stage_id, self._database, (stage_output_id,))
				self.model_ids.append(stage_output_id)
				self._add_to_pipeline(my_stage)
				return my_stage
			elif stage is LoadFromDataset:
				stage_output_id = ID(RawData)
				my_stage = stage(stage_id, self._database, (stage_output_id,))
				self._add_to_pipeline(my_stage)
				return my_stage
			elif stage is LoadRaw:
				raise Exception(
					'You have test and train datas, you cant use load again')
			elif stage is LoadEpochs:
				raise Exception(
					'You have test and train datas, you cant use load again')
			elif stage is TestTrainSplit:
				raise Exception('error using TestTrainSplit twice!')
			elif stage is Train:
				stage_output_id = ID(SKModel)
				my_stage = stage(stage_id, self._database, (self.train_ids[-1],),
				                 (stage_output_id,), self.model_ids[-1])
				self.train_pipeline.append(my_stage)
				self.model_ids.append(stage_output_id)
				return my_stage
			elif stage is Test:
				stage_output_id = ID(BaseResult)
				my_stage = stage(stage_id, self._database, (self.test_ids[-1],),
				                 (stage_output_id,), self.model_ids[-1])
				self.test_pipeline.append(my_stage)
				return my_stage
			elif (stage is PCA) or (stage is ICA):
				stage_output_id_train = ID(
					stage.in_out[self.train_ids[-1].get_type()])
				my_stage_train = stage(stage_id, self._database, (self.train_ids[-1],),
				                       (stage_output_id_train,))
				self.train_ids.append(stage_output_id_train)
				self.train_pipeline.append(my_stage_train)

				stage_output_id_test = ID(
					stage.in_out[self.test_ids[-1].get_type()])
				my_stage_test = stage(stage_id, self._database, (self.test_ids[-1],),
				                      (stage_output_id_test,), mark_as_test=True)
				my_stage_test.cache = my_stage_train.cache
				self.test_ids.append(stage_output_id_test)
				self.test_pipeline.append(my_stage_test)

				my_stage_test._params = my_stage_train._params
				return my_stage_train
			else:
				stage_output_id_train = ID(
					stage.in_out[self.train_ids[-1].get_type()])
				my_stage_train = stage(stage_id, self._database, (self.train_ids[-1],),
				                       (stage_output_id_train,))
				self.train_ids.append(stage_output_id_train)
				self.train_pipeline.append(my_stage_train)

				stage_output_id_test = ID(
					stage.in_out[self.test_ids[-1].get_type()])
				my_stage_test = stage(stage_id, self._database, (self.test_ids[-1],),
				                      (stage_output_id_test,))
				self.test_ids.append(stage_output_id_test)
				self.test_pipeline.append(my_stage_test)

				my_stage_test._params = my_stage_train._params
				return my_stage_train

	def set_stage_params(self, stage_idx=-1):
		"""
		DESCRIPTION
		-----------
		set_stage_params

		Parameters
		-----------
		stage_idx : int | -1

		"""
		return self.pipeline[stage_idx].set_params

	def do_task(self):
		"""
		DESCRIPTION
		-----------
		do_task

		"""
		for stage in self.pipeline:
			stage.do_task()
		for stage in self.train_pipeline:
			stage.do_task()
		for stage in self.test_pipeline:
			stage.do_task()


class Pipeline(BaseObject):
	"""
	DESCRIPTION
	-----------
	The Constructor for SingleRun

	Attributes
	-----------
	id : ID

	edges : Tuple[Tuple[Stage, Stage or None], ...] | None

	"""

	def __init__(self, id: ID, edges: Tuple[Tuple[Stage, Stage or None], ...] = None):
		"""
		DESCRIPTION
		-----------
		The Constructor for Pipeline

		Parameters
		-----------
		id : ID

		edges : Tuple[Tuple[Stage, Stage or None], ...] | None

		"""
		super().__init__(id)
		self._edges = dict()
		self._edges[None] = list()  # for root
		self._incoming_edge_count = dict()
		if edges is not None:
			for edge in edges:
				self.add_edge(dst=edge[0], src=edge[1])

	def add_edge(self, dst: Stage, src: Stage = None):
		"""
		DESCRIPTION
		-----------
		add_edge

		Parameters
		-----------
		dst : bci_lib.Stage

		src : bci_lib.Stage | None

		"""
		if src not in self._edges:
			self._edges[src] = list()
			if src is not None:
				self.add_edge(dst=src, src=None)
		self._edges[src].append(dst)
		if dst not in self._incoming_edge_count:
			self._incoming_edge_count[dst] = 0
		self._incoming_edge_count[dst] += 1

	def get_edges(self) -> Tuple[Tuple[Stage, Stage or None], ...]:
		return tuple((dst, src) for src in self._edges for dst in self._edges[src])

	def get_topo_sort(self):
		topo_order = list()
		roots = self._edges[None].copy()
		while roots:
			src = roots.pop(0)
			# Iterate through the adjacency list
			if src in self._edges:
				for stage in self._edges[src]:
					self._incoming_edge_count[stage] -= 1
					if self._incoming_edge_count[stage] == 0:
						roots.append(stage)
			topo_order.append(src)
		del roots
		return topo_order
