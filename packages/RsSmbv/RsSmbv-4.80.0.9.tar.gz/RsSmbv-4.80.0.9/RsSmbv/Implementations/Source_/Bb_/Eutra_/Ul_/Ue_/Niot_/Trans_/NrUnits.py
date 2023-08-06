from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NrUnits:
	"""NrUnits commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nrUnits", core, parent)

	def set(self, resource_units: enums.EutraIotRu, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:NRUNits \n
		Sets the number of allocated resource units. \n
			:param resource_units: RU1| RU2| RU3| RU4| RU5| RU6| RU8| RU10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')"""
		param = Conversions.enum_scalar_to_str(resource_units, enums.EutraIotRu)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:NRUNits {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraIotRu:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:TRANs<CH>:NRUNits \n
		Sets the number of allocated resource units. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Trans')
			:return: resource_units: RU1| RU2| RU3| RU4| RU5| RU6| RU8| RU10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:TRANs{channel_cmd_val}:NRUNits?')
		return Conversions.str_to_scalar_enum(response, enums.EutraIotRu)
