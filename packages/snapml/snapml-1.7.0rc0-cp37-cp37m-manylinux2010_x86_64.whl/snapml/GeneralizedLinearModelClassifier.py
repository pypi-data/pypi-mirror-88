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
import math

from snapml.utils import _is_mpi_enabled, _is_data_snapml_partition_type
_mpi_enabled = _is_mpi_enabled()

from snapml.GeneralizedLinearModel import GeneralizedLinearModel

class GeneralizedLinearModelClassifier(GeneralizedLinearModel):

    def set_classes(self, y_train):
        # Number of unique labels used in _check_devicendarray_types, 
        #Added here to avoid multiple use of unique().
        self.classes_ = np.unique(y_train)

    def check_and_modify_labels(self, labs, y_train, y_train_device, gpu_matrix):

        # Check and modify the labels of y_train
        _multiclass = False
        if ((y_train is not None) and (not _is_data_snapml_partition_type(y_train))):
            if _mpi_enabled:
                labs = y_train.astype(np.float32)
            else: #local
                if(len(self.classes_) == 1):
                    raise ValueError("There must be at least two unique label values in the training data")
                elif (len(self.classes_) == 2):
                    _multiclass = False
                    if ( (self.classes_[0] == 0 and self.classes_[1] == 1)):
                        self.labels_flag = True
                        if (gpu_matrix == False ):
                            labs = 2.0 * y_train.astype(np.float32) - 1.0
                        else:
                            labs = 2.0 * y_train.astype(np.float32) - 1.0
                            index = 16
                            th_per_blk = (index,index)
                            bl_per_grd_x = math.ceil(y_train_device.shape[0] / th_per_blk[0])
                            bl_per_grd_y = math.ceil(y_train_device.shape[1] / th_per_blk[1])
                            bl_per_grd  = (bl_per_grd_x,bl_per_grd_y)
                            from snapml._gpu_utils import _convert_labs, _cuda_synchronize
                            _convert_labs[bl_per_grd, th_per_blk](y_train_device)
                            _cuda_synchronize()
                    elif (not(self.classes_[0] == -1 and self.classes_[1] == 1)):
                        raise ValueError("The labels in the train dataset should be {-1, 1} or {0, 1}.")
                    else:
                        if (gpu_matrix == False):
                            labs = y_train.astype(np.float32)
                else:
                    labs = y_train.astype(np.float32)
                    _multiclass = True
        return labs

    def post_predict(self, pred, num_train_unique_labs):
        # For binary classification transform the labels if needed
        if ((num_train_unique_labs <= 2) and (self.labels_flag)):
            pred = (pred + 1) / 2

        # Multi-class classification case
        if (num_train_unique_labs > 2):
            pred = np.argmax(pred, axis=0)

            class_to_index_mapping = np.array([])
            for class_ in self.classes_:
                class_to_index_mapping = np.append(class_to_index_mapping, class_)

            for example_index in range(len(pred)):
                pred[example_index] = class_to_index_mapping[pred[example_index]]

            pred = pred.astype(np.float64)

        return pred   