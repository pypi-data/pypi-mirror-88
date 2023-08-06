# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Record Transport signals
"""
import logging
import uuid

from .record_signal import RecordSignalMixin

LOGGER = logging.getLogger(__name__)


class RecordTransportMixin(RecordSignalMixin):

    def action_processor(self, result_action):
        result_action = super(RecordTransportMixin, self).action_processor(result_action)
        if result_action is None:
            return
        transports = result_action.get("transports")
        if transports is not None:
            for transport in transports:
                self.record_transport(*transport)
        return result_action

    def record_transport(self, scope, transport, at=None):
        sampler = self.runner.tracing_sampler
        tracing_identifier_prefix = self.runner.settings.tracing_identifier_prefix
        use_signals = self.runner.session.use_signals
        if use_signals is False or tracing_identifier_prefix is None or sampler is None:
            return False
        decision = sampler.should_sample(scope=scope, at=at)
        if not decision:
            return False
        tracing_identifier = transport.get("tracing_identifier")
        if tracing_identifier is None:
            tracing_identifier = "{}.{}".format(tracing_identifier_prefix,
                                                uuid.uuid4())
            transport["tracing_identifier"] = tracing_identifier
        payload = self.runner.interface_manager.call(
            "format_payload", scope, transport)
        if payload is None:
            LOGGER.debug("No tracing payload formatted, skipping")
            return False
        return self.record_signal(
            signal_name="tracing.{}".format(scope),
            payload=payload,
            payload_schema="tracing/{}-2020-04-21".format(scope),
            trigger=decision.attrs["trigger"],
            at=at
        )
