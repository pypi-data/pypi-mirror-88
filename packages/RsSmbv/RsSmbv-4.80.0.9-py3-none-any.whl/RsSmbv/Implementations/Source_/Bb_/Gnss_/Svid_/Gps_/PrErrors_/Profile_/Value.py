from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("value", core, parent)

	def set(self, profile_value: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:PRERrors:PROFile<GR>:VALue \n
		Sets the pseudorange error value. \n
			:param profile_value: float Range: -1000 to 1000
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		param = Conversions.decimal_value_to_str(profile_value)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:VALue {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:PRERrors:PROFile<GR>:VALue \n
		Sets the pseudorange error value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')
			:return: profile_value: float Range: -1000 to 1000"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:VALue?')
		return Conversions.str_to_float(response)
