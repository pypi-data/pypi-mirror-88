from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Smodulation:
	"""Smodulation commands group definition. 5 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("smodulation", core, parent)

	def clone(self) -> 'Smodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Smodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_clock'):
			from .Smodulation_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def rcvState(self):
		"""rcvState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rcvState'):
			from .Smodulation_.RcvState import RcvState
			self._rcvState = RcvState(self._core, self._base)
		return self._rcvState

	@property
	def throughput(self):
		"""throughput commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_throughput'):
			from .Smodulation_.Throughput import Throughput
			self._throughput = Throughput(self._core, self._base)
		return self._throughput

	# noinspection PyTypeChecker
	def get_border(self) -> enums.BitOrder:
		"""[SOURce<HW>]:BB:DM:SMODulation:BORDer \n
		No command help available \n
			:return: bit_order: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:BORDer?')
		return Conversions.str_to_scalar_enum(response, enums.BitOrder)

	def set_border(self, bit_order: enums.BitOrder) -> None:
		"""[SOURce<HW>]:BB:DM:SMODulation:BORDer \n
		No command help available \n
			:param bit_order: No help available
		"""
		param = Conversions.enum_scalar_to_str(bit_order, enums.BitOrder)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SMODulation:BORDer {param}')

	def get_cdtdeviation(self) -> float:
		"""[SOURce<HW>]:BB:DM:SMODulation:CDTDeviation \n
		No command help available \n
			:return: deviation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:CDTDeviation?')
		return Conversions.str_to_float(response)
