from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Infinite:
	"""Infinite commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("infinite", core, parent)

	def set(self, infinite: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PACKet:INFinite \n
		Enables or disables sending an unlimited number of packets to the selected user. \n
			:param infinite: 0| 1| OFF| ON ON Enables sending of an unlimited number of packets to the user. OFF Disables sending of an unlimited number of packets to the user. The number of packets to be sent can be specified.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.bool_to_str(infinite)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PACKet:INFinite {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PACKet:INFinite \n
		Enables or disables sending an unlimited number of packets to the selected user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: infinite: 0| 1| OFF| ON ON Enables sending of an unlimited number of packets to the user. OFF Disables sending of an unlimited number of packets to the user. The number of packets to be sent can be specified."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PACKet:INFinite?')
		return Conversions.str_to_bool(response)
