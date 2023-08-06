from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:MULTislot<ST>:STATe \n
		Switches the multislot configuration on. The suffix in MULTislot defines the first slot in a multislot group.
		In a multiframe configuration, this setting applies to the slots in all frames. \n
			:param state: 0| 1| OFF| ON
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'MultiSlot')"""
		param = Conversions.bool_to_str(state)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:MULTislot{stream_cmd_val}:STATe {param}')

	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:MULTislot<ST>:STATe \n
		Switches the multislot configuration on. The suffix in MULTislot defines the first slot in a multislot group.
		In a multiframe configuration, this setting applies to the slots in all frames. \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'MultiSlot')
			:return: state: 0| 1| OFF| ON"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:MULTislot{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
