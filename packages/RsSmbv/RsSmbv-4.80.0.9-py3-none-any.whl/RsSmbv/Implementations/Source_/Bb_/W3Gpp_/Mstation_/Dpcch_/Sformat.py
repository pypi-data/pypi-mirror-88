from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sformat:
	"""Sformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sformat", core, parent)

	def set(self, sf_ormat: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:SFORmat \n
		The command sets the slot format for the DPCCH. The slot format defines the structure of the DPCCH slots and the control
		fields. Slot formats 0 to 4 are available for the DPCCH channel as defined in the 3GPP Release 7 specification TS 25.211.
		Note: The former slot formats 4 and 5 according to 3GPP Release 4 specification TS 25.211 are not supported any more. The
		command sets the FBI mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Fbi.Mode.set) , the TFCI status (method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set) and the TPC Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Mode.
		set) to the associated values. \n
			:param sf_ormat: integer Range: 0 to 4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(sf_ormat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:SFORmat {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:SFORmat \n
		The command sets the slot format for the DPCCH. The slot format defines the structure of the DPCCH slots and the control
		fields. Slot formats 0 to 4 are available for the DPCCH channel as defined in the 3GPP Release 7 specification TS 25.211.
		Note: The former slot formats 4 and 5 according to 3GPP Release 4 specification TS 25.211 are not supported any more. The
		command sets the FBI mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Fbi.Mode.set) , the TFCI status (method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Dpcch.Tfci.State.set) and the TPC Mode (method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Tpc.Mode.
		set) to the associated values. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: sf_ormat: integer Range: 0 to 4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:SFORmat?')
		return Conversions.str_to_int(response)
