from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Serror:
	"""Serror commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("serror", core, parent)

	def clone(self) -> 'Serror':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Serror(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def set(self):
		"""set commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_set'):
			from .Serror_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set

	def set_unset(self, path: int) -> None:
		"""TEST:SERRor:UNSet \n
		No command help available \n
			:param path: No help available
		"""
		param = Conversions.decimal_value_to_str(path)
		self._core.io.write(f'TEST:SERRor:UNSet {param}')
