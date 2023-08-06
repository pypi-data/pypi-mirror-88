from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("minimum", core, parent)

	def set(self, minimum: enums.EvdoPayload, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:APCHannel:PAYLoad:MINimum \n
		(enabled for Physical Layer subtype 2 and for an access terminal working in traffic mode) Sets the minimum payload size
		in bits of the data channel that activates the transmission of the auxiliary pilot channel. \n
			:param minimum: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS6144| PS8192| PS12288
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.enum_scalar_to_str(minimum, enums.EvdoPayload)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:APCHannel:PAYLoad:MINimum {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoPayload:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:APCHannel:PAYLoad:MINimum \n
		(enabled for Physical Layer subtype 2 and for an access terminal working in traffic mode) Sets the minimum payload size
		in bits of the data channel that activates the transmission of the auxiliary pilot channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: minimum: PS128| PS256| PS512| PS768| PS1024| PS1536| PS2048| PS3072| PS4096| PS6144| PS8192| PS12288"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:APCHannel:PAYLoad:MINimum?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoPayload)
