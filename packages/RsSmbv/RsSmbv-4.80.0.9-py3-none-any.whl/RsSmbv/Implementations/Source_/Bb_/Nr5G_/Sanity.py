from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sanity:
	"""Sanity commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sanity", core, parent)

	def clone(self) -> 'Sanity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sanity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def inspection(self):
		"""inspection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inspection'):
			from .Sanity_.Inspection import Inspection
			self._inspection = Inspection(self._core, self._base)
		return self._inspection

	def get_state(self) -> bool:
		"""[SOURce]:BB:NR5G:SANity:STATe \n
		No command help available \n
			:return: sanity_state: No help available
		"""
		response = self._core.io.query_str('SOURce:BB:NR5G:SANity:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sanity_state: bool) -> None:
		"""[SOURce]:BB:NR5G:SANity:STATe \n
		No command help available \n
			:param sanity_state: No help available
		"""
		param = Conversions.bool_to_str(sanity_state)
		self._core.io.write(f'SOURce:BB:NR5G:SANity:STATe {param}')
