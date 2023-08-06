import unittest
import os

from tests.utils import *

from torch.utils.data.dataset import TensorDataset
from torch.utils.data.dataloader import DataLoader
from torch.optim.adam import Adam

from aitoolbox.torchtrain.train_loop import TrainLoop
from aitoolbox.torchtrain.model import ModelWrap
from aitoolbox.torchtrain.tl_components.callback_handler import CallbacksHandler
from aitoolbox.torchtrain.multi_loss_optim import MultiOptimizer
from aitoolbox.torchtrain.schedulers.basic import ReduceLROnPlateauScheduler, StepLRScheduler
from aitoolbox.torchtrain.schedulers.warmup import LinearWithWarmupScheduler
from aitoolbox.torchtrain.callbacks.basic import EarlyStopping, ListRegisteredCallbacks


class TestTrainLoop(unittest.TestCase):
    def test_init_values(self):
        train_loop_non_val = TrainLoop(NetUnifiedBatchFeed(), None, None, None, None, None)
        self.assertEqual(train_loop_non_val.train_history.train_history, {'loss': [], 'accumulated_loss': []})

        train_loop = TrainLoop(NetUnifiedBatchFeed(), None, 100, None, None, None)
        self.assertEqual(train_loop.train_history.train_history, {'loss': [], 'accumulated_loss': [], 'val_loss': []})

        self.assertEqual(train_loop.callbacks, [])
        self.assertIsInstance(train_loop.callbacks_handler, CallbacksHandler)
        self.assertEqual(train_loop.callbacks_handler.train_loop_obj, train_loop)
        self.assertFalse(train_loop.early_stop)
        self.assertIsNone(train_loop.amp_scaler)

    def test_fit_mode_selection_single_gpu(self):
        gpu_mode, num_epochs, callbacks, grad_accumulation = self.execute_train_loop_fit_in_mode('single')

        self.assertEqual(gpu_mode, 'train_single')
        self.assertEqual(num_epochs, 5)
        self.assertEqual(callbacks, [10])
        self.assertEqual(grad_accumulation, 1)

    def test_fit_mode_selection_dp(self):
        gpu_mode, num_epochs, callbacks, grad_accumulation, dp_model_args = \
            self.execute_train_loop_fit_in_mode('dp', dp_model_args={'aaa': 1})

        self.assertEqual(gpu_mode, 'train_dp')
        self.assertEqual(num_epochs, 5)
        self.assertEqual(callbacks, [10])
        self.assertEqual(grad_accumulation, 1)
        self.assertEqual(dp_model_args, {'aaa': 1})

    def test_fit_mode_selection_ddp(self):
        gpu_mode, num_epochs, callbacks, grad_accumulation, ddp_model_args, in_process_data_load, num_nodes = \
            self.execute_train_loop_fit_in_mode(
                'ddp',
                ddp_model_args={'aaa': 1}, in_process_data_load='bla', num_nodes=5
            )

        self.assertEqual(gpu_mode, 'train_ddp')
        self.assertEqual(num_epochs, 5)
        self.assertEqual(callbacks, [10])
        self.assertEqual(grad_accumulation, 1)
        self.assertEqual(ddp_model_args, {'aaa': 1})
        self.assertEqual(in_process_data_load, 'bla')
        self.assertEqual(num_nodes, 5)

    @staticmethod
    def execute_train_loop_fit_in_mode(gpu_mode, **fit_kwargs):
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))
        model = NetUnifiedBatchFeed()

        tl = TrainLoopFitMethodTracking(
            model, dummy_train_loader, dummy_val_loader, dummy_test_loader,
            dummy_optimizer, dummy_loss,
            gpu_mode=gpu_mode
        )
        return tl.fit(5, callbacks=[10], **fit_kwargs)

    def test_callback_registration(self):
        train_loop = TrainLoop(NetUnifiedBatchFeed(), None, 100, None, None, None)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort()])

        self.assertEqual(len(train_loop.callbacks), 3)
        for reg_cb, true_cb in zip(train_loop.callbacks, [AbstractCallback, CallbackTracker, CallbackTrackerShort]):
            self.assertEqual(type(reg_cb), true_cb)
        for reg_cb in train_loop.callbacks:
            self.assertEqual(reg_cb.train_loop_obj, train_loop)

        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test2')])
        self.assertEqual(len(train_loop.callbacks), 4)
        for reg_cb, true_cb in zip(train_loop.callbacks, [AbstractCallback, CallbackTracker, CallbackTrackerShort, AbstractCallback]):
            self.assertEqual(type(reg_cb), true_cb)

        for reg_cb in train_loop.callbacks:
            self.assertEqual(reg_cb.train_loop_obj, train_loop)

        for reg_cb, cb_name in zip(train_loop.callbacks,
                                   ['callback_test1', 'CallbackTracker1', 'CallbackTracker2', 'callback_test2']):
            self.assertEqual(reg_cb.callback_name, cb_name)

    def test_callback_registration_reordering(self):
        cb_1 = AbstractCallback('callback_test1')
        cb_1.execution_order = 10
        cb_2 = CallbackTracker()
        cb_2.execution_order = 0
        cb_3 = CallbackTrackerShort()
        cb_3.execution_order = 7

        train_loop = TrainLoop(NetUnifiedBatchFeed(), None, 100, None, None, None)
        train_loop.callbacks_handler.register_callbacks([cb_1, cb_2, cb_3])

        self.assertEqual(len(train_loop.callbacks), 3)
        for reg_cb, true_cb in zip(train_loop.callbacks, [CallbackTracker, CallbackTrackerShort, AbstractCallback]):
            self.assertEqual(type(reg_cb), true_cb)

        for reg_ord, true_ord in zip([cb.execution_order for cb in train_loop.callbacks], [0, 7, 10]):
            self.assertEqual(reg_ord, true_ord)

        cb_4 = AbstractCallback('callback_test2')
        cb_4.execution_order = 2
        cb_5 = AbstractCallback('callback_test3')
        cb_5.execution_order = 100
        train_loop.callbacks_handler.register_callbacks([cb_4, cb_5])

        self.assertEqual(len(train_loop.callbacks), 5)
        for reg_cb, true_cb in zip(train_loop.callbacks, [CallbackTracker, AbstractCallback, CallbackTrackerShort,
                                                          AbstractCallback, AbstractCallback]):
            self.assertEqual(type(reg_cb), true_cb)

        for reg_ord, true_ord in zip([cb.execution_order for cb in train_loop.callbacks], [0, 2, 7, 10, 100]):
            self.assertEqual(reg_ord, true_ord)

    def test_callback_on_execution(self):
        num_epochs = 2
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = NetUnifiedBatchFeed()
        train_loop = TrainLoop(model, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, dummy_loss)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort(),
                                                         AbstractCallback('callback_test2')])

        callback_full = train_loop.callbacks[1]
        callback_short = train_loop.callbacks[2]

        model_return = train_loop.fit(num_epochs=num_epochs)

        self.assertEqual(model, model_return)
        self.assertFalse(train_loop.early_stop)
        self.assertEqual(train_loop.epoch, num_epochs-1)
        self.assertEqual(dummy_loss.device.type, 'cpu')

        self.assertEqual(model.dummy_batch.back_ctr, num_epochs*len(dummy_train_loader))
        self.assertEqual(model.dummy_batch.item_ctr,
                         num_epochs * len(dummy_train_loader) + num_epochs * len(dummy_train_loader) +
                         num_epochs * len(dummy_val_loader) +
                         len(dummy_test_loader))

        self.assertEqual(dummy_optimizer.zero_grad_ctr, num_epochs*len(dummy_train_loader))
        self.assertEqual(dummy_optimizer.step_ctr, num_epochs * len(dummy_train_loader))

        self.assertEqual(callback_full.callback_calls,
                         ['on_train_loop_registration', 'on_train_begin', 'on_epoch_begin', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_epoch_end',
                          'on_epoch_begin', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_epoch_end', 'on_train_end'])
        self.assertEqual(callback_full.call_ctr,
                         {'on_train_loop_registration': 1, 'on_epoch_begin': 2, 'on_epoch_end': 2, 'on_train_begin': 1,
                          'on_train_end': 1, 'on_batch_begin': 8, 'on_batch_end': 8,
                          'on_after_gradient_update': 8, 'on_after_optimizer_step': 8})

        self.assertEqual(callback_short.callback_calls,
                         ['on_epoch_begin', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_epoch_end', 'on_epoch_begin',
                          'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_epoch_end', 'on_train_end'])
        self.assertEqual(callback_short.call_ctr,
                         {'on_train_loop_registration': 0, 'on_epoch_begin': 2, 'on_epoch_end': 2, 'on_train_begin': 0,
                          'on_train_end': 1, 'on_batch_begin': 8, 'on_batch_end': 0,
                          'on_after_gradient_update': 8, 'on_after_optimizer_step': 8})

    def test_callback_on_execution_separate_batch_feed(self):
        num_epochs = 2
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = Net()
        dummy_feed_def = DeactivateModelFeedDefinition()
        model_wrap = ModelWrap(model=model, batch_model_feed_def=dummy_feed_def)

        train_loop = TrainLoop(model_wrap, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, dummy_loss)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort(),
                                                         AbstractCallback('callback_test2')])

        callback_full = train_loop.callbacks[1]
        callback_short = train_loop.callbacks[2]

        model_return = train_loop.fit(num_epochs=num_epochs)

        self.assertEqual(model, model_return)
        self.assertFalse(train_loop.early_stop)
        self.assertEqual(train_loop.epoch, num_epochs-1)

        self.assertEqual(dummy_feed_def.dummy_batch.back_ctr, num_epochs*len(dummy_train_loader))
        self.assertEqual(dummy_feed_def.dummy_batch.item_ctr,
                         num_epochs * len(dummy_train_loader) + num_epochs * len(dummy_train_loader) +
                         num_epochs * len(dummy_val_loader) +
                         len(dummy_test_loader))

        self.assertEqual(dummy_optimizer.zero_grad_ctr, num_epochs*len(dummy_train_loader))
        self.assertEqual(dummy_optimizer.step_ctr, num_epochs * len(dummy_train_loader))
        self.assertEqual(dummy_loss.device.type, 'cpu')

        self.assertEqual(callback_full.callback_calls,
                         ['on_train_loop_registration', 'on_train_begin', 'on_epoch_begin', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_end', 'on_epoch_end',
                          'on_epoch_begin', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_end', 'on_epoch_end', 'on_train_end'])
        self.assertEqual(callback_full.call_ctr,
                         {'on_train_loop_registration': 1, 'on_epoch_begin': 2, 'on_epoch_end': 2, 'on_train_begin': 1,
                          'on_train_end': 1, 'on_batch_begin': 8, 'on_batch_end': 8,
                          'on_after_gradient_update': 8, 'on_after_optimizer_step': 8})

        self.assertEqual(callback_short.callback_calls,
                         ['on_epoch_begin', 'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step',
                          'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_epoch_end', 'on_epoch_begin',
                          'on_batch_begin', 'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_batch_begin',
                          'on_after_gradient_update', 'on_after_optimizer_step', 'on_epoch_end', 'on_train_end'])
        self.assertEqual(callback_short.call_ctr,
                         {'on_train_loop_registration': 0, 'on_epoch_begin': 2, 'on_epoch_end': 2, 'on_train_begin': 0,
                          'on_train_end': 1, 'on_batch_begin': 8, 'on_batch_end': 0,
                          'on_after_gradient_update': 8, 'on_after_optimizer_step': 8})

    def test_predict_train_data(self):
        self.eval_prediction('train')
        self.eval_prediction_separate_batch_feed('train')

    def test_predict_val_data(self):
        self.eval_prediction('val')
        self.eval_prediction_separate_batch_feed('val')

    def test_predict_test_data(self):
        self.eval_prediction('test')
        self.eval_prediction_separate_batch_feed('test')

    def eval_prediction(self, eval_mode):
        num_epochs = 2
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = NetUnifiedBatchFeed()
        train_loop = TrainLoop(model, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, dummy_loss)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort(),
                                                         AbstractCallback('callback_test2')])
        train_loop.fit(num_epochs=num_epochs)

        if eval_mode == 'train':
            y_pred, y_test, metadata = train_loop.predict_on_train_set()
            data_loader = dummy_train_loader
        elif eval_mode == 'val':
            y_pred, y_test, metadata = train_loop.predict_on_validation_set()
            data_loader = dummy_val_loader
        else:
            y_pred, y_test, metadata = train_loop.predict_on_test_set()
            data_loader = dummy_test_loader

        r = []
        for i in range(1, len(data_loader) + 1):
            r += [i] * 64
        r2 = []
        for i in range(1, len(data_loader) + 1):
            r2 += [i + 100] * 64
        self.assertEqual(y_test.tolist(), r)
        self.assertEqual(y_pred.tolist(), r2)

        d = {'bla': []}
        for i in range(1, len(data_loader) + 1):
            d['bla'] += [i + 200] * 64
        self.assertEqual(metadata, d)

    def eval_prediction_separate_batch_feed(self, eval_mode):
        num_epochs = 2
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = Net()
        dummy_feed_def = DeactivateModelFeedDefinition()
        model_wrap = ModelWrap(model=model, batch_model_feed_def=dummy_feed_def)

        train_loop = TrainLoop(model_wrap, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, dummy_loss)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort(),
                                                         AbstractCallback('callback_test2')])
        train_loop.fit(num_epochs=num_epochs)

        if eval_mode == 'train':
            y_pred, y_test, metadata = train_loop.predict_on_train_set()
            data_loader = dummy_train_loader
        elif eval_mode == 'val':
            y_pred, y_test, metadata = train_loop.predict_on_validation_set()
            data_loader = dummy_val_loader
        else:
            y_pred, y_test, metadata = train_loop.predict_on_test_set()
            data_loader = dummy_test_loader

        r = []
        for i in range(1, len(data_loader) + 1):
            r += [i] * 64
        r2 = []
        for i in range(1, len(data_loader) + 1):
            r2 += [i + 100] * 64
        self.assertEqual(y_test.tolist(), r)
        self.assertEqual(y_pred.tolist(), r2)

        d = {'bla': []}
        for i in range(1, len(data_loader) + 1):
            d['bla'] += [i + 200] * 64
        self.assertEqual(metadata, d)

    def test_basic_history_tracking(self):
        num_epochs = 2
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = NetUnifiedBatchFeed()
        train_loop = TrainLoop(model, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, dummy_loss)
        train_loop.callbacks_handler.register_callbacks([AbstractCallback('callback_test1'),
                                                         CallbackTracker(), CallbackTrackerShort(),
                                                         AbstractCallback('callback_test2')])
        train_loop.fit(num_epochs=num_epochs)

        self.assertEqual(train_loop.train_history.train_history, {'loss': [1.0, 1.0], 'accumulated_loss': [1.0, 1.0],
                                                                  'val_loss': [1.0, 1.0], 'train_end_test_loss': [1.0]})

        train_loop.insert_metric_result_into_history('test_metric_1', 10.11)
        train_loop.insert_metric_result_into_history('test_metric_2', 40.11)
        train_loop.insert_metric_result_into_history('test_metric_1', 100.11)
        train_loop.insert_metric_result_into_history('test_metric_2', 400.11)

        self.assertEqual(train_loop.train_history.train_history,
                         {'loss': [1.0, 1.0], 'accumulated_loss': [1.0, 1.0], 'val_loss': [1.0, 1.0],
                          'train_end_test_loss': [1.0],
                          'test_metric_1': [10.11, 100.11], 'test_metric_2': [40.11, 400.11]})

    def test_prediction_store_caching(self):
        def eval_predictions(data_loader, y_test, y_pred, metadata, offset=0):
            r = []
            for i in range(1, len(data_loader) + 1):
                r += [i + offset] * 64
            r2 = []
            for i in range(1, len(data_loader) + 1):
                r2 += [i + offset + 100] * 64
            self.assertEqual(y_test.tolist(), r)
            self.assertEqual(y_pred.tolist(), r2)

            d = {'bla': []}
            for i in range(1, len(data_loader) + 1):
                d['bla'] += [i + offset + 200] * 64
            self.assertEqual(metadata, d)

        dummy_optimizer = DummyOptimizer()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = Net()
        dummy_feed_def = DeactivateModelFeedDefinition()
        model_wrap = ModelWrap(model=model, batch_model_feed_def=dummy_feed_def)

        train_loop = TrainLoop(model_wrap, dummy_train_loader, dummy_val_loader, dummy_test_loader,
                               dummy_optimizer, None)

        y_pred, y_test, metadata = train_loop.predict_on_train_set()
        eval_predictions(dummy_train_loader, y_test, y_pred, metadata)

        # even though we changed to test loader we still get the predictions from the train loader as the predictions
        # are not calculated again but are taken from the store.
        train_loop.train_loader = dummy_test_loader
        y_pred_store, y_test_store, metadata_store = train_loop.predict_on_train_set()
        eval_predictions(dummy_train_loader, y_test_store, y_pred_store, metadata_store)

        y_pred_store, y_test_store, metadata_store = train_loop.predict_on_train_set(force_prediction=True)
        eval_predictions(dummy_test_loader, y_test_store, y_pred_store, metadata_store, offset=3+1)

        y_pred_test, y_test_test, metadata = train_loop.predict_on_test_set()
        eval_predictions(dummy_test_loader, y_test_test, y_pred_test, metadata, offset=4+2)

        self.assertEqual(list(train_loop.prediction_store.prediction_store.keys()),
                         ['epoch', 'train_pred', 'test_pred'])
        self.assertEqual(train_loop.prediction_store.prediction_store['epoch'], 0)

        # Test store purge
        train_loop.epoch += 1
        y_pred, y_test, metadata = train_loop.predict_on_validation_set()
        self.assertEqual(train_loop.prediction_store.prediction_store['epoch'], 1)
        self.assertEqual(list(train_loop.prediction_store.prediction_store.keys()), ['epoch', 'val_pred'])

    def test_ddp_env_settings(self):
        dummy_optimizer = DummyOptimizer()
        dummy_loss = DummyLoss()
        dummy_train_loader = list(range(4))
        dummy_val_loader = list(range(3))
        dummy_test_loader = list(range(2))

        model = NetUnifiedBatchFeed()
        train_loop = TrainLoop(
            model, dummy_train_loader, dummy_val_loader, dummy_test_loader,
            dummy_optimizer, dummy_loss,
            gpu_mode='ddp'
        )
        train_loop.fit(num_epochs=1)

        self.assertTrue(train_loop.ddp_training_mode)

        self.assertEqual(os.environ['MASTER_ADDR'], 'localhost')
        self.assertEqual(os.environ['MASTER_PORT'], '8888')
        self.assertEqual(os.environ['MKL_THREADING_LAYER'], 'GNU')

    def test_get_schedulers(self):
        schedulers_list = [
            ReduceLROnPlateauScheduler(), StepLRScheduler(step_size=5), LinearWithWarmupScheduler(5, 100)
        ]
        callbacks_list = [
            EarlyStopping(), ListRegisteredCallbacks()
        ]

        model = NetUnifiedBatchFeed()
        train_loop = TrainLoop(model, None, None, None, Adam(model.parameters()), None)
        train_loop.callbacks_handler.register_callbacks(schedulers_list + callbacks_list)

        tl_filtered_schedulers = train_loop.get_schedulers()
        self.assertEqual(tl_filtered_schedulers, schedulers_list)


class TestMultiLossOptiTrainLoop(unittest.TestCase):
    def test_multi_loss_in_train_loop(self):
        self.run_multi_loss_for_epochs(num_epochs=1)
        self.run_multi_loss_for_epochs(num_epochs=2)
        self.run_multi_loss_for_epochs(num_epochs=3)
        self.run_multi_loss_for_epochs(num_epochs=5)
        self.run_multi_loss_for_epochs(num_epochs=10)

    def run_multi_loss_for_epochs(self, num_epochs):
        train_dataset = TensorDataset(torch.randn(100, 10), torch.randint(low=0, high=10, size=(100,)))
        val_dataset = TensorDataset(torch.randn(30, 10), torch.randint(low=0, high=10, size=(30,)))
        test_dataset = TensorDataset(torch.randn(30, 10), torch.randint(low=0, high=10, size=(30,)))

        train_dataloader = DataLoader(train_dataset, batch_size=20)
        val_dataloader = DataLoader(val_dataset, batch_size=10)
        test_dataloader = DataLoader(test_dataset, batch_size=10)

        loss_1, loss_2 = MultiLossDummy(), MultiLossDummy()
        optimizer_1, optimizer_2 = DummyOptimizer(), DummyOptimizer()

        optimizers = MultiOptimizer([optimizer_1, optimizer_2])
        criterion = DummyLoss()
        model = MultiLossModel(loss_1, loss_2)

        train_loop = TrainLoop(
            model,
            train_dataloader, val_dataloader, test_dataloader,
            optimizers, criterion
        )
        train_loop.fit(num_epochs=num_epochs)

        self.assertEqual(loss_1.backward_ctr, 5 * num_epochs)
        self.assertEqual(loss_1.call_ctr, (5 + 5 + 3) * num_epochs + 3)
        self.assertEqual(loss_1.div_ctr, 5 * num_epochs)
        self.assertEqual(loss_1.retain_graph_ctr, 5 * num_epochs)

        self.assertEqual(loss_2.backward_ctr, 5 * num_epochs)
        self.assertEqual(loss_2.call_ctr, (5 + 5 + 3) * num_epochs + 3)
        self.assertEqual(loss_2.div_ctr, 5 * num_epochs)
        self.assertEqual(loss_2.retain_graph_ctr, 0)

        self.assertEqual(optimizer_1.step_ctr, 5 * num_epochs)
        self.assertEqual(optimizer_1.zero_grad_ctr, 5 * num_epochs)

        self.assertEqual(optimizer_2.step_ctr, 5 * num_epochs)
        self.assertEqual(optimizer_2.zero_grad_ctr, 5 * num_epochs)

    def test_returned_multi_loss_format(self):
        train_dataset = TensorDataset(torch.randn(100, 10), torch.randint(low=0, high=10, size=(100,)))
        val_dataset = TensorDataset(torch.randn(30, 10), torch.randint(low=0, high=10, size=(30,)))
        test_dataset = TensorDataset(torch.randn(30, 10), torch.randint(low=0, high=10, size=(30,)))

        train_dataloader = DataLoader(train_dataset, batch_size=20)
        val_dataloader = DataLoader(val_dataset, batch_size=10)
        test_dataloader = DataLoader(test_dataset, batch_size=10)

        loss_1, loss_2 = MultiLossDummy(), MultiLossDummy()
        optimizer_1, optimizer_2 = DummyOptimizer(), DummyOptimizer()

        optimizers = MultiOptimizer([optimizer_1, optimizer_2])
        criterion = DummyLoss()
        model = MultiLossModel(loss_1, loss_2)

        train_loop = TrainLoop(
            model,
            train_dataloader, val_dataloader, test_dataloader,
            optimizers, criterion
        )
        train_loop.fit(num_epochs=2)
        loss_result = train_loop.evaluate_loss_on_train_set(force_prediction=True)

        self.assertEqual(loss_result, {'loss_1': 32.0, 'loss_2': 32.0})
