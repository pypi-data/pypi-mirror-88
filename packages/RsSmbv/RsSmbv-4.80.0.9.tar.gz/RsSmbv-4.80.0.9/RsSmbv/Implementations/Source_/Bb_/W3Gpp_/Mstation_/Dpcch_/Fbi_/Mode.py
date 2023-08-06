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
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:FBI:MODE \n
		The command sets the number of bits for the FBI field. With OFF, the FBI field is not used. Note: The former 2-bits long
		FBI Mode 'D2B' according to 3GPP Release 4 specification TS 25.211 is not supported any more. The command sets the slot
		format (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Sformat.set) in conjunction with the set TFCI status (method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set) and the TPC Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Mode.
		set) to the associated values. \n
			:param mode: OFF| D1B
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.FbiMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:FBI:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.FbiMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:FBI:MODE \n
		The command sets the number of bits for the FBI field. With OFF, the FBI field is not used. Note: The former 2-bits long
		FBI Mode 'D2B' according to 3GPP Release 4 specification TS 25.211 is not supported any more. The command sets the slot
		format (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Sformat.set) in conjunction with the set TFCI status (method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set) and the TPC Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Mode.
		set) to the associated values. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mode: OFF| D1B"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:FBI:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FbiMode)
