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
	def sync(self):
		"""sync commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sync'):
			from .External_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	def get_rdelay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:EXTernal:RDELay \n
		Queries the time (in seconds) of an external trigger event is delayed for. \n
			:return: res_ext_delay_sec: float Range: 0 to 688
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:RDELay?')
		return Conversions.str_to_float(response)

	def get_tdelay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:EXTernal:TDELay \n
		Specifies the trigger delay for external triggering. The value affects all external trigger signals. \n
			:return: trig_ext_time_del: float Range: 0 to 688
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:TDELay?')
		return Conversions.str_to_float(response)

	def set_tdelay(self, trig_ext_time_del: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:EXTernal:TDELay \n
		Specifies the trigger delay for external triggering. The value affects all external trigger signals. \n
			:param trig_ext_time_del: float Range: 0 to 688
		"""
		param = Conversions.decimal_value_to_str(trig_ext_time_del)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:TDELay {param}')

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:[EXTernal]:DELay \n
		Sets the trigger delay. \n
			:return: delay: float Range: 0 to 2147483647
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:[EXTernal]:DELay \n
		Sets the trigger delay. \n
			:param delay: float Range: 0 to 2147483647
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:DELay {param}')

	def get_inhibit(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols by which a restart is inhibited. \n
			:return: inhibit: integer Range: 0 to 21.47*symbRate
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:INHibit?')
		return Conversions.str_to_int(response)

	def set_inhibit(self, inhibit: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:TRIGger:[EXTernal]:INHibit \n
		Specifies the number of symbols by which a restart is inhibited. \n
			:param inhibit: integer Range: 0 to 21.47*symbRate
		"""
		param = Conversions.decimal_value_to_str(inhibit)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:TRIGger:EXTernal:INHibit {param}')
