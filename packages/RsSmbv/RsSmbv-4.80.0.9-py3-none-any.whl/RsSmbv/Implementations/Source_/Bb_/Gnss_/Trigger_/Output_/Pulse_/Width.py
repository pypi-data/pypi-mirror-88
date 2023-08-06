from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Width:
	"""Width commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("width", core, parent)

	def set(self, width: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:PULSe:WIDTh \n
		Sets the pulse width for 1PPS, 1PP2S and PPS10 marker mode. The maximum pulse width depends on the marker mode.
			Table Header:  \n
			- Marker mode / 1PPS / 1PP2S / PPS10
			- Max. pulse width / 1 s / 2 s / 0.1 s \n
			:param width: float Range: 1E-9 to depends on the marker mode
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(width)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:PULSe:WIDTh {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:TRIGger:OUTPut<CH>:PULSe:WIDTh \n
		Sets the pulse width for 1PPS, 1PP2S and PPS10 marker mode. The maximum pulse width depends on the marker mode.
			Table Header:  \n
			- Marker mode / 1PPS / 1PP2S / PPS10
			- Max. pulse width / 1 s / 2 s / 0.1 s \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: width: float Range: 1E-9 to depends on the marker mode"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TRIGger:OUTPut{channel_cmd_val}:PULSe:WIDTh?')
		return Conversions.str_to_float(response)
