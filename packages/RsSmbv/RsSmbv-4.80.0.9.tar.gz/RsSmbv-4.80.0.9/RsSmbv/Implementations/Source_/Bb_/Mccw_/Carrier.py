from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Carrier:
	"""Carrier commands group definition. 8 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carrier", core, parent)

	def clone(self) -> 'Carrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Carrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def listPy(self):
		"""listPy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .Carrier_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:MCCW:CARRier:COUNt \n
		Sets the number of carriers in the multi carrier CW signal. \n
			:return: count: integer Range: 1 to 160001
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:CARRier:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:COUNt \n
		Sets the number of carriers in the multi carrier CW signal. \n
			:param count: integer Range: 1 to 160001
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CARRier:COUNt {param}')

	# noinspection PyTypeChecker
	class PhaseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Carrier_Index: int: integer Range: 0 to lastCarrier
			- Phase: float: float Range: 0 to 359.99, Unit: DEG"""
		__meta_args_list = [
			ArgStruct.scalar_int('Carrier_Index'),
			ArgStruct.scalar_float('Phase')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Carrier_Index: int = None
			self.Phase: float = None

	def get_phase(self) -> PhaseStruct:
		"""[SOURce<HW>]:BB:MCCW:CARRier:PHASe \n
		For disabled optimization of the crest factor, sets the start phase of the selected carrier. \n
			:return: structure: for return value, see the help for PhaseStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:MCCW:CARRier:PHASe?', self.__class__.PhaseStruct())

	def set_phase(self, value: PhaseStruct) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:PHASe \n
		For disabled optimization of the crest factor, sets the start phase of the selected carrier. \n
			:param value: see the help for PhaseStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:MCCW:CARRier:PHASe', value)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Carrier_Index: int: integer Range: 0 to lastCarrier
			- Power: float: float Range: -80 to 0"""
		__meta_args_list = [
			ArgStruct.scalar_int('Carrier_Index'),
			ArgStruct.scalar_float('Power')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Carrier_Index: int = None
			self.Power: float = None

	def get_power(self) -> PowerStruct:
		"""[SOURce<HW>]:BB:MCCW:CARRier:POWer \n
		Sets the power of the selected carrier. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:MCCW:CARRier:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:POWer \n
		Sets the power of the selected carrier. \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:MCCW:CARRier:POWer', value)

	def get_spacing(self) -> float:
		"""[SOURce<HW>]:BB:MCCW:CARRier:SPACing \n
		Sets the carrier spacing. \n
			:return: spacing: float Value range depends on the available bandwidth and the number of carriers, see 'Cross-reference between total bandwidth, carrier spacing, and number of carriers'. Range: 0 to depends on the installed options, e.g. 120E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:CARRier:SPACing?')
		return Conversions.str_to_float(response)

	def set_spacing(self, spacing: float) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:SPACing \n
		Sets the carrier spacing. \n
			:param spacing: float Value range depends on the available bandwidth and the number of carriers, see 'Cross-reference between total bandwidth, carrier spacing, and number of carriers'. Range: 0 to depends on the installed options, e.g. 120E6
		"""
		param = Conversions.decimal_value_to_str(spacing)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CARRier:SPACing {param}')

	# noinspection PyTypeChecker
	class StateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Carrier_Index: int: integer Range: 0 to lastCarrier
			- State: bool: 0| 1| OFF| ON"""
		__meta_args_list = [
			ArgStruct.scalar_int('Carrier_Index'),
			ArgStruct.scalar_bool('State')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Carrier_Index: int = None
			self.State: bool = None

	def get_state(self) -> StateStruct:
		"""[SOURce<HW>]:BB:MCCW:CARRier:STATe \n
		Switches the selected carrier on or off. \n
			:return: structure: for return value, see the help for StateStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:MCCW:CARRier:STATe?', self.__class__.StateStruct())

	def set_state(self, value: StateStruct) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:STATe \n
		Switches the selected carrier on or off. \n
			:param value: see the help for StateStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:MCCW:CARRier:STATe', value)
