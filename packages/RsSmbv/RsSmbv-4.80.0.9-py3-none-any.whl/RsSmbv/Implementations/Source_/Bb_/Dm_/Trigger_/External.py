from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("external", core, parent)

	def clone(self) -> 'External':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = External(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def synchronize(self):
		"""synchronize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_synchronize'):
			from .External_.Synchronize import Synchronize
			self._synchronize = Synchronize(self._core, self._base)
		return self._synchronize

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:DELay \n
		Specifies the trigger delay in symbols. Maximum trigger delay and trigger inhibit values depend on the installed options.
		See 'Specifying delay and inhibit values'. \n
			:return: delay: float Range: 0 to depends on the symbol rate, Unit: symbol
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:DELay \n
		Specifies the trigger delay in symbols. Maximum trigger delay and trigger inhibit values depend on the installed options.
		See 'Specifying delay and inhibit values'. \n
			:param delay: float Range: 0 to depends on the symbol rate, Unit: symbol
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:DELay {param}')

	def get_inhibit(self) -> int:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols, by which a restart is inhibited. Maximum trigger delay and trigger inhibit values depend
		on the installed options. See 'Specifying delay and inhibit values'. \n
			:return: inhibit: integer Range: 0 to 21.47 * (symbol rate) , Unit: symbol
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols, by which a restart is inhibited. Maximum trigger delay and trigger inhibit values depend
		on the installed options. See 'Specifying delay and inhibit values'. \n
			:param inhibit: integer Range: 0 to 21.47 * (symbol rate) , Unit: symbol
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:INHibit {param}')

	def get_rdelay(self) -> float:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:RDELay \n
		Queries the time (in seconds) an external trigger event is delayed for. \n
			:return: res_time_delay_sec: float Range: 0 to 688
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:RDELay?')
		return Conversions.str_to_float(response)

	def get_tdelay(self) -> float:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:TDELay \n
		Specifies the trigger delay for external triggering. The value affects all external trigger signals. Maximum trigger
		delay and trigger inhibit values depend on the installed options. See 'Specifying delay and inhibit values'. \n
			:return: ext_time_delay: float Range: 0 to 7929.170398682, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:TDELay?')
		return Conversions.str_to_float(response)

	def set_tdelay(self, ext_time_delay: float) -> None:
		"""[SOURce<HW>]:BB:DM:TRIGger:[EXTernal]:TDELay \n
		Specifies the trigger delay for external triggering. The value affects all external trigger signals. Maximum trigger
		delay and trigger inhibit values depend on the installed options. See 'Specifying delay and inhibit values'. \n
			:param ext_time_delay: float Range: 0 to 7929.170398682, Unit: s
		"""
		param = Conversions.decimal_value_to_str(ext_time_delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:TRIGger:EXTernal:TDELay {param}')
