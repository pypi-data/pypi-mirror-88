from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Latency:
	"""Latency commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("latency", core, parent)

	def clone(self) -> 'Latency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Latency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def statistics(self):
		"""statistics commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_statistics'):
			from .Latency_.Statistics import Statistics
			self._statistics = Statistics(self._core, self._base)
		return self._statistics

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RT:RECeiver:[V<ST>]:HILPosition:LATency \n
		Queries the time delay (or prediction latency) between the time specified with the parameter <ElapsedTime> in the HIL
		mode A position data command and the time this command is executed in the R&S SMBV100B. You can use the retrieved value
		for latency calibration, see 'Latency Calibration'. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: latency: float Range: min to max, Unit: s"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RT:RECeiver:V{stream_cmd_val}:HILPosition:LATency?')
		return Conversions.str_to_float(response)
