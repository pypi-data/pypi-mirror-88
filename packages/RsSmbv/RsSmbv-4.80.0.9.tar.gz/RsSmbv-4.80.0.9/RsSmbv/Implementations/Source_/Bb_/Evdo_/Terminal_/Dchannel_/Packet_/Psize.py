from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psize:
	"""Psize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psize", core, parent)

	def set(self, psize: enums.EvdoPayload, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:PSIZe \n
		(enabled for an access terminal working in traffic mode) Sets the Payload Size in bits for the selected packet.
		Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for
		physical layer subtype 2. \n
			:param psize: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS6144| PS8192| PS12288
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')"""
		param = Conversions.enum_scalar_to_str(psize, enums.EvdoPayload)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:PSIZe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EvdoPayload:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DCHannel:PACKet<CH>:PSIZe \n
		(enabled for an access terminal working in traffic mode) Sets the Payload Size in bits for the selected packet.
		Note: Configuration of Packet 2 and Packet 3 transmitted on the second and the third subframe, is only enabled for
		physical layer subtype 2. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Packet')
			:return: psize: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS6144| PS8192| PS12288"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DCHannel:PACKet{channel_cmd_val}:PSIZe?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoPayload)
