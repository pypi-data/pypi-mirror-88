from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CycShift:
	"""CycShift commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cycShift", core, parent)

	def set(self, cyclic_shift: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:CYCShift \n
		Sets the cyclic shift used for the generation of the sounding reference signal CAZAC sequence. \n
			:param cyclic_shift: integer Range: 0 to 11 CyclicShift = 7 to 11 if BB:EUTRa:UL:REFSig:NKTC 4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')"""
		param = Conversions.decimal_value_to_str(cyclic_shift)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:CYCShift {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:CYCShift \n
		Sets the cyclic shift used for the generation of the sounding reference signal CAZAC sequence. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')
			:return: cyclic_shift: integer Range: 0 to 11 CyclicShift = 7 to 11 if BB:EUTRa:UL:REFSig:NKTC 4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:CYCShift?')
		return Conversions.str_to_int(response)
