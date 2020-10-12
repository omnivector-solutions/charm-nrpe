#!/usr/bin/python3
"""Nrpe charm."""
import logging

from interface_general_info import GeneralInfo
from interface_monitors import Monitors
from interface_local_monitors import LocalMonitors
from interface_nrpe_external_master import NrpeExternalMaster

import nrpe_helpers
import nrpe_utils

from ops.charm import CharmBase
from ops.main import main


logger = logging.getLogger()


class Nrpe(CharmBase):
    """Nrpe."""

    monitors_relation = nrpe_helpers.MonitorsRelation()
    principal_relation = nrpe_helpers.PrincipalRelation()
    nagios_info = nrpe_helpers.NagiosInfo()

    def __init__(self, *args):
        """Initialize class level attributes and observe events."""
        super().__init__(*args)

        self._general_info = GeneralInfo(self, 'general-info')
        self._local_monitors = LocalMonitors(self, 'local-monitors')
        self._monitors = Monitors(self, 'monitors')
        self._nrpe_external_master = NrpeExternalMaster(self, 'nrpe-external-master')

        self.framework.observe(
            self.on.install,
            self._on_install
        )
        self.framework.observe(
            self.on.config_changed,
            self._on_config_changed
        )
        self.framework.observe(
            self.on.self._general_info.available,
            self._on_check_status_and_configure_event
        )

        self.framework.observe(
            self.on.self._monitors.available,
            self._on_check_status_and_configure_event
        )

        self.framework.observe(
            self.on.self._local_monitors.available,
            self._on_check_status_and_configure_event
        )

        self.framework.observe(
            self.on.self._nrpe_external_master.available,
            self._on_check_status_and_configure_event
        )

    def _on_install(self, event):
        """Install packages and charm files."""
        logger.debug("IN _ON_INSTALL")
        logger.debug(monitors_relation.__dict__)
        logger.debug(principal_relation.__dict__)
        logger.debug(nagios_info.__dict__)
        nrpe_utils.install_packages()
        nrpe_utils.install_charm_files()

    def _on_config_changed(self, event):
        logger.debug("IN _ON_CONFIG_CHANGED")
        logger.debug(monitors_relation.__dict__)
        logger.debug(principal_relation.__dict__)
        logger.debug(nagios_info.__dict__)
        self._check_status_and_configure_event(event)

    def _check_status_and_configure_event(event):
        logger.debug("IN _CHECK_STATUS_AND_CONFIGUR")
        logger.debug(monitors_relation.__dict__)
        logger.debug(principal_relation.__dict__)
        logger.debug(nagios_info.__dict__)
        if not self._check_status_and_configure():
            event.defer()

    def _check_status_and_configure(self):
        if not self._check_status():
            return False
        self._configure()
        return True
        
    def _check_status(self):
        if not (self.monitors_relation and self.principal_relation and
                self.nagios_info):
            return False
        return True

    def _configure(self):
        nrpe_utils.update_nrpe_external_master_relation()
        nrpe_utils.update_monitor_relation()
        nrpe_utils.create_host_export_fragment
        nrpe_utils.render_nrped_files()
        helpers.render_template(
            source="nrpe.tmpl", target="/etc/nagios/nrpe.cfg"
        )
        nrpe_utils.maybe_open_ports
        nrpe_utils.restart_nrpe()
