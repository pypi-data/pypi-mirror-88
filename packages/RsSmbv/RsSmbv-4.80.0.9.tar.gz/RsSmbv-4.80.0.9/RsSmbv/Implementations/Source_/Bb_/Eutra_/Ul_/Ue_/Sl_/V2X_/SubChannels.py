from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubChannels:
	"""SubChannels commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subChannels", core, parent)

	def set(self, num_subchannels: enums.EutraSlV2XnUmSubchannels, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SUBChannels \n
		Sets the number of subchannels. \n
			:param num_subchannels: 1| 3| 5| 8| 10| 15| 20
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(num_subchannels, enums.EutraSlV2XnUmSubchannels)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SUBChannels {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlV2XnUmSubchannels:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SUBChannels \n
		Sets the number of subchannels. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: num_subchannels: 1| 3| 5| 8| 10| 15| 20"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SUBChannels?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlV2XnUmSubchannels)
