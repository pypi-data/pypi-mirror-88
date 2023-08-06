from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubSize:
	"""SubSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subSize", core, parent)

	def set(self, subchannel_size: enums.EutraSlV2XSubchannelSize, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SUBSize \n
		Sets the number of resource blocks the subchannel spans. \n
			:param subchannel_size: 4| 5| 6| 8| 9| 10| 12| 15| 16| 18| 20| 25| 30| 48| 50| 72| 96| 75| 100| 32
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(subchannel_size, enums.EutraSlV2XSubchannelSize)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SUBSize {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlV2XSubchannelSize:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SUBSize \n
		Sets the number of resource blocks the subchannel spans. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: subchannel_size: 4| 5| 6| 8| 9| 10| 12| 15| 16| 18| 20| 25| 30| 48| 50| 72| 96| 75| 100| 32"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SUBSize?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlV2XSubchannelSize)
