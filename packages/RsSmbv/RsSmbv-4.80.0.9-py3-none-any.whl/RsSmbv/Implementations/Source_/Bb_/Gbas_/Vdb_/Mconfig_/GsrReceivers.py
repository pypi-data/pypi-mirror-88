from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsrReceivers:
	"""GsrReceivers commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gsrReceivers", core, parent)

	def set(self, gsrr: enums.GbasGrdStRefRec, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GSRReceivers \n
		Sets the number of ground station reference receivers. \n
			:param gsrr: GW3R| GW4R| GW2R
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(gsrr, enums.GbasGrdStRefRec)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GSRReceivers {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasGrdStRefRec:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GSRReceivers \n
		Sets the number of ground station reference receivers. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: gsrr: GW3R| GW4R| GW2R"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GSRReceivers?')
		return Conversions.str_to_scalar_enum(response, enums.GbasGrdStRefRec)
