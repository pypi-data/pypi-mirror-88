from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Upptsadd:
	"""Upptsadd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("upptsadd", core, parent)

	def set(self, srs_up_pts_add: enums.EutraNumUpPts, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:UPPTsadd \n
		In TDD mode, sets the parameter srs-UpPtsAdd and defines the number of additional SC-FDMA symbols in UpPTS. \n
			:param srs_up_pts_add: 0| 2| 4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')"""
		param = Conversions.enum_scalar_to_str(srs_up_pts_add, enums.EutraNumUpPts)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:UPPTsadd {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default) -> enums.EutraNumUpPts:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:UPPTsadd \n
		In TDD mode, sets the parameter srs-UpPtsAdd and defines the number of additional SC-FDMA symbols in UpPTS. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')
			:return: srs_up_pts_add: 0| 2| 4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:UPPTsadd?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNumUpPts)
