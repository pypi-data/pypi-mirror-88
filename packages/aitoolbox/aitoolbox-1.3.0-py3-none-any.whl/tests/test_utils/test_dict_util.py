import unittest

from aitoolbox.utils import dict_util


class TestCombinePredictionMetadataBatches(unittest.TestCase):
    def test_combine_prediction_metadata_batches(self):
        metadata_batches = [
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))}
        ]

        combined_metadata = dict_util.combine_prediction_metadata_batches(metadata_batches)
        self.assertEqual(combined_metadata,
                         {'meta_1': [1, 100, 1000, 10000] * 4, 'meta_2': list(range(4)) * 4})

    def test_combine_metadata_dicts_with_elements_missing(self):
        metadata_batches = [
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4)), 'meta_2_special': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4)), 'meta_2_special': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))}
        ]

        combined_metadata = dict_util.combine_prediction_metadata_batches(metadata_batches)
        self.assertEqual(
            combined_metadata,
            {'meta_1': [1, 100, 1000, 10000] * 4,
             'meta_2': list(range(4)) * 4,
             'meta_2_special': list(range(4)) * 2}
        )

    def test_combine_metadata_dicts_with_varying_elements(self):
        metadata_batches = [
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4)), 'meta_2_special': list(range(2))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4))},
            {'meta_1': [1, 100, 1000, 10000], 'meta_2': list(range(4)), 'completely_new_meta': ['334', '1000', 'bla']}
        ]

        combined_metadata = dict_util.combine_prediction_metadata_batches(metadata_batches)
        self.assertEqual(
            combined_metadata,
            {'meta_1': [1, 100, 1000, 10000] * 4,
             'meta_2': list(range(4)) * 4,
             'meta_2_special': list(range(2)),
             'completely_new_meta': ['334', '1000', 'bla']}
        )


class TestFlattenDict(unittest.TestCase):
    def test_flatten_dict(self):
        input_dict = {'bla': 12, 'www': 455, 'pppp': 4004}
        self.assertEqual(dict_util.flatten_dict(input_dict), input_dict)

        input_dict_1_level = {'bla': {'uuu': 334, 'www': 1010}, 'rogue': {'ppp': 123}}
        self.assertEqual(dict_util.flatten_dict(input_dict_1_level),
                         {'bla_uuu': 334, 'bla_www': 1010, 'rogue_ppp': 123})
        
        input_dict_2_level = {'bla': {'rogue_1': {'m': 10, 'p': 11}, 'rogue_2': {'m': 20, 'p': 22}}}
        self.assertEqual(dict_util.flatten_dict(input_dict_2_level),
                         {'bla_rogue_1_m': 10, 'bla_rogue_1_p': 11, 'bla_rogue_2_m': 20, 'bla_rogue_2_p': 22})


class TestCombineDictElements(unittest.TestCase):
    def test_combine_dict_elements(self):
        list_of_dicts = [
            {'acc': 0.9, 'f1': 0., 'ROC': 0.95, 'PR': 0.88},
            {'acc': 0.92, 'f1': 0.1, 'ROC': 0.92, 'PR': 0.48},
            {'acc': 0.33, 'f1': 0.2, 'ROC': 0.965, 'PR': 0.8338},
            {'acc': 0.22, 'f1': 0.3, 'ROC': 0., 'PR': 0.38}
        ]

        combined_dict = dict_util.combine_dict_elements(list_of_dicts)
        self.assertEqual(combined_dict,
                         {'acc': [0.9, 0.92, 0.33, 0.22], 'f1': [0.0, 0.1, 0.2, 0.3],
                          'ROC': [0.95, 0.92, 0.965, 0.0], 'PR': [0.88, 0.48, 0.8338, 0.38]})

    def test_combine_dict_with_non_matching_elements(self):
        list_of_dicts = [
            {'acc': 0.9, 'f1': 0., 'ROC': 0.95, 'New_metric_1': 0.88},
            {'acc': 0.92, 'f1': 0.1, 'New_metric_3': 0.92, 'PR': 0.48},
            {'acc': 0.33, 'New_metric_2': 0.2, 'ROC': 0.965, 'PR': 0.8338},
            {'acc': 0.22, 'New_metric_2': 0.3, 'New_metric_3': 0., 'ROC': 0.2, 'PR': 0.38}
        ]

        combined_dict = dict_util.combine_dict_elements(list_of_dicts)
        self.assertEqual(combined_dict,
                         {'acc': [0.9, 0.92, 0.33, 0.22], 'f1': [0.0, 0.1], 'ROC': [0.95, 0.965, 0.2],
                          'New_metric_1': [0.88], 'New_metric_3': [0.92, 0.0], 'PR': [0.48, 0.8338, 0.38],
                          'New_metric_2': [0.2, 0.3]})


class TestFlattenCombineDict(unittest.TestCase):
    def test_flatten_combine_dict(self):
        dict_sub_dict = {'loss': [1., 11.], 'accumulated_loss': [2., 3.], 'val_loss': [3, 100],
                         'ROGUE': [{'m1': 0.9, 'm2:': 22.}, {'m1': 0.3, 'm2:': 221.}]}

        self.assertEqual(dict_util.flatten_combine_dict(dict_sub_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0, 3.0], 'val_loss': [3, 100],
                          'ROGUE_m1': [0.9, 0.3], 'ROGUE_m2:': [22.0, 221.0]})

        dict_sub_dict = {'loss': [1., 11.], 'accumulated_loss': [2., 3.], 'val_loss': [3, 100],
                         'ROGUE': [{'m1': 0.9, 'm2:': 22.}, {'m1': 0.3, 'm2:': 221.}, {'m1': 100., 'm2:': 2121.}]}

        self.assertEqual(dict_util.flatten_combine_dict(dict_sub_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0, 3.0], 'val_loss': [3, 100],
                          'ROGUE_m1': [0.9, 0.3, 100.0], 'ROGUE_m2:': [22.0, 221.0, 2121.0]})

    def test_multiple_flatten_combine_dict(self):
        dict_sub_dict = {'loss': [1., 11.], 'accumulated_loss': [2., 3.], 'val_loss': [3, 100],
                         'ROGUE': [{'m1': 0.9, 'm2:': 22.}, {'m1': 0.3, 'm2:': 221.}],
                         'New_metric': [{'mn1': 0.9, 'mn2:': 22.}, {'mn1': 0.3, 'mn2:': 221.}]}

        self.assertEqual(dict_util.flatten_combine_dict(dict_sub_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0, 3.0], 'val_loss': [3, 100],
                          'ROGUE_m1': [0.9, 0.3], 'ROGUE_m2:': [22.0, 221.0],
                          'New_metric_mn1': [0.9, 0.3], 'New_metric_mn2:': [22.0, 221.0]})

    def test_multiple_uneven_flatten_combine_dict(self):
        dict_sub_dict = {'loss': [1., 11.], 'accumulated_loss': [2., 3.], 'val_loss': [3, 100],
                         'ROGUE': [{'m1': 0.9, 'm2:': 22.}, {'m1': 0.3, 'm2:': 221.}],
                         'New_metric': [{'mn1': 0.9, 'mn2:': 22.}, {'mn1': 0.3, 'mn2:': 221.}],
                         'Uneven_metric': [{'mn1': 0.9, 'mn2:': 22., 'NEW_submetric': 23.},
                                           {'mn1': 0.3, 'NEW_submetric_2': 44., 'mn2:': 221.}]}

        self.assertEqual(dict_util.flatten_combine_dict(dict_sub_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0, 3.0], 'val_loss': [3, 100],
                          'ROGUE_m1': [0.9, 0.3], 'ROGUE_m2:': [22.0, 221.0],
                          'New_metric_mn1': [0.9, 0.3], 'New_metric_mn2:': [22.0, 221.0],
                          'Uneven_metric_mn1': [0.9, 0.3], 'Uneven_metric_mn2:': [22.0, 221.0],
                          'Uneven_metric_NEW_submetric': [23.0],
                          'Uneven_metric_NEW_submetric_2': [44.0]})

    def test_flatten_combine_dict_no_nested_dict(self):
        simple_dict = {'loss': [1., 11.], 'accumulated_loss': [2., 3.], 'val_loss': [3, 100]}
        self.assertEqual(dict_util.flatten_combine_dict(simple_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0, 3.0], 'val_loss': [3, 100]})

        un_even_dict = {'loss': [1., 11.], 'accumulated_loss': [2.], 'val_loss': [3, 100, 234]}
        self.assertEqual(dict_util.flatten_combine_dict(un_even_dict),
                         {'loss': [1.0, 11.0], 'accumulated_loss': [2.0], 'val_loss': [3, 100, 234]})
