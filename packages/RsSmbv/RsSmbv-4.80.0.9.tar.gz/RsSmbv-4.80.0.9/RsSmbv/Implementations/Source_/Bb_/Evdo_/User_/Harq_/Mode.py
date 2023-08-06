from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.EvdoHarqMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:HARQ:MODE \n
		Enables or disables the H-ARQ Channel. The H-ARQ channel is used by the access network to transmit positive
		acknowledgement (ACK) or a negative acknowledgement (NAK) in response to a physical layer packet. Note: This parameter is
		enabled for Physical Layer Subtype 2 only. \n
			:param mode: OFF| ACK| NAK OFF Disables transmission of the H-ARQ channel. ACK Enables transmission of H-ARQ. The channel is transmitted with all bits set to ACK. NAK Enables transmission of H-ARQ. The channel is transmitted with all bits set to NAK
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(mode, enums.EvdoHarqMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:HARQ:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoHarqMode:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:HARQ:MODE \n
		Enables or disables the H-ARQ Channel. The H-ARQ channel is used by the access network to transmit positive
		acknowledgement (ACK) or a negative acknowledgement (NAK) in response to a physical layer packet. Note: This parameter is
		enabled for Physical Layer Subtype 2 only. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: mode: OFF| ACK| NAK OFF Disables transmission of the H-ARQ channel. ACK Enables transmission of H-ARQ. The channel is transmitted with all bits set to ACK. NAK Enables transmission of H-ARQ. The channel is transmitted with all bits set to NAK"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:HARQ:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoHarqMode)
