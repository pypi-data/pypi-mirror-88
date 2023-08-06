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

from snapml.utils import _is_mpi_enabled
_mpi_enabled = _is_mpi_enabled()

from snapml.GeneralizedLinearModel import GeneralizedLinearModel

class GeneralizedLinearModelRegressor(GeneralizedLinearModel):

    def set_classes(self, y_train):
       pass

    def check_and_modify_labels(self, labs, y_train, y_train_device, gpu_matrix):
        return labs

    def post_predict(self, pred, num_train_unique_labs):
        return pred