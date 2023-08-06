from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	# noinspection PyTypeChecker
	def get(self, carrierComponent=repcap.CarrierComponent.Default, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraUlFreqHopType:
		"""[SOURce<HW>]:BB:EUTRa:UL:[CELL<CCIDX>]:[SUBF<ST>]:ALLoc<CH>:PUSCh:FHOP:TYPE \n
		Queries the frequency hopping type used, as defined in 3GPP TS36.213. \n
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: type_py: TP1| TP2| NONE"""
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:CELL{carrierComponent_cmd_val}:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUSCh:FHOP:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlFreqHopType)
