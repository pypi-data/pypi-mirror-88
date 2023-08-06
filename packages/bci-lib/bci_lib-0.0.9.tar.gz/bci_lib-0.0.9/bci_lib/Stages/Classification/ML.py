from abc import ABC
from enum import Enum
from sklearn import svm, model_selection, metrics, discriminant_analysis
from bci_lib.DataTypes import Stage, Database, SKModel, ID, SimpleResult, TwoDFeature, OneDFeature
from sklearn.linear_model import LogisticRegression

from typing import Any, Tuple, List
from copy import deepcopy


class MLModel:
	class SVM(Enum):
		SVC = svm.SVC
		NuSVC = svm.NuSVC
		LinearSVC = svm.LinearSVC

	class DiscriminantAnalysis(Enum):
		Linear = discriminant_analysis.LinearDiscriminantAnalysis
		Quadratic = discriminant_analysis.QuadraticDiscriminantAnalysis

	class LogisticRegression(Enum):
		LR = LogisticRegression


class CreateModel(Stage):
	"""
	DESCRIPTION
	-----------
	Defines the Classifier for Creating the Model

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

	# @_deprecate_positional_args
	def __init__(self, id: ID, database: Database, outputs: Tuple[ID]):
		"""
		DESCRIPTION
		-----------
		The Constructor for CreateModel

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
		super().__init__(id, database, (), outputs)
		self._classifier = None

	# @_deprecate_positional_args
	def set_params(self, classifier):
		"""
		DESCRIPTION
		-----------
		Defines the Classifier for Creating the Model

		Parameters
		-----------
		classifier :                                          ########### TODO: Complete this param

		-----------
		"""
		self._classifier = classifier
		self._outputs[0].classifier = classifier

	# @_deprecate_positional_args
	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database

		-----------
		"""
		classifier = self._classifier.value
		clf = classifier()

		model = SKModel(id=self._outputs[0],
		                model=clf, classifier=self._classifier)
		self._set_output(model, self._outputs[0])
		self._finish()


class Train(Stage):
	"""
	DESCRIPTION
	-----------
	Defines the Classifier for Creating the Model

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

	model_id : ID

		It's id of the train model

	"""
	in_out = {TwoDFeature: SKModel, OneDFeature: SKModel}

	# @_deprecate_positional_args
	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...], model_id: ID):
		"""
	DESCRIPTION
	-----------
	The Constructor for Train

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

	model_id : ID

		It's id of the train model

	"""
		super().__init__(id, database, inputs, outputs)
		self._model_id = model_id
		self._outputs[0].classifier = model_id.classifier
		classifier = self._outputs[0].classifier
		self.set_params = getattr(self,
		                          "_set_params_{}_{}".format(classifier.__class__.__name__,
		                                                     classifier.name))

	# @_deprecate_positional_args
	def _set_params_SVM_SVC(self, C=1.0, kernel='rbf', degree=3, gamma='scale',
	                        coef0=0.0, shrinking=True, probability=False, tol=0.001,
	                        cache_size=200, class_weight=None, verbose=False, max_iter=-1,
	                        decision_function_shape='ovr', break_ties=False, random_state=None):
		"""
		DESCRIPTION
		-----------
		C-Support Vector Classification.

		The implementation is based on libsvm. The fit time scales at least quadratically with the number of samples and may be impractical beyond tens of thousands of samples. For large datasets consider using :class:sklearn.svm.LinearSVC or :class:sklearn.linear_model.SGDClassifier instead, possibly after a :class:sklearn.kernel_approximation.Nystroem transformer.

		The multiclass support is handled according to a one-vs-one scheme.

		For details on the precise mathematical formulation of the provided kernel functions and how gamma, coef0 and degree affect each other, see the corresponding section in the narrative documentation: :ref:svm_kernels.

		Parameters
		-----------
		C : float, optional (default=1.0)

			Regularization parameter. The strength of the regularization is
			inversely proportional to C. Must be strictly positive. The penalty
			is a squared l2 penalty.

		kernel : string, optional (default='rbf')

			Specifies the kernel type to be used in the algorithm.
			It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' or
			a callable.
			If none is given, 'rbf' will be used. If a callable is given it is
			used to pre-compute the kernel matrix from data matrices; that matrix
			should be an array of shape `(n_samples, n_samples)`.

		degree : int, optional (default=3)

			Degree of the polynomial kernel function ('poly').
			Ignored by all other kernels.

		gamma : {'scale', 'auto'} or float, optional (default='scale')

			Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.

			- if `gamma='scale'` (default) is passed then it uses
			1 / (n_features * X.var()) as value of gamma,
			- if 'auto', uses 1 / n_features.

			The default value of `gamma` changed from 'auto' to 'scale'.

		coef0 : float, optional (default=0.0)

			Independent term in kernel function.
			It is only significant in 'poly' and 'sigmoid'.

		shrinking : boolean, optional (default=True)

			Whether to use the shrinking heuristic.

		probability : boolean, optional (default=False)

			Whether to enable probability estimates. This must be enabled prior
			to calling `fit`, will slow down that method as it internally uses
			5-fold cross-validation, and `predict_proba` may be inconsistent with
			`predict`. Read more in the :ref:`User Guide  scores_probabilities `.

		tol : float, optional (default=1e-3)

			Tolerance for stopping criterion.

		cache_size : float, optional

			Specify the size of the kernel cache (in MB).

		class_weight : {dict, 'balanced'}, optional

			Set the parameter C of class i to class_weight[i]*C for
			SVC. If not given, all classes are supposed to have
			weight one.
			The "balanced" mode uses the values of y to automatically adjust
			weights inversely proportional to class frequencies in the input data
			as `n_samples / (n_classes * np.bincount(y))`

		verbose : bool, default: False

			Enable verbose output. Note that this setting takes advantage of a
			per-process runtime setting in libsvm that, if enabled, may not work
			properly in a multithreaded context.

		max_iter : int, optional (default=-1)

			Hard limit on iterations within solver, or -1 for no limit.

		decision_function_shape : 'ovo', 'ovr', default='ovr'

			Whether to return a one-vs-rest ('ovr') decision function of shape
			(n_samples, n_classes) as all other classifiers, or the original
			one-vs-one ('ovo') decision function of libsvm which has shape
			(n_samples, n_classes * (n_classes - 1) / 2). However, one-vs-one
			('ovo') is always used as multi-class strategy.

				decision_function_shape is 'ovr' by default.

			*decision_function_shape='ovr'* is recommended.

			Deprecated *decision_function_shape='ovo' and None*.

		break_ties : bool, optional (default=False)

			If true, `decision_function_shape='ovr'`, and number of classes   2,
			:term:`predict` will break ties according to the confidence values of
			:term:`decision_function`; otherwise the first class among the tied
			classes is returned. Please note that breaking ties comes at a
			relatively high computational cost compared to a simple predict.

		random_state : int, RandomState instance or None, optional (default=None)

			The seed of the pseudo random number generator used when shuffling
			the data for probability estimates. If int, random_state is the
			seed used by the random number generator; If RandomState instance,
			random_state is the random number generator; If None, the random
			number generator is the RandomState instance used by `np.random`.

		Examples
		-----------

		-----------
		"""
		self._params = {'C': C, 'kernel': kernel, 'degree': degree, 'gamma': gamma, 'coef0': coef0,
		                'shrinking': shrinking,
		                'probability': probability, 'tol': tol, 'cache_size': cache_size, 'class_weight': class_weight,
		                'verbose': verbose,
		                'max_iter': max_iter, 'decision_function_shape': decision_function_shape,
		                'break_ties': break_ties, 'random_state': random_state}

	# @_deprecate_positional_args
	def _set_params_SVM_NuSVC(self, break_ties=False, cache_size=200, class_weight=None, coef0=0.0,
	                          decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf', max_iter=-1,
	                          nu=0.5, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False):
		"""
		DESCRIPTION
		-----------
		Nu-Support Vector Classification.

		Similar to SVC but uses a parameter to control the number of support vectors.

		The implementation is based on libsvm.


		Parameters
		-----------
		nu : float, optional (default=0.5)

			An upper bound on the fraction of training errors and a lower
			bound of the fraction of support vectors. Should be in the
			interval (0, 1].

		kernel : string, optional (default='rbf')

		Specifies the kernel type to be used in the algorithm.
		It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' or
		a callable.
		If none is given, 'rbf' will be used. If a callable is given it is
		used to precompute the kernel matrix.

		degree : int, optional (default=3)

			Degree of the polynomial kernel function ('poly').
			Ignored by all other kernels.

		gamma : {'scale', 'auto'} or float, optional (default='scale')

			Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.

			- if `gamma='scale'` (default) is passed then it uses
			1 / (n_features * X.var()) as value of gamma,
			- if 'auto', uses 1 / n_features.

			The default value of `gamma` changed from 'auto' to 'scale'.

		coef0 : float, optional (default=0.0)

			Independent term in kernel function.
			It is only significant in 'poly' and 'sigmoid'.

		shrinking : boolean, optional (default=True)

			Whether to use the shrinking heuristic.

		probability : boolean, optional (default=False)

			Whether to enable probability estimates. This must be enabled prior
			to calling `fit`, will slow down that method as it internally uses
			5-fold cross-validation, and `predict_proba` may be inconsistent with
			`predict`. Read more in the :ref:`User Guide  scores_probabilities `.

		tol : float, optional (default=1e-3)

			Tolerance for stopping criterion.

		cache_size : float, optional

			Specify the size of the kernel cache (in MB).

		class_weight : {dict, 'balanced'}, optional

			Set the parameter C of class i to class_weight[i]*C for
			SVC. If not given, all classes are supposed to have
			weight one. The "balanced" mode uses the values of y to automatically
			adjust weights inversely proportional to class frequencies as
			`n_samples / (n_classes * np.bincount(y))`

		verbose : bool, default: False

			Enable verbose output. Note that this setting takes advantage of a
			per-process runtime setting in libsvm that, if enabled, may not work
			properly in a multithreaded context.

		max_iter : int, optional (default=-1)

			Hard limit on iterations within solver, or -1 for no limit.

		decision_function_shape : 'ovo', 'ovr', default='ovr'

			Whether to return a one-vs-rest ('ovr') decision function of shape
			(n_samples, n_classes) as all other classifiers, or the original
			one-vs-one ('ovo') decision function of libsvm which has shape
			(n_samples, n_classes * (n_classes - 1) / 2).

				decision_function_shape is 'ovr' by default.

			*decision_function_shape='ovr'* is recommended.

			Deprecated *decision_function_shape='ovo' and None*.

		break_ties : bool, optional (default=False)

			If true, `decision_function_shape='ovr'`, and number of classes   2,
			:term:`predict` will break ties according to the confidence values of
			:term:`decision_function`; otherwise the first class among the tied
			classes is returned. Please note that breaking ties comes at a
			relatively high computational cost compared to a simple predict.

		random_state : int, RandomState instance or None, optional (default=None)

			The seed of the pseudo random number generator used when shuffling
			the data for probability estimates. If int, random_state is the seed
			used by the random number generator; If RandomState instance,
			random_state is the random number generator; If None, the random
			number generator is the RandomState instance used by `np.random`.

		Examples
		-----------

		-----------
		"""
		self._params = {'break_ties': break_ties, 'cache_size': cache_size, 'class_weight': class_weight,
		                'coef0': coef0,
		                'decision_function_shape': decision_function_shape, 'degree': degree, 'gamma': gamma,
		                'kernel': kernel,
		                'max_iter': max_iter, 'nu': nu, 'probability': probability, 'random_state': random_state,
		                'shrinking': shrinking, 'tol': tol,
		                'verbose': verbose}

	# @_deprecate_positional_args
	def _set_params_SVM_LinearSVC(self, C=1.0, class_weight=None, dual=True, fit_intercept=True,
	                              intercept_scaling=1, loss='squared_hinge', max_iter=1000, multi_class='ovr',
	                              penalty='l2', random_state=None, tol=0.0001, verbose=0):
		"""
		DESCRIPTION
		-----------
		Linear Support Vector Classification.

		Similar to SVC with parameter kernel='linear', but implemented in terms of liblinear rather than libsvm, so it has more flexibility in the choice of penalties and loss functions and should scale better to large numbers of samples.

		This class supports both dense and sparse input and the multiclass support is handled according to a one-vs-the-rest scheme.

		Parameters
		-----------
		penalty : str, 'l1' or 'l2' (default='l2')

			Specifies the norm used in the penalization. The 'l2'
			penalty is the standard used in SVC. The 'l1' leads to `coef_`
			vectors that are sparse.

		loss : str, 'hinge' or 'squared_hinge' (default='squared_hinge')

			Specifies the loss function. 'hinge' is the standard SVM loss
			(used e.g. by the SVC class) while 'squared_hinge' is the
			square of the hinge loss.

		dual : bool, (default=True)

			Select the algorithm to either solve the dual or primal
			optimization problem. Prefer dual=False when n_samples   n_features.

		tol : float, optional (default=1e-4)

			Tolerance for stopping criteria.

		C : float, optional (default=1.0)

			Regularization parameter. The strength of the regularization is
			inversely proportional to C. Must be strictly positive.

		multi_class : str, 'ovr' or 'crammer_singer' (default='ovr')

			Determines the multi-class strategy if `y` contains more than
			two classes.
			`"ovr"` trains n_classes one-vs-rest classifiers, while
			`"crammer_singer"` optimizes a joint objective over all classes.
			While `crammer_singer` is interesting from a theoretical perspective
			as it is consistent, it is seldom used in practice as it rarely leads
			to better accuracy and is more expensive to compute.
			If `"crammer_singer"` is chosen, the options loss, penalty and dual
			will be ignored.

		fit_intercept : bool, optional (default=True)

			Whether to calculate the intercept for this model. If set
			to false, no intercept will be used in calculations
			(i.e. data is expected to be already centered).

		intercept_scaling : float, optional (default=1)

			When self.fit_intercept is True, instance vector x becomes
			`[x, self.intercept_scaling]`,
			i.e. a "synthetic" feature with constant value equals to
			intercept_scaling is appended to the instance vector.
			The intercept becomes intercept_scaling * synthetic feature weight
			Note! the synthetic feature weight is subject to l1/l2 regularization
			as all other features.
			To lessen the effect of regularization on synthetic feature weight
			(and therefore on the intercept) intercept_scaling has to be increased.

		class_weight : {dict, 'balanced'}, optional

			Set the parameter C of class i to `class_weight[i]*C` for
			SVC. If not given, all classes are supposed to have
			weight one.
			The "balanced" mode uses the values of y to automatically adjust
			weights inversely proportional to class frequencies in the input data
			as `n_samples / (n_classes * np.bincount(y))`.

		verbose : int, (default=0)

			Enable verbose output. Note that this setting takes advantage of a
			per-process runtime setting in liblinear that, if enabled, may not work
			properly in a multithreaded context.

		random_state : int, RandomState instance or None, optional (default=None)

			The seed of the pseudo random number generator to use when shuffling
			the data for the dual coordinate descent (if `dual=True`). When
			`dual=False` the underlying implementation of :class:`LinearSVC`
			is not random and `random_state` has no effect on the results. If
			int, random_state is the seed used by the random number generator; If
			RandomState instance, random_state is the random number generator; If
			None, the random number generator is the RandomState instance used by
			`np.random`.

		max_iter : int, (default=1000)

			The maximum number of iterations to be run.

		Notes:
		The default solver is 'svd'. It can perform both classification and transform, and it does not rely on the calculation of the covariance matrix. This can be an advantage in situations where the number of features is large. However, the 'svd' solver cannot be used with shrinkage.

		The 'lsqr' solver is an efficient algorithm that only works for classification. It supports shrinkage.

		The 'eigen' solver is based on the optimization of the between class scatter to within class scatter ratio. It can be used for both classification and transform, and it supports shrinkage. However, the 'eigen' solver needs to compute the covariance matrix, so it might not be suitable for situations with a high number of features.

		Examples
		-----------

		"""

		self._params = {'C': C, 'class_weight': class_weight, 'dual': dual, 'fit_intercept': fit_intercept,
		                'intercept_scaling': intercept_scaling, 'loss': loss, 'max_iter': max_iter,
		                'multi_class': multi_class,
		                'penalty': penalty, 'random_state': random_state, 'tol': tol, 'verbose': verbose}

	# @_deprecate_positional_args
	def _set_params_DiscriminantAnalysis_Quadratic(self, priors=None, reg_param=0.0, store_covariance=False,
	                                               tol=0.0001):
		"""
		DESCRIPTION
		-----------
		Quadratic Discriminant Analysis

		A classifier with a quadratic decision boundary, generated by fitting class conditional densities to the data and using Bayes' rule.

		The model fits a Gaussian density to each class.

		Parameters
		-----------
		priors : array, optional, shape = [n_classes]

			Priors on classes

		reg_param : float, optional

			Regularizes the covariance estimate as
			`(1-reg_param)*Sigma + reg_param*np.eye(n_features)`

		store_covariance : boolean

			If True the covariance matrices are computed and stored in the
			`self.covariance_` attribute.

		tol : float, optional, default 1.0e-4

			Threshold used for rank estimation.

		Examples
		-----------


		-----------
		"""
		self._params = {'priors': priors, 'reg_param': reg_param,
		                'store_covariance': store_covariance, 'tol': tol}

	# @_deprecate_positional_args
	def _set_params_LogisticRegression_LR(self, C=1.0, class_weight=None, dual=False, fit_intercept=True,
	                                      intercept_scaling=1,
	                                      l1_ratio=None, max_iter=100, multi_class='auto', n_jobs=None, penalty='l2',
	                                      random_state=None, solver='lbfgs', tol=0.0001, verbose=0, warm_start=False):
		"""
		DESCRIPTION
		-----------
		Logistic Regression (aka logit, MaxEnt) classifier.

		In the multiclass case, the training algorithm uses the one-vs-rest (OvR) scheme if the 'multi_class' option is set to 'ovr', and uses the cross-entropy loss if the 'multi_class' option is set to 'multinomial'. (Currently the 'multinomial' option is supported only by the 'lbfgs', 'sag', 'saga' and 'newton-cg' solvers.)

		This class implements regularized logistic regression using the 'liblinear' library, 'newton-cg', 'sag', 'saga' and 'lbfgs' solvers. **Note that regularization is applied by default**. It can handle both dense and sparse input. Use C-ordered arrays or CSR matrices containing 64-bit floats for optimal performance; any other input format will be converted (and copied).

		The 'newton-cg', 'sag', and 'lbfgs' solvers support only L2 regularization with primal formulation, or no regularization. The 'liblinear' solver supports both L1 and L2 regularization, with a dual formulation only for the L2 penalty. The Elastic-Net regularization is only supported by the 'saga' solver.

		Parameters
		-----------
		penalty : {'l1', 'l2', 'elasticnet', 'none'}, default='l2'

			Used to specify the norm used in the penalization. The 'newton-cg',
			'sag' and 'lbfgs' solvers support only l2 penalties. 'elasticnet' is
			only supported by the 'saga' solver. If 'none' (not supported by the
			liblinear solver), no regularization is applied.

			l1 penalty with SAGA solver (allowing 'multinomial' + L1)

		dual : bool, default=False

			Dual or primal formulation. Dual formulation is only implemented for
			l2 penalty with liblinear solver. Prefer dual=False when
			n_samples   n_features.

		tol : float, default=1e-4

			Tolerance for stopping criteria.

		C : float, default=1.0

			Inverse of regularization strength; must be a positive float.
			Like in support vector machines, smaller values specify stronger
			regularization.

		fit_intercept : bool, default=True

			Specifies if a constant (a.k.a. bias or intercept) should be
			added to the decision function.

		intercept_scaling : float, default=1

			Useful only when the solver 'liblinear' is used
			and self.fit_intercept is set to True. In this case, x becomes
			[x, self.intercept_scaling],
			i.e. a "synthetic" feature with constant value equal to
			intercept_scaling is appended to the instance vector.
			The intercept becomes `intercept_scaling * synthetic_feature_weight`.

			Note! the synthetic feature weight is subject to l1/l2 regularization
			as all other features.
			To lessen the effect of regularization on synthetic feature weight
			(and therefore on the intercept) intercept_scaling has to be increased.

		class_weight : dict or 'balanced', default=None

			Weights associated with classes in the form `{class_label: weight}`.
			If not given, all classes are supposed to have weight one.

			The "balanced" mode uses the values of y to automatically adjust
			weights inversely proportional to class frequencies in the input data
			as `n_samples / (n_classes * np.bincount(y))`.

			Note that these weights will be multiplied with sample_weight (passed
			through the fit method) if sample_weight is specified.

			*class_weight='balanced'*

		random_state : int, RandomState instance, default=None

			The seed of the pseudo random number generator to use when shuffling
			the data.  If int, random_state is the seed used by the random number
			generator; If RandomState instance, random_state is the random number
			generator; If None, the random number generator is the RandomState
			instance used by `np.random`. Used when `solver` == 'sag' or
			'liblinear'.

		solver : {'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'}, default='lbfgs'

			Algorithm to use in the optimization problem.

			- For small datasets, 'liblinear' is a good choice, whereas 'sag' and
			'saga' are faster for large ones.
			- For multiclass problems, only 'newton-cg', 'sag', 'saga' and 'lbfgs'
			handle multinomial loss; 'liblinear' is limited to one-versus-rest
			schemes.
			- 'newton-cg', 'lbfgs', 'sag' and 'saga' handle L2 or no penalty
			- 'liblinear' and 'saga' also handle L1 penalty
			- 'saga' also supports 'elasticnet' penalty
			- 'liblinear' does not support setting `penalty='none'`

			Note that 'sag' and 'saga' fast convergence is only guaranteed on
			features with approximately the same scale. You can
			preprocess the data with a scaler from sklearn.preprocessing.

			Stochastic Average Gradient descent solver.
			SAGA solver.
				The default solver changed from 'liblinear' to 'lbfgs' in 0.22.

		max_iter : int, default=100

			Maximum number of iterations taken for the solvers to converge.

		multi_class : {'auto', 'ovr', 'multinomial'}, default='auto'

			If the option chosen is 'ovr', then a binary problem is fit for each
			label. For 'multinomial' the loss minimised is the multinomial loss fit
			across the entire probability distribution, *even when the data is
			binary*. 'multinomial' is unavailable when solver='liblinear'.
			'auto' selects 'ovr' if the data is binary, or if solver='liblinear',
			and otherwise selects 'multinomial'.

			Stochastic Average Gradient descent solver for 'multinomial' case.
				Default changed from 'ovr' to 'auto' in 0.22.

		verbose : int, default=0

			For the liblinear and lbfgs solvers set verbose to any positive
			number for verbosity.

		warm_start : bool, default=False

			When set to True, reuse the solution of the previous call to fit as
			initialization, otherwise, just erase the previous solution.
			Useless for liblinear solver. See :term:`the Glossary  warm_start `.

			*warm_start* to support *lbfgs*, *newton-cg*, *sag*, *saga* solvers.

		n_jobs : int, default=None

			Number of CPU cores used when parallelizing over classes if
			multi_class='ovr'". This parameter is ignored when the `solver` is
			set to 'liblinear' regardless of whether 'multi_class' is specified or
			not. `None` means 1 unless in a :obj:`joblib.parallel_backend`
			context. `-1` means using all processors.
			See :term:`Glossary  n_jobs ` for more details.

		l1_ratio : float, default=None

			The Elastic-Net mixing parameter, with `0  = l1_ratio  = 1`. Only
			used if `penalty='elasticnet'`. Setting `l1_ratio=0` is equivalent
			to using `penalty='l2'`, while setting `l1_ratio=1` is equivalent
			to using `penalty='l1'`. For `0   l1_ratio  1`, the penalty is a
			combination of L1 and L2.

		Notes:
		The underlying C implementation uses a random number generator to select features when fitting the model. It is thus not uncommon, to have slightly different results for the same input data. If that happens, try with a smaller tol parameter.

		Predict output may not match that of standalone liblinear in certain cases. See :ref:differences from liblinear <liblinear_differences> in the narrative documentation.

		Examples
		-----------


		-----------
		"""
		self._params = {'C': C, 'class_weight': class_weight, 'dual': dual, 'fit_intercept': fit_intercept,
		                'intercept_scaling': intercept_scaling,
		                'l1_ratio': l1_ratio, 'max_iter': max_iter, 'multi_class': multi_class, 'n_jobs': n_jobs,
		                'penalty': penalty,
		                'random_state': random_state, 'solver': solver, 'tol': tol, 'verbose': verbose,
		                'warm_start': warm_start}

	# @_deprecate_positional_args
	def find_params(self, params: dict, scoring):
		"""
		DESCRIPTION
		-----------
		GridSearchCV

		Exhaustive search over specified parameter values for an estimator.

		Important members are fit, predict.

		GridSearchCV implements a "fit" and a "score" method. It also implements "predict",
		"predict_proba", "decision_function", "transform" and "inverse_transform" if they
		are implemented in the estimator used.

		The parameters of the estimator used to apply these methods are optimized
		by cross-validated grid-search over a parameter grid.

		Parameters
		----------

		params : dict or list of dictionaries
			Dictionary with parameters names (str) as keys and lists of parameter settings to try as values, or a list of such dictionaries, in which case the grids spanned by each dictionary in the list are explored. This enables searching over any sequence of parameter settings.

		scoring : str, callable, list/tuple or dict, default=None
			A single str (see The scoring parameter: defining model evaluation rules) or a callable (see Defining your scoring strategy from metric functions) to evaluate the predictions on the test set.

			For evaluating multiple metrics, either give a list of (unique) strings or a dict with names as keys and callables as values.

			NOTE that when using custom scorers, each scorer should return a single value. Metric functions returning a list/array of values can be wrapped into multiple scorers that return one value each.

		Examples
		----------

		-----------
		"""
		model = deepcopy(self._database.get(self._model_id)[0])
		input_features_list = self._get_input()
		input_feature = input_features_list[0]
		x_train, y_train = input_feature.get_2d_feature()

		# running grid search to find best parameters
		grid = model_selection.GridSearchCV(
			estimator=model, param_grid=params, scoring=scoring, verbose=3)
		grid_result = grid.fit(x_train, y_train)
		best_params = grid_result.best_params_

		for k, v in best_params.items():
			self._params[k] = v

	# @_deprecate_positional_args
	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database

		-----------
		"""
		model_data = deepcopy(self._database.get(self._model_id)[0])
		model = model_data._model
		input_features_list = self._get_input()
		input_feature = input_features_list[0]
		x_train, y_train = input_feature.get_2d_feature()
		x_train = x_train.reshape(x_train.shape[0], -1)
		model.set_params(**self._params)
		trained_model = model.fit(x_train, y_train)
		t_model = SKModel(
			id=self._outputs[0], model=trained_model, classifier=model_data._classifier)
		self._set_output(t_model, self._outputs[0])


class Test(Stage):
	"""
	DESCRIPTION
	-----------
	Tests the data using the trained model

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

	model_id : ID

		It's id of the train model

	"""
	in_out = {TwoDFeature: SimpleResult, OneDFeature: SimpleResult}

	# @_deprecate_positional_args
	def __init__(self, id: ID, database: Database, inputs: Tuple[ID, ...], outputs: Tuple[ID, ...], model_id: ID):
		"""
	DESCRIPTION
	-----------
	The Constructor for Test

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

	model_id : ID

		It's id of the train model

	"""
		super().__init__(id, database, inputs, outputs)
		self._model_id = model_id
		self.scoring = None

	# @_deprecate_positional_args
	def set_params(self, scoring: str):
		"""
		DESCRIPTION
		-----------
		set Scoring parameter

		Parameters
		----------
		scoring : str

			A single str (see The scoring parameter: defining model evaluation rules) to evaluate the predictions on the test set.

		-----------
		"""
		self.scoring = scoring

	# @_deprecate_positional_args
	def do_task(self):
		"""
		DESCRIPTION
		-----------
		Imports input from database and performs the task on it and saves output to database

		-----------
		"""
		model_data = deepcopy(self._database.get(self._model_id)[0])
		trained_model = model_data._model
		input_feature = self._get_input()[0]
		x_test, y_test = input_feature.get_2d_feature()
		x_test = x_test.reshape(x_test.shape[0], -1)
		y_pred = trained_model.predict(x_test)
		acc = 0
		if self.scoring == 'accuracy':
			acc = metrics.accuracy_score(y_test, y_pred)
		my_result = SimpleResult(
			id=self._outputs[0], result=acc, classifier=model_data._classifier)
		self._set_output(my_result, self._outputs[0])
