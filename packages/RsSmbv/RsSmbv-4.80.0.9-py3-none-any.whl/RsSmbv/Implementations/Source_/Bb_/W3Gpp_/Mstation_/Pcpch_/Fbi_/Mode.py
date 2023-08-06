from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.FbiMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:FBI:MODE \n
		The command sets the number of bits (1 or 2) for the FBI field. With OFF, the field is not used.
			INTRO_CMD_HELP: The FBI pattern automatically sets the associated slot format: \n
			- FBI OFF = Slot format 0
			- FBI 1 bit = Slot format 1
			- FBI 2 bits = Slot format 2 \n
			:param mode: OFF| D1B| D2B
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.FbiMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:FBI:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.FbiMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:FBI:MODE \n
		The command sets the number of bits (1 or 2) for the FBI field. With OFF, the field is not used.
			INTRO_CMD_HELP: The FBI pattern automatically sets the associated slot format: \n
			- FBI OFF = Slot format 0
			- FBI 1 bit = Slot format 1
			- FBI 2 bits = Slot format 2 \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mode: OFF| D1B| D2B"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:FBI:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FbiMode)
