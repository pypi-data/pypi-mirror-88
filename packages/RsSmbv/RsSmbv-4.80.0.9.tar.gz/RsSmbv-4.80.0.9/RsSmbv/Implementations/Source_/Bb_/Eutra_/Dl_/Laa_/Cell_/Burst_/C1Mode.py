from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class C1Mode:
	"""C1Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("c1Mode", core, parent)

	def set(self, dc_i_1_cm_ode: enums.EutraLaadci1CMode, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:C1Mode \n
		Defines how the DCI format 1C is sent. \n
			:param dc_i_1_cm_ode: MANual| N1| N| N1N
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.enum_scalar_to_str(dc_i_1_cm_ode, enums.EutraLaadci1CMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:C1Mode {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EutraLaadci1CMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:C1Mode \n
		Defines how the DCI format 1C is sent. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: dc_i_1_cm_ode: MANual| N1| N| N1N"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:C1Mode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraLaadci1CMode)
