from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("device", core, parent)

	def clone(self) -> 'Device':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Device(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def settings(self):
		"""settings commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_settings'):
			from .Device_.Settings import Settings
			self._settings = Settings(self._core, self._base)
		return self._settings

	def preset(self) -> None:
		"""DEVice:PRESet \n
		Presets all parameters which are not related to the signal path, including the LF generator. \n
		"""
		self._core.io.write(f'DEVice:PRESet')

	def preset_with_opc(self) -> None:
		"""DEVice:PRESet \n
		Presets all parameters which are not related to the signal path, including the LF generator. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DEVice:PRESet')
