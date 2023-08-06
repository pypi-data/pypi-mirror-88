from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psize:
	"""Psize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psize", core, parent)

	def set(self, psize: enums.EvdoPacketSize, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PSIZe \n
		Sets the packet size for the packets sent to the selected user. Note: Selected rate becomes effective at the beginning of
		the next packet transmitted to the selected user. \n
			:param psize: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS5120| PS6144| PS8192| PS12288| PS7168
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(psize, enums.EvdoPacketSize)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PSIZe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoPacketSize:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PSIZe \n
		Sets the packet size for the packets sent to the selected user. Note: Selected rate becomes effective at the beginning of
		the next packet transmitted to the selected user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: psize: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS5120| PS6144| PS8192| PS12288| PS7168"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PSIZe?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoPacketSize)
