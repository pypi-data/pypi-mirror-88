from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Node:
	"""Node commands group definition. 110 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("node", core, parent)

	def clone(self) -> 'Node':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Node(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def carMapping(self):
		"""carMapping commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_carMapping'):
			from .Node_.CarMapping import CarMapping
			self._carMapping = CarMapping(self._core, self._base)
		return self._carMapping

	@property
	def cell(self):
		"""cell commands group. 23 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Node_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def rfPhase(self):
		"""rfPhase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfPhase'):
			from .Node_.RfPhase import RfPhase
			self._rfPhase = RfPhase(self._core, self._base)
		return self._rfPhase

	def get_ncarrier(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:NCARrier \n
		Sets the number of simulated carriers. When used in a previously configured system, reconfigures the number of simulated
		carriers. \n
			:return: num_carrier: integer Range: 1 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:NCARrier?')
		return Conversions.str_to_int(response)

	def set_ncarrier(self, num_carrier: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:NCARrier \n
		Sets the number of simulated carriers. When used in a previously configured system, reconfigures the number of simulated
		carriers. \n
			:param num_carrier: integer Range: 1 to 16
		"""
		param = Conversions.decimal_value_to_str(num_carrier)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:NCARrier {param}')
