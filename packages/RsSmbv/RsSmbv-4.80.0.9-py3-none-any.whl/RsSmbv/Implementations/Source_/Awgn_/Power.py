from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 7 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def noise(self):
		"""noise commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_noise'):
			from .Power_.Noise import Noise
			self._noise = Noise(self._core, self._base)
		return self._noise

	@property
	def sum(self):
		"""sum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sum'):
			from .Power_.Sum import Sum
			self._sum = Sum(self._core, self._base)
		return self._sum

	def get_carrier(self) -> float:
		"""[SOURce<HW>]:AWGN:POWer:CARRier \n
		Sets the carrier power. \n
			:return: carrier: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:POWer:CARRier?')
		return Conversions.str_to_float(response)

	def set_carrier(self, carrier: float) -> None:
		"""[SOURce<HW>]:AWGN:POWer:CARRier \n
		Sets the carrier power. \n
			:param carrier: float
		"""
		param = Conversions.decimal_value_to_str(carrier)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:POWer:CARRier {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.NoisAwgnPowMode:
		"""[SOURce<HW>]:AWGN:POWer:MODE \n
		Selects the mode for setting the noise level. \n
			:return: mode: CN| SN | EN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:POWer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnPowMode)

	def set_mode(self, mode: enums.NoisAwgnPowMode) -> None:
		"""[SOURce<HW>]:AWGN:POWer:MODE \n
		Selects the mode for setting the noise level. \n
			:param mode: CN| SN | EN
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.NoisAwgnPowMode)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:POWer:MODE {param}')

	# noinspection PyTypeChecker
	def get_rmode(self) -> enums.NoisAwgnPowRefMode:
		"""[SOURce<HW>]:AWGN:POWer:RMODe \n
		Determines whether the carrier or the noise level is kept constant when the C/N value or Eb/N0 value is changed. \n
			:return: rm_ode: CARRier| NOISe
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:POWer:RMODe?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnPowRefMode)

	def set_rmode(self, rm_ode: enums.NoisAwgnPowRefMode) -> None:
		"""[SOURce<HW>]:AWGN:POWer:RMODe \n
		Determines whether the carrier or the noise level is kept constant when the C/N value or Eb/N0 value is changed. \n
			:param rm_ode: CARRier| NOISe
		"""
		param = Conversions.enum_scalar_to_str(rm_ode, enums.NoisAwgnPowRefMode)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:POWer:RMODe {param}')
