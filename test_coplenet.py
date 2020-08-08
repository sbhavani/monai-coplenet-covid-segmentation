# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import torch
from parameterized import parameterized

from coplenet import CopleNet

TEST_CASES = [
    [{"spatial_dims": 2}, torch.randn(16, 1, 32, 32), (16, 2, 32, 32)],  # single channel 2D, batch 16, no residual
    [
        {"spatial_dims": 2, "in_channels": 5, "out_channels": 4},
        torch.randn(16, 5, 32, 32),
        (16, 4, 32, 32),
    ],  # 5-channel 2D, batch 16
    [{"spatial_dims": 2}, torch.randn(16, 1, 32, 48, 48), (16, 2, 32, 48, 48)],  # 1-channel 3D, batch 16
    [
        {"spatial_dims": 2, "bilinear": False},
        torch.randn(16, 1, 32, 64, 48),
        (16, 2, 32, 64, 48),
    ],  # 1-channel 3D, batch 16
    [
        {"spatial_dims": 2, "in_channels": 2, "out_channels": 3, "bilinear": False},
        torch.randn(16, 2, 32, 64, 48),
        (16, 3, 32, 64, 48),
    ],  # 4-channel 3D, batch 16, batch normalisation
]


class TestCopleNET(unittest.TestCase):
    @parameterized.expand(TEST_CASES)
    def test_shape(self, input_param, input_data, expected_shape):
        net = CopleNet(**input_param)
        if torch.cuda.is_available():
            net = net.to(torch.device("cuda"))
            input_data = input_data.to(torch.device("cuda"))
        net.eval()
        with torch.no_grad():
            result = net.forward(input_data.float())
            self.assertEqual(result.shape, expected_shape)


if __name__ == "__main__":
    unittest.main()
