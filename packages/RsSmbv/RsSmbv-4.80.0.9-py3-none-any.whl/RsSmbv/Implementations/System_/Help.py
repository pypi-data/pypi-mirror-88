from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Help:
	"""Help commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("help", core, parent)

	def clone(self) -> 'Help':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Help(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def syntax(self):
		"""syntax commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_syntax'):
			from .Help_.Syntax import Syntax
			self._syntax = Syntax(self._core, self._base)
		return self._syntax

	def export(self) -> None:
		"""SYSTem:HELP:EXPort \n
		Saves the online help as zip archive in the user directory. \n
		"""
		self._core.io.write(f'SYSTem:HELP:EXPort')

	def export_with_opc(self) -> None:
		"""SYSTem:HELP:EXPort \n
		Saves the online help as zip archive in the user directory. \n
		Same as export, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:HELP:EXPort')

	def get_headers(self) -> str:
		"""SYSTem:HELP:HEADers \n
		No command help available \n
			:return: headers: No help available
		"""
		response = self._core.io.query_str('SYSTem:HELP:HEADers?')
		return trim_str_response(response)
