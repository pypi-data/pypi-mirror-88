from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 11 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	def clone(self) -> 'Auto':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Auto(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def directory(self):
		"""directory commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_directory'):
			from .Auto_.Directory import Directory
			self._directory = Directory(self._core, self._base)
		return self._directory

	@property
	def file(self):
		"""file commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_file'):
			from .Auto_.File import File
			self._file = File(self._core, self._base)
		return self._file

	def get_state(self) -> bool:
		"""HCOPy:FILE:[NAME]:AUTO:STATe \n
		Activates automatic naming of the hard copy files. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:STATe \n
		Activates automatic naming of the hard copy files. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'HCOPy:FILE:NAME:AUTO:STATe {param}')

	def get_value(self) -> str:
		"""HCOPy:FILE:[NAME]:AUTO \n
		Queries path and file name of the hardcopy file, if you have enabled Automatic Naming. \n
			:return: auto: string
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO?')
		return trim_str_response(response)
