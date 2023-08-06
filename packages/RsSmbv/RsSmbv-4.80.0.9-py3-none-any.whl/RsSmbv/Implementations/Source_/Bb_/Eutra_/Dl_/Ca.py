from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ca:
	"""Ca commands group definition. 16 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ca", core, parent)

	def clone(self) -> 'Ca':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ca(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cell(self):
		"""cell commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Ca_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:CA:STATe \n
		Enables/disables the generation of several component carriers. \n
			:return: ca_global_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:CA:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, ca_global_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CA:STATe \n
		Enables/disables the generation of several component carriers. \n
			:param ca_global_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(ca_global_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CA:STATe {param}')
