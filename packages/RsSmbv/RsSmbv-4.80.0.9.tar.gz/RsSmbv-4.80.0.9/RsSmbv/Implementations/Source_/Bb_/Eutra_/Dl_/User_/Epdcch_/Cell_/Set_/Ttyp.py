from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttyp:
	"""Ttyp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ttyp", core, parent)

	def set(self, trans_type: enums.EutraEpdcchTransType, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:TTYP \n
		Select the EPDCCH transmission type. \n
			:param trans_type: LOCalized| DISTributed
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.enum_scalar_to_str(trans_type, enums.EutraEpdcchTransType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:TTYP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, direction=repcap.Direction.Default) -> enums.EutraEpdcchTransType:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:EPDCch:CELL<ST>:SET<DIR>:TTYP \n
		Select the EPDCCH transmission type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param direction: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: trans_type: LOCalized| DISTributed"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		direction_cmd_val = self._base.get_repcap_cmd_value(direction, repcap.Direction)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:EPDCch:CELL{stream_cmd_val}:SET{direction_cmd_val}:TTYP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraEpdcchTransType)
