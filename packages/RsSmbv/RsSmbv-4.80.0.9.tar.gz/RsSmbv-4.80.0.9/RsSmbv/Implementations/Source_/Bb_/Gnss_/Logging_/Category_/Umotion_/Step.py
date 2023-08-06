from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Step':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Step(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, resolution: enums.LogRes, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:STEP<ST> \n
		Sets the logging step. \n
			:param resolution: R1S| R2S| R5S| R10S| R02S| R04S| R08S
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Step')"""
		param = Conversions.enum_scalar_to_str(resolution, enums.LogRes)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:STEP{stream_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.LogRes:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:CATegory:UMOTion:STEP<ST> \n
		Sets the logging step. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Step')
			:return: resolution: R1S| R2S| R5S| R10S| R02S| R04S| R08S"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:LOGGing:CATegory:UMOTion:STEP{stream_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.LogRes)
