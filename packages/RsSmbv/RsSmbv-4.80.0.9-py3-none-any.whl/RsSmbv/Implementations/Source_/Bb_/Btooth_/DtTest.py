from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DtTest:
	"""DtTest commands group definition. 17 total commands, 3 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtTest", core, parent)

	def clone(self) -> 'DtTest':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DtTest(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def stDefault(self):
		"""stDefault commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stDefault'):
			from .DtTest_.StDefault import StDefault
			self._stDefault = StDefault(self._core, self._base)
		return self._stDefault

	@property
	def table(self):
		"""table commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_table'):
			from .DtTest_.Table import Table
			self._table = Table(self._core, self._base)
		return self._table

	@property
	def tpConfiguration(self):
		"""tpConfiguration commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tpConfiguration'):
			from .DtTest_.TpConfiguration import TpConfiguration
			self._tpConfiguration = TpConfiguration(self._core, self._base)
		return self._tpConfiguration

	def get_dtt_state(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:DTTState \n
		Activates the 'Dirty Transmitter Test'. For EDR packets, the parameter sets apply for 20 packets each. \n
			:return: dtt_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:DTTState?')
		return Conversions.str_to_bool(response)

	def set_dtt_state(self, dtt_state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:DTTState \n
		Activates the 'Dirty Transmitter Test'. For EDR packets, the parameter sets apply for 20 packets each. \n
			:param dtt_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(dtt_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:DTTState {param}')

	def get_fd_deviation(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:FDDeviation \n
		Sets a frequency drift rate. A sine wave is used to drift the modulated Bluetooth signal around center frequency +
		carrier frequency offset. The maximum deviation reached during the drift equals the set frequency drift deviation. \n
			:return: fd_deviation: integer Range: -100 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:FDDeviation?')
		return Conversions.str_to_int(response)

	def set_fd_deviation(self, fd_deviation: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:FDDeviation \n
		Sets a frequency drift rate. A sine wave is used to drift the modulated Bluetooth signal around center frequency +
		carrier frequency offset. The maximum deviation reached during the drift equals the set frequency drift deviation. \n
			:param fd_deviation: integer Range: -100 to 100
		"""
		param = Conversions.decimal_value_to_str(fd_deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:FDDeviation {param}')

	def get_fd_rate(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:FDRate \n
		Sets a frequency drift rate. A sine wave is used to drift the modulated Bluetooth signal around center frequency +
		carrier frequency offset with the set frequency drift rate. \n
			:return: fd_rate: 0.3 KHz| 0.5 KHz| 1.6 KHz| 10 KHz Range: depends on packet type to depends on packet type
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:FDRate?')
		return Conversions.str_to_float(response)

	def set_fd_rate(self, fd_rate: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:FDRate \n
		Sets a frequency drift rate. A sine wave is used to drift the modulated Bluetooth signal around center frequency +
		carrier frequency offset with the set frequency drift rate. \n
			:param fd_rate: 0.3 KHz| 0.5 KHz| 1.6 KHz| 10 KHz Range: depends on packet type to depends on packet type
		"""
		param = Conversions.decimal_value_to_str(fd_rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:FDRate {param}')

	# noinspection PyTypeChecker
	def get_mi_mode(self) -> enums.BtoModIdxMode:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:MIMode \n
		Determines standard or stable mode for the modulation index of dirty transmitter according to the Bluetooth core
		specification. \n
			:return: mi_mode: STANdard| STABle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:MIMode?')
		return Conversions.str_to_scalar_enum(response, enums.BtoModIdxMode)

	def set_mi_mode(self, mi_mode: enums.BtoModIdxMode) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:MIMode \n
		Determines standard or stable mode for the modulation index of dirty transmitter according to the Bluetooth core
		specification. \n
			:param mi_mode: STANdard| STABle
		"""
		param = Conversions.enum_scalar_to_str(mi_mode, enums.BtoModIdxMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:MIMode {param}')

	# noinspection PyTypeChecker
	def get_nppset(self) -> enums.BtoNumOfPackPerSet:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:NPPSet \n
		Specifies the number of packets to be transmitted per dirty transmitter set. \n
			:return: num_pack: NP50| NP2| NP1 50, 2 packets or 1 packet per set
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:NPPSet?')
		return Conversions.str_to_scalar_enum(response, enums.BtoNumOfPackPerSet)

	def set_nppset(self, num_pack: enums.BtoNumOfPackPerSet) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:NPPSet \n
		Specifies the number of packets to be transmitted per dirty transmitter set. \n
			:param num_pack: NP50| NP2| NP1 50, 2 packets or 1 packet per set
		"""
		param = Conversions.enum_scalar_to_str(num_pack, enums.BtoNumOfPackPerSet)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:NPPSet {param}')

	def get_sphase(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:SPHase \n
		The command enters a start phase. The start phase of the sine wave used to drift the modulated Bluetooth signal around
		center frequency + carrier frequency offset is set here. \n
			:return: sphase: integer Range: 0 to 359, Unit: degree
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DTTest:SPHase?')
		return Conversions.str_to_int(response)

	def set_sphase(self, sphase: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:SPHase \n
		The command enters a start phase. The start phase of the sine wave used to drift the modulated Bluetooth signal around
		center frequency + carrier frequency offset is set here. \n
			:param sphase: integer Range: 0 to 359, Unit: degree
		"""
		param = Conversions.decimal_value_to_str(sphase)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:SPHase {param}')
