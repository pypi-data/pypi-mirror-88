# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2017, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# ******************************************************************

import numpy as np

from snapml.utils import _is_mpi_enabled, _check_devicendarray_types
from snapml._predict_utils import _predict_common_processing, _lr_single_row_predict
_mpi_enabled = _is_mpi_enabled()

from abc import ABC, abstractmethod
from collections import namedtuple

class GeneralizedLinearModel(ABC):
    PredictVars = namedtuple('PredictVars', ['num_ex' ,'num_ft' ,'num_train_unique_labs' ,
                             'X_ptr_' ,'X_type_' ,'indptr' ,'indices' ,'data' ,'shortcut_predict'])

    @abstractmethod
    def param_check(self):
        pass

    @abstractmethod
    def __init__(self):
        # just for reference
        self.max_iter = None,
        self.regularizer = None
        self.device_ids = None
        self.verbose = None
        self.use_gpu = None
        self.class_weight = None
        self.dual = None
        self.n_jobs = None
        self.penalty = None
        self.tol = None
        self.generate_training_history = None
        self.fit_intercept = None
        self.intercept_scaling = None
        self.privacy = None
        self.eta = None
        self.batch_size = None
        self.grad_clip = None
        self.privacy_epsilon = None
        self.is_regression = None
        self.fit_intercept = None
        self.intercept_scaling = None
        self.num_train_unique_labs = None
        self.model_size = None
        self.labels_flag = None
        self.params = None
        self.standard_predict_type = None
        pass

    @abstractmethod
    def set_classes(self, y_train):
        pass

    @abstractmethod
    def check_and_modify_labels(self, labs, y_train, y_train_device, gpu_matrix):
        pass

    @abstractmethod
    def c_fit(self,
                    balanced,
                    col_major,
                    num_ex,
                    num_ft,
                    num_nz,
                    indptr,
                    indices,
                    data,
                    labs,
                    gpu_data_ptr,
                    gpu_lab_ptr,
                    gpu_matrix,
                    X_train_ptr_,
                    X_train_type_,
                    generate_training_code):
        pass

    @abstractmethod
    def post_training(self, gpu_matrix, training_metadata, X_train, _mpi_enabled, num_ft):
        pass

    @abstractmethod
    def c_predict(self, n_jobs):
        pass

    @abstractmethod
    def post_predict(self, pred, num_train_unique_labs):
        pass

    def fit(self, X_train, y_train=None):

        """
        Fit the model according to the given train dataset.

        Parameters
        ----------
        X_train : Train dataset. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. DeviceNDArray. Not supported for MPI execution.
            3. SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        y_train : The target corresponding to X_train.
            If X_train is sparse matrix or dense matrix, y_train should be array-like of shape = (n_samples,)
            In case of deviceNDArray, y_train should be array-like of shape = (n_samples, 1)
            For binary classification the labels should be {-1, 1} or {0, 1}.
            If X_train is SnapML data partition type, then y_train is not required (i.e. None).

        Returns
        -------
        self : object
        """

        self.param_check()

        if self.regularizer < 0.0001:
            print("[Warning] Parameter regularizer: value might be too small.")

        if any(val < 0 for val in self.device_ids):
            raise ValueError("Parameter device_id: value too small. Should be an integer >= 0.")
        self.device_ids.sort()
        self.device_ids = np.array(self.device_ids).astype(np.uint32)

        if (self.use_gpu == True):
            if (not self.n_jobs % 32 == 0):
                print("[Info] If set n_jobs should be a multiple of 32. GPU training will run with n_jobs=256.")
                self.n_jobs = 256
        else:
            if (self.n_jobs > 1):
                print("[Info] Training will run in multi-threaded mode on CPU.")
            else:
                print("[Info] Training will run in single-threaded mode on CPU.")

        if (self.use_gpu == False) and (len(self.device_ids) > 0):
            print("[Warning] Parameter device_ids will be ignored. The use_gpu parameter was set to False. The training will run on the CPU.")

        if (self.use_gpu == True) and (len(self.device_ids) == 0):
            # With MPI, we recommend snaprun instead of mpirun. snaprun gives
            # 1 GPU per process. So no need of device_ids as argument for that case.
            if not _mpi_enabled:
                print("[Warning] Parameter device_ids not set. The training will run on GPU 0.")

        if ((self.penalty == "l1") and (self.dual)):
            raise ValueError("L1 regularization is supported only for primal optimization problems. Set dual to False.")

        if(_mpi_enabled and self.privacy):
            raise ValueError("Privacy not supported for MPI execution. Set privacy=False.")

        if(self.privacy and self.dual):
            raise ValueError("Privacy only supported for primal objective functions.")

        if(self.privacy and self.penalty == "l1"):
            raise ValueError("Privacy only supported for L2-regularized objective functions.")

        if(self.privacy and self.use_gpu):
            print("[Warning] Privacy not supported by GPU solvers. Will train on CPU")

        if(self.privacy and self.fit_intercept):
            raise ValueError("Privacy not supported with fit_intercept=True.")

        if (hasattr(self,'balanced') and self.class_weight == 'balanced'):
            balanced = True
        else:
            balanced = False

        self.set_classes(y_train)

        # Performing all the initial checks for DeviceNDArray inputs
        _check_devicendarray_types(X_train, y_train, self)

        # if we are solving the primal case (without privacy)
        # then we need the data to be col-major
        col_major = (not self.dual) and (not self.privacy)

        # enforce col/row major
        if type(X_train).__name__ == 'ndarray':
            if col_major:
                X_train = np.asfortranarray(X_train, dtype=np.float32)
            else:
                X_train = np.ascontiguousarray(X_train, dtype=np.float32)
        elif type(X_train).__name__ == 'csr_matrix':
            if col_major:
                X_train = X_train.tocsc()
        elif type(X_train).__name__ == 'csc_matrix':
            if not col_major:
                X_train = X_train.tocsr()

        # define set of valid python data types depending on parameters
        if self.privacy:
            valid_types = ['ndarray','csr_matrix']
        else:
            valid_types = ['ndarray', 'SparsePartition', 'DensePartition', 'ConstantValueSparsePartition']

            if self.dual:
                valid_types.append('csr_matrix')
            else:
                valid_types.append('csc_matrix')

            if not _mpi_enabled:
                valid_types.append('DeviceNDArray')

        # check that the data is one of the types
        if type(X_train).__name__ not in valid_types:
            raise ValueError("X_train has type %s, but for the parameter specification [_mpi_enabled: %d, dual: %d, privacy: %d] it must have one of the following types: "
                % (type(X_train).__name__, _mpi_enabled, self.dual, self.privacy), valid_types)

        # populate fields
        X_train_ptr_ = ""
        X_train_type_ = -1
        num_ex = 0
        num_ft = 0
        num_nz = 0
        indptr = np.array([])
        indices = np.array([])
        data = np.array([], dtype=np.float32)
        labs = np.array([])
        y_train_device = np.array([])
        # by default gpu_matrix is set to False.
        # It will be set to True if xtrain and ytrain is coming from GPU device.
        gpu_matrix = False
        gpu_data_ptr = 0
        gpu_lab_ptr = 0

        # first check if X_train is a custom Snap ML data structure
        if type(X_train).__name__ in ['SparsePartition', 'DensePartition', 'ConstantValueSparsePartition']:
            X_train_ptr_ = X_train.ptr_
            X_train_type_ = X_train.type_
        else:

            # get number of examples/features
            num_ex = X_train.shape[0]
            num_ft = X_train.shape[1]

            # check that y_train was provided
            if y_train is None:
                raise ValueError("Parameter y_train: Input data is required.")

            # in most cases, y_train should contain all examples
            if (not _mpi_enabled) or (not self.dual):
                assert len(y_train) == num_ex

            # numpy array
            if (type(X_train).__name__ == "ndarray"):
                num_nz    = num_ex * num_ft
                data      = X_train
                labs      = y_train.astype(np.float32)

            # sparse matrices
            if (type(X_train).__name__ in ["csr_matrix", "csc_matrix"]):
                num_nz    = X_train.nnz
                indptr    = X_train.indptr.astype(np.uint64)
                data      = X_train.data.astype(np.float32)
                indices   = X_train.indices.astype(np.uint32)
                labs      = y_train.astype(np.float32)
                if (self.fit_intercept == True):
                    print("[Warning] May affect speed of convergence for sparse datasets as fit_intercept is set.")

            # deviceNDarray
            if (type(X_train).__name__ == "DeviceNDArray"):
                num_nz    = num_ex * num_ft
                # data      = np.ascontiguousarray(data)   # ensure row-major format - is it necessary?
                gpu_matrix = True
                # data_ptr will have GPU device address.
                gpu_data_ptr   = X_train.device_ctypes_pointer.value
                gpu_lab_ptr    = y_train.device_ctypes_pointer.value
                # To find unique label we are copying lab into host as ndarray so that np.unique() can be performed
                # TODO : avoid the separate host copy
                y_train_host   = y_train.copy_to_host()
                y_train_device = y_train
                y_train        = y_train_host
                labs           = y_train.astype(np.float32)

        if(self.generate_training_history is None):
            generate_training_code = 0
        elif(self.generate_training_history == 'summary'):
            generate_training_code = 1
        else:
            generate_training_code = 2

        labs = self.check_and_modify_labels(labs, y_train, y_train_device, gpu_matrix)

        out_fit = self.c_fit(balanced,
                                   col_major,
                                   num_ex,
                                   num_ft,
                                   num_nz,
                                   indptr,
                                   indices,
                                   data,
                                   labs,
                                   gpu_data_ptr,
                                   gpu_lab_ptr,
                                   gpu_matrix,
                                   X_train_ptr_,
                                   X_train_type_,
                                   generate_training_code)

        self.model_ = out_fit[0]
        if generate_training_code == 0:
            self.training_history_ = None
        else:
            self.training_history_ = out_fit[1]
        if not _mpi_enabled:
            self.support_ = np.array(out_fit[2], np.int32)
            self.n_iter_ = out_fit[3]

        # training_metadata
        training_metadata = out_fit[4]
        self.model_size = training_metadata['model_size']                

        # Assign the model to the coef_ attribute
        self.coef_ = self.model_.T

        self.post_training(gpu_matrix, training_metadata, X_train, _mpi_enabled, num_ft)

        return self

    def pre_predict_is_single(self, X, _mpi_enabled, predict_type):


        pred_vars = GeneralizedLinearModel.PredictVars._make(_predict_common_processing(
            self, X, self.is_regression, _mpi_enabled))       

        pred = np.array([])
        # Compute predictions/probabilities
        if pred_vars.shortcut_predict and X.shape[0] == 1:
            # Inference for single row numpy or csr (local mode only)
            pred = _lr_single_row_predict(self.model_, self.fit_intercept, X, predict_type)
            return True, pred, pred_vars
        else:
            return False, pred, pred_vars

    def predict(self, X, n_jobs=0):

        """
        Class predictions

        The returned class estimates.

        Parameters
        ----------
        X : Dataset used for predicting estimates or class. Supports the following input data-types :
            1. Sparse matrix (csr_matrix, csc_matrix) or dense matrix (ndarray)
            2. SnapML data partition of type DensePartition, SparsePartition or ConstantValueSparsePartition

        n_jobs : int, default=0
            Number of threads used to run inference.
            By default inference runs with maximum number of available threads.
            This parameter is ignored for predict of a single observation.

        Returns
        -------
        pred: array-like, shape = (n_samples,)
            Returns the predicted estimate/class of the sample.
        """

        is_single, pred, pred_vars = self.pre_predict_is_single(X, _mpi_enabled, self.standard_predict_type)

        if is_single == False:
            # Multi-row or snap-data or MPI
            pred, pred_metadata = self.c_predict(n_jobs, pred_vars)

        return self.post_predict(pred, pred_vars.num_train_unique_labs)

