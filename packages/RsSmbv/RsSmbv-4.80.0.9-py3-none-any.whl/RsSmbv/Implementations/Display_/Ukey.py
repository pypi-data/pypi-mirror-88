from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ukey:
	"""Ukey commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ukey", core, parent)

	def clone(self) -> 'Ukey':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ukey(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def add(self):
		"""add commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_add'):
			from .Ukey_.Add import Add
			self._add = Add(self._core, self._base)
		return self._add

	def set_name(self, name: str) -> None:
		"""DISPlay:UKEY:NAME \n
		No command help available \n
			:param name: No help available
		"""
		param = Conversions.value_to_quoted_str(name)
		self._core.io.write(f'DISPlay:UKEY:NAME {param}')

	def set_scpi(self, scpi: str) -> None:
		"""DISPlay:UKEY:SCPI \n
		No command help available \n
			:param scpi: No help available
		"""
		param = Conversions.value_to_quoted_str(scpi)
		self._core.io.write(f'DISPlay:UKEY:SCPI {param}')
