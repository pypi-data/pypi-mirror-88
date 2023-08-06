# Copyright (c) 2019 Fabien Georget <fabien.georget@epfl.ch>, EPFL
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from ..core.experiment import PartOfExperiment
from skimage.color import grey2rgb
from skimage.color import rgb2hsv

import numpy as np

class CompositeMap(PartOfExperiment):
    """A composite map"""
    def __init__(self, composite_img, channels, parent):
        super().__init__(parent)
        self._img = composite_img
        self._channels = channels
        self._parent = parent

    @property
    def map(self):
        return self._img

    @property
    def channels(self):
        """Return the channels use to build this composite image."""
        return self._channels

    def mix_with_bse(self, bse, alpha):
        self._img = self._img*alpha+(1.0-alpha)*grey2rgb(bse.map)

    @property
    def hsv(self):
        return rgb2hsv(self._img)

    def to_features_matrix(self, rgb=True):
        if rgb:
            tensor = self._img
        else:
            tensor = self.hsv()

        nb_points = tensor.shape[0]*tensor.shape[1]
        array = np.zeros((nb_points, 3))
        for feat in range(3):
            array[:, feat] = tensor[:,:,feat].flatten()

        return tensor