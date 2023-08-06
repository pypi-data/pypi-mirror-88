from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Comid:
	"""Comid commands group definition. 12 total commands, 1 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("comid", core, parent)

	def clone(self) -> 'Comid':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Comid(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def code(self):
		"""code commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_code'):
			from .Comid_.Code import Code
			self._code = Code(self._core, self._base)
		return self._code

	def get_dash(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DASH \n
		Sets the length of a Morse code dash. \n
			:return: dash: float Range: 0.05 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:DASH?')
		return Conversions.str_to_float(response)

	def set_dash(self, dash: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DASH \n
		Sets the length of a Morse code dash. \n
			:param dash: float Range: 0.05 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(dash)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:DASH {param}')

	def get_depth(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DEPTh \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DEPTh \n
		Sets the AM modulation depth of the COM/ID signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:DEPTh {param}')

	def get_dot(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DOT \n
		Sets the length of a Morse code dot. \n
			:return: dot: float Range: 0.05 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:DOT?')
		return Conversions.str_to_float(response)

	def set_dot(self, dot: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:DOT \n
		Sets the length of a Morse code dot. \n
			:param dot: float Range: 0.05 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(dot)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:DOT {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:FREQuency \n
		Sets the frequency of the COM/ID signal. \n
			:return: frequency: float Range: 0.1 to 20E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:FREQuency \n
		Sets the frequency of the COM/ID signal. \n
			:param frequency: float Range: 0.1 to 20E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:FREQuency {param}')

	def get_letter(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:LETTer \n
		Sets the length of a Morse code letter space. \n
			:return: letter: float Range: 0.05 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:LETTer?')
		return Conversions.str_to_float(response)

	def set_letter(self, letter: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:LETTer \n
		Sets the length of a Morse code letter space. \n
			:param letter: float Range: 0.05 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(letter)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:LETTer {param}')

	def get_period(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:PERiod \n
		Sets the period of the COM/ID signal. \n
			:return: period: float Range: 0 to 120, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:PERiod \n
		Sets the period of the COM/ID signal. \n
			:param period: float Range: 0 to 120, Unit: s
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:PERiod {param}')

	def get_repeat(self) -> int:
		"""[SOURce<HW>]:[BB]:VOR:COMid:REPeat \n
		No command help available \n
			:return: repeat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:REPeat?')
		return Conversions.str_to_int(response)

	def set_repeat(self, repeat: int) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:REPeat \n
		No command help available \n
			:param repeat: No help available
		"""
		param = Conversions.decimal_value_to_str(repeat)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:REPeat {param}')

	def get_symbol(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:COMid:SYMBol \n
		Sets the length of the Morse code symbol space. \n
			:return: symbol: float Range: 0.05 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:SYMBol?')
		return Conversions.str_to_float(response)

	def set_symbol(self, symbol: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:SYMBol \n
		Sets the length of the Morse code symbol space. \n
			:param symbol: float Range: 0.05 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(symbol)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:SYMBol {param}')

	# noinspection PyTypeChecker
	def get_tschema(self) -> enums.AvionicComIdTimeSchem:
		"""[SOURce<HW>]:[BB]:VOR:COMid:TSCHema \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:return: tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:TSCHema?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicComIdTimeSchem)

	def set_tschema(self, tschema: enums.AvionicComIdTimeSchem) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:TSCHema \n
		Sets the time schema of the Morse code for the COM/ID signal. \n
			:param tschema: STD| USER STD Activates the standard time schema of the Morse code. The set dot length determines the dash length, which is 3 times the dot length. USER Activates the user-defined time schema of the Morse code. Dot and dash length, as well as symbol and letter space can be set separately.
		"""
		param = Conversions.enum_scalar_to_str(tschema, enums.AvionicComIdTimeSchem)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:TSCHema {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:[BB]:VOR:COMid:[STATe] \n
		Enables/disables the COM/ID signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:COMid:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:[BB]:VOR:COMid:[STATe] \n
		Enables/disables the COM/ID signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:COMid:STATe {param}')
