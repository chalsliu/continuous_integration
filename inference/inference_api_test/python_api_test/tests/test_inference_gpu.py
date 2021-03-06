# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest
import os
import sys
import argparse
import logging
import struct
import six

import numpy as np

sys.path.append("..")
from src.test_case import Predictor

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


def parse_args():
    """
    parse input arguments
    Return:
        test_args(argparse)
        remaining_args(argparse)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model_path', type=str, default='', help='A path to infer model.')
    parser.add_argument(
        '--data_path', type=str, default='', help='A path to a data.json')
    parser.add_argument(
        '--delta', type=float, default=1e-4, help='compare results delta')

    test_args, args = parser.parse_known_args(namespace=unittest)
    return test_args, sys.argv[:1] + args


class TestModelInferenceGPU(unittest.TestCase):
    """
    TestModelInferenceGPU
    Args:
    Return:
    """

    def check_data(self, result, expect):
        """
        check result
        Args:
            result(list): list of result data
            expect(list): list of expect data
        Return:
            None
        """
        delta = test_case_args.delta
        logger.info("current comparison delta is : {0}".format(delta))
        assert len(expect) == len(result)
        for i in range(0, len(expect)):
            self.assertAlmostEqual(expect[i], result[i], delta=delta)

    def test_inference(self):
        """
        Inference and check value
        Args:
            model_path(string): parent path of __model__ file
            data_path(string): path of data.json
        Return:
            None
        """
        model_path = test_case_args.model_path
        data_path = test_case_args.data_path
        AnalysisPredictor = Predictor(
            model_path, predictor_mode="Analysis", config_type="gpu")
        res, ave_time = AnalysisPredictor.analysis_predict(data_path)
        logger.info(ave_time)

        NativePredictor = Predictor(
            model_path, predictor_mode="Native", config_type="gpu")
        exp, ave_time = NativePredictor.native_predict(data_path)
        logger.info(ave_time)

        assert len(exp) == len(res)
        for i in range(len(res)):
            self.check_data(res[i].flatten(), exp[i].flatten())


if __name__ == '__main__':
    global test_case_args
    test_case_args, remaining_args = parse_args()
    unittest.main(argv=remaining_args)
