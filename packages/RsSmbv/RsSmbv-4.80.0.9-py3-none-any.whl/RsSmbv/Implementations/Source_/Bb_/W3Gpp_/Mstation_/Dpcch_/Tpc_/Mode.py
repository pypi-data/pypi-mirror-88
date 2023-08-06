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

	def set(self, mode: enums.TpcMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:MODE \n
		Selects the TPC (Transmit Power Control) mode. The command sets the slot format (method RsSmbv.Source.Bb.W3Gpp.Mstation.
		Dpcch.Sformat.set) in conjunction with the set TFCI status (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set)
		and the FBI Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Fbi.Mode.set) to the associated values. \n
			:param mode: D2B| D4B D2B A TPC field with a length of 2 bits is used. D4B A TPC field with a length of 4 bits is used. A 4 bits long TPC field can be selected, only for Slot Format 4 and disabled FBI and TFCI fields.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.TpcMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TpcMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:TPC:MODE \n
		Selects the TPC (Transmit Power Control) mode. The command sets the slot format (method RsSmbv.Source.Bb.W3Gpp.Mstation.
		Dpcch.Sformat.set) in conjunction with the set TFCI status (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set)
		and the FBI Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Fbi.Mode.set) to the associated values. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mode: D2B| D4B D2B A TPC field with a length of 2 bits is used. D4B A TPC field with a length of 4 bits is used. A 4 bits long TPC field can be selected, only for Slot Format 4 and disabled FBI and TFCI fields."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:TPC:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TpcMode)
