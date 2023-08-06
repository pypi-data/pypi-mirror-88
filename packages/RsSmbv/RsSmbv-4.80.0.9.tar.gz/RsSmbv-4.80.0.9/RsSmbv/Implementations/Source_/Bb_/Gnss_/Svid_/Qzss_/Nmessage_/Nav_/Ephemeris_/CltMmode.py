from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CltMmode:
	"""CltMmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cltMmode", core, parent)

	def set(self, code_on_l_2_mode: enums.CodeOnL2, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:EPHemeris:CLTMode \n
		Sets the code on L2. \n
			:param code_on_l_2_mode: REServed| PCODe| CACode
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.enum_scalar_to_str(code_on_l_2_mode, enums.CodeOnL2)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:EPHemeris:CLTMode {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.CodeOnL2:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:EPHemeris:CLTMode \n
		Sets the code on L2. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: code_on_l_2_mode: REServed| PCODe| CACode"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:EPHemeris:CLTMode?')
		return Conversions.str_to_scalar_enum(response, enums.CodeOnL2)
