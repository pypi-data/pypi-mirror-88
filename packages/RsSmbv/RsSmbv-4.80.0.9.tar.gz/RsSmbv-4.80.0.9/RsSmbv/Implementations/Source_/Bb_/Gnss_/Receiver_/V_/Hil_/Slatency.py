from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slatency:
	"""Slatency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slatency", core, parent)

	def set(self, system_latency: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:SLATency \n
		Sets the time delay between the time specified with the parameter <ElapsedTime> in the HIL mode A position data command
		and the time this command is executed in the R&S SMBV100B. See also 'System Latency'. You can use the retrieved value for
		latency calibration, see 'Latency Calibration'. \n
			:param system_latency: float Range: 0.002 to 0.15, Unit: s
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(system_latency)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:SLATency {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:SLATency \n
		Sets the time delay between the time specified with the parameter <ElapsedTime> in the HIL mode A position data command
		and the time this command is executed in the R&S SMBV100B. See also 'System Latency'. You can use the retrieved value for
		latency calibration, see 'Latency Calibration'. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: system_latency: float Range: 0.002 to 0.15, Unit: s"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:SLATency?')
		return Conversions.str_to_float(response)
