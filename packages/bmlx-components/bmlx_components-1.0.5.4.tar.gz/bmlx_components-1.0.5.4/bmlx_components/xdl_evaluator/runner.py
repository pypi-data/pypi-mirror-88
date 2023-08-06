import xdl
import tensorflow as tf
import random
import numpy as np
import logging
import functools
import datetime

from typing import Dict, Text, List
from bmlx.flow import Artifact
from bmlx.utils import var_utils, import_utils, io_utils
from xdl.python.framework.session import Hook
from xdl.python.training.training_utils import get_global_step
from bmlx_components.xdl_base.runner import XdlRunner
from bmlx_components.xdl_base.model import ProcessResult


# 同时支持 xdl eval 和 xdl eval slots
class XdlEvalRunner(XdlRunner):
    def run(self, reader: xdl.DataReader, eval_slots=[]):
        batch = reader.read()

        log_str = "gstep: [{0}], timestamp: [{1}]"
        global_step = get_global_step().value
        timestamp, _ = xdl.split(
            batch["_timestamp"],
            np.array(
                [
                    1,
                    self._parameters["reader"]["batch_size"].as_number(1024)
                    - 1,
                ]
            ),
            0,
            2,
        )
        log_tensors = [global_step, timestamp]

        train_ops = []
        hooks = []
        metric_tensors = []

        logging.info("xdl begin with phase %s" % self._parameters["phases"])

        # eval phase = 1
        if not eval_slots:  # 正常eval
            with xdl.model_scope("phase0"):
                ret = self._model.process(batch=batch, phase=0,)
        else:  # eval slots
            ret = ProcessResult()
            for slot in eval_slots:
                with xdl.model_scope("slot" + str(slot)):
                    partial_ret = self._model.process(
                        batch=batch, phase=0, eval_slot=slot
                    )
                    for k, v in partial_ret.tensor_map.items():
                        partial_ret["slot_{}_{}".format(slot, k)] = v
                        del partial_ret.tensor_map[k]
                    ret.append(partial_ret)

        for name, tensor in ret.tensor_map.items():
            metric_tensors.append(("phase%s/%s" % (0, name), tensor))
            log_str += ", p%d_%s:{%d}" % (0, name, len(log_tensors))
            log_tensors.append(tensor)
            train_ops.append(tensor)

        if ret.additional_hooks:
            hooks.extend(ret.additional_hooks)

        # add log hooks
        hooks.append(
            xdl.LoggerHook(
                log_tensors[:],
                log_str,
                interval=self._parameters["log_interval"].as_number(),
            )
        )

        ts_tensor = batch["_timestamp"]
        if not self._is_local:
            hooks.extend(self.gen_worker_finish_hook())

        if self._is_training:
            hooks.extend(self.gen_hash_slots_update_hook())
            hooks.extend(self.gen_checkpoint_hook(ts_tensor))
            hooks.extend(self.gen_vars_sync_hook(ts_tensor))
            hooks.extend(self.gen_notify_barrier_slave_hook())
            hooks.extend(self.gen_global_step_filter_hook())
            hooks.extend(self.gen_timestamp_filter_hook(ts_tensor))
            hooks.extend(self.gen_hash_feature_decay_hook(ts_tensor))
            hooks.extend(self.gen_hash_feature_score_filter_hook(ts_tensor))

        if self._stage in ("predict" "train", "eval"):
            hooks.extend(self.gen_trace_hook())

        hooks.extend(
            self.gen_metrics_hook(ts_tensor, additional_metrics=metric_tensors,)
        )

        timeline_hook = self.timeline_hook()
        if timeline_hook:
            hooks.append(timeline_hook)

        sess = xdl.TrainSession(hooks=hooks)
        while not sess.should_stop():
            if timeline_hook:
                run_option = timeline_hook.run_option()
                run_option.timeout_second = self._parameters[
                    "timeout"
                ].as_number()
                sess.run(
                    train_ops,
                    run_option=run_option,
                    run_statistic=timeline_hook.run_statistic(),
                )
            else:
                run_option = xdl.RunOption()
                run_option.timeout_second = self._parameters[
                    "timeout"
                ].as_number()
                sess.run(train_ops, run_option=run_option)
