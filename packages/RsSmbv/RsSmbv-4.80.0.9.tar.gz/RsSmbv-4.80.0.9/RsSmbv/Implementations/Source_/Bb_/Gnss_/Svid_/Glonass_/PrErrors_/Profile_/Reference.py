from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reference", core, parent)

	def set(self, profile_ref_time: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:PRERrors:PROFile<GR>:REFerence \n
		Sets the reference time for the pseudorange error. \n
			:param profile_ref_time: float Range: 0 to 86400
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')"""
		param = Conversions.decimal_value_to_str(profile_ref_time)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:REFerence {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, pseudoRange=repcap.PseudoRange.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:PRERrors:PROFile<GR>:REFerence \n
		Sets the reference time for the pseudorange error. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:param pseudoRange: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Profile')
			:return: profile_ref_time: float Range: 0 to 86400"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		pseudoRange_cmd_val = self._base.get_repcap_cmd_value(pseudoRange, repcap.PseudoRange)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:PRERrors:PROFile{pseudoRange_cmd_val}:REFerence?')
		return Conversions.str_to_float(response)
