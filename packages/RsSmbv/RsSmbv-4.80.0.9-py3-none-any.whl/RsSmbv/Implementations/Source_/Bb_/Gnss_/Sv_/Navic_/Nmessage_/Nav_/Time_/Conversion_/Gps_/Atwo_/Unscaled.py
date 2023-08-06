from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, a_2: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:NAVic<ST>:NMESsage:NAV:TIME:CONVersion:GPS<CH>:ATWO:UNSCaled \n
		Sets the A2 parameter. \n
			:param a_2: integer Range: -64 to 63
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(a_2)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:NAVic{stream_cmd_val}:NMESsage:NAV:TIME:CONVersion:GPS{channel_cmd_val}:ATWO:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:SV:NAVic<ST>:NMESsage:NAV:TIME:CONVersion:GPS<CH>:ATWO:UNSCaled \n
		Sets the A2 parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: a_2: integer Range: -64 to 63"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:NAVic{stream_cmd_val}:NMESsage:NAV:TIME:CONVersion:GPS{channel_cmd_val}:ATWO:UNSCaled?')
		return Conversions.str_to_float(response)
