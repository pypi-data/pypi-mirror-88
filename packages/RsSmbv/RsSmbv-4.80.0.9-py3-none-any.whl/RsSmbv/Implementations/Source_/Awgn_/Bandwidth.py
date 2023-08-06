from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bandwidth", core, parent)

	def clone(self) -> 'Bandwidth':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bandwidth(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def coupling(self):
		"""coupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coupling'):
			from .Bandwidth_.Coupling import Coupling
			self._coupling = Coupling(self._core, self._base)
		return self._coupling

	def get_noise(self) -> float:
		"""[SOURce<HW>]:AWGN:BWIDth:NOISe \n
		Queries the real noise bandwidth. \n
			:return: noise: float Range: 0 to 200E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:BWIDth:NOISe?')
		return Conversions.str_to_float(response)

	def get_ratio(self) -> float:
		"""[SOURce<HW>]:AWGN:BWIDth:RATio \n
		Sets the ratio of minimum real noise bandwidth to system bandwidth, see also 'Signal and noise parameters'. \n
			:return: ratio: float Range: 1 to Max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:BWIDth:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""[SOURce<HW>]:AWGN:BWIDth:RATio \n
		Sets the ratio of minimum real noise bandwidth to system bandwidth, see also 'Signal and noise parameters'. \n
			:param ratio: float Range: 1 to Max
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:BWIDth:RATio {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:AWGN:BWIDth \n
		Sets the system bandwidth. \n
			:return: bwidth: float Range: 1000 to 80E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:BWIDth?')
		return Conversions.str_to_float(response)

	def set_value(self, bwidth: float) -> None:
		"""[SOURce<HW>]:AWGN:BWIDth \n
		Sets the system bandwidth. \n
			:param bwidth: float Range: 1000 to 80E6
		"""
		param = Conversions.decimal_value_to_str(bwidth)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:BWIDth {param}')
