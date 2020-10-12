#!/usr/bin/python3
"""Monitors interface."""
import logging

from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
    StoredState,
)

logger = logging.getLogger()


class MonitorAvailableEvent(EventBase):
    """RATS"""


class MonitorEvents(ObjectEvents):
    """LocalMonitorEvents."""

    available = EventSource(MonitorAvailableEvent)


class Monitors(Object):
    """Monitors interface."""

    on = MonitorEvents()

    def __init__(self, charm, relation_name):
        """Observe relation events."""
        super().__init__(charm, relation_name)
        self._charm = charm
        self._relation_name = relation_name

        self.framework.observe(
            self._charm.on[self._relation_name].relation_joined,
            self._on_relation_joined
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def _on_relation_joined(self, event):
        self.on.available.emit()

    def _on_relation_changed(self, event):
        self.on.available.emit()

    def _on_relation_broken(self, event):
        self.on.available.emit()
