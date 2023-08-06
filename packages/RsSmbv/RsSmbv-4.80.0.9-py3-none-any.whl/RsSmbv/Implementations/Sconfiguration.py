from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sconfiguration:
	"""Sconfiguration commands group definition. 19 total commands, 5 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sconfiguration", core, parent)

	def clone(self) -> 'Sconfiguration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sconfiguration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Sconfiguration_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def baseband(self):
		"""baseband commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_baseband'):
			from .Sconfiguration_.Baseband import Baseband
			self._baseband = Baseband(self._core, self._base)
		return self._baseband

	@property
	def diq(self):
		"""diq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_diq'):
			from .Sconfiguration_.Diq import Diq
			self._diq = Diq(self._core, self._base)
		return self._diq

	@property
	def multiInstrument(self):
		"""multiInstrument commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_multiInstrument'):
			from .Sconfiguration_.MultiInstrument import MultiInstrument
			self._multiInstrument = MultiInstrument(self._core, self._base)
		return self._multiInstrument

	@property
	def output(self):
		"""output commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Sconfiguration_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def preset(self) -> None:
		"""SCONfiguration:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SCONfiguration:PRESet')

	def preset_with_opc(self) -> None:
		"""SCONfiguration:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SCONfiguration:PRESet')
