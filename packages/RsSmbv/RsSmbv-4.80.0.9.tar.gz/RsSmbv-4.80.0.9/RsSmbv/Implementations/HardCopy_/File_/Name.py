from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 12 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("name", core, parent)

	def clone(self) -> 'Name':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Name(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def auto(self):
		"""auto commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_auto'):
			from .Name_.Auto import Auto
			self._auto = Auto(self._core, self._base)
		return self._auto

	def get_value(self) -> str:
		"""HCOPy:FILE:[NAME] \n
		Determines the file name and path to save the hard copy, provided automatic naming is disabled. Note: If you have enabled
		automatic naming, the instrument automatically generates the file name and directory, see 'Automatic Naming'. \n
			:return: name: string
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME?')
		return trim_str_response(response)

	def set_value(self, name: str) -> None:
		"""HCOPy:FILE:[NAME] \n
		Determines the file name and path to save the hard copy, provided automatic naming is disabled. Note: If you have enabled
		automatic naming, the instrument automatically generates the file name and directory, see 'Automatic Naming'. \n
			:param name: string
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'HCOPy:FILE:NAME {param}')
