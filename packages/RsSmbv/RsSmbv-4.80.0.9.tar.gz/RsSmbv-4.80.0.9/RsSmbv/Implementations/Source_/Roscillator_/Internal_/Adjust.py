from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adjust:
	"""Adjust commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adjust", core, parent)

	def get_value(self) -> int:
		"""[SOURce]:ROSCillator:[INTernal]:ADJust:VALue \n
		Specifies the frequency correction value (adjustment value) . \n
			:return: value: integer
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:INTernal:ADJust:VALue?')
		return Conversions.str_to_int(response)

	def set_value(self, value: int) -> None:
		"""[SOURce]:ROSCillator:[INTernal]:ADJust:VALue \n
		Specifies the frequency correction value (adjustment value) . \n
			:param value: integer
		"""
		param = Conversions.decimal_value_to_str(value)
		self._core.io.write(f'SOURce:ROSCillator:INTernal:ADJust:VALue {param}')

	def get_state(self) -> bool:
		"""[SOURce]:ROSCillator:[INTernal]:ADJust:[STATe] \n
		Determines whether the calibrated (off) or a user-defined (on) adjustment value is used for fine adjustment of the
		frequency. \n
			:return: state: 0| 1| OFF| ON 0 Fine adjustment with the calibrated frequency value 1 User-defined adjustment value. The instrument is no longer in the calibrated state. The calibration value is, however, not changed. The instrument resumes the calibrated state if you send SOURce:ROSCillator:INTernal:ADJust:STATe 0.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:INTernal:ADJust:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce]:ROSCillator:[INTernal]:ADJust:[STATe] \n
		Determines whether the calibrated (off) or a user-defined (on) adjustment value is used for fine adjustment of the
		frequency. \n
			:param state: 0| 1| OFF| ON 0 Fine adjustment with the calibrated frequency value 1 User-defined adjustment value. The instrument is no longer in the calibrated state. The calibration value is, however, not changed. The instrument resumes the calibrated state if you send SOURce:ROSCillator:INTernal:ADJust:STATe 0.
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:ROSCillator:INTernal:ADJust:STATe {param}')
