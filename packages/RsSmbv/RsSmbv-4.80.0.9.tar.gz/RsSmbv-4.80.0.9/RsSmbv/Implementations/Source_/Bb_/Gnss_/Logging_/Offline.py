from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offline:
	"""Offline commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offline", core, parent)

	def clone(self) -> 'Offline':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Offline(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def generate(self):
		"""generate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_generate'):
			from .Offline_.Generate import Generate
			self._generate = Generate(self._core, self._base)
		return self._generate

	def abort(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:ABORt \n
		Logging files are created and saved. Files with the same name are overwritten. To stop the generation, send method RsSmbv.
		Source.Bb.Gnss.Logging.Offline.abort. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:ABORt')

	def abort_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:ABORt \n
		Logging files are created and saved. Files with the same name are overwritten. To stop the generation, send method RsSmbv.
		Source.Bb.Gnss.Logging.Offline.abort. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:ABORt')

	def get_duration(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:DURation \n
		Sets the logging duration. \n
			:return: duration: float Range: 0 to 864000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, duration: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:DURation \n
		Sets the logging duration. \n
			:param duration: float Range: 0 to 864000
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:DURation {param}')

	def get_progress(self) -> int:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:PROGress \n
		Querries the progress of the offline data logging generation. \n
			:return: progress: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:PROGress?')
		return Conversions.str_to_int(response)

	def get_toffset(self) -> float:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:TOFFset \n
		Delays the logging start. \n
			:return: time_offset: float Range: 0 to 864000, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:TOFFset?')
		return Conversions.str_to_float(response)

	def set_toffset(self, time_offset: float) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:OFFLine:TOFFset \n
		Delays the logging start. \n
			:param time_offset: float Range: 0 to 864000, Unit: s
		"""
		param = Conversions.decimal_value_to_str(time_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:OFFLine:TOFFset {param}')
