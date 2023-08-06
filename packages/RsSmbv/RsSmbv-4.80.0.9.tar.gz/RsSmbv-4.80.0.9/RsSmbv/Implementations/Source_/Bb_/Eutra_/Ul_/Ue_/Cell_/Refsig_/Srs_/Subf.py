from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subf:
	"""Subf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: SubframeIx, default value after init: SubframeIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subf", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subframeIx_get', 'repcap_subframeIx_set', repcap.SubframeIx.Nr1)

	def clone(self) -> 'Subf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Subf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_subframeIx_set(self, enum_value: repcap.SubframeIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SubframeIx.Default
		Default value after init: SubframeIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subframeIx_get(self) -> repcap.SubframeIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, subframe: int, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default, subframeIx=repcap.SubframeIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:SUBF<SUBFIDX> \n
		Sets the subframes in that SRS is transmitted. \n
			:param subframe: integer Range: 0 to (10*SeqLengthARB - 1)
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')
			:param subframeIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.decimal_value_to_str(subframe)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		subframeIx_cmd_val = self._base.get_repcap_cmd_value(subframeIx, repcap.SubframeIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:SUBF{subframeIx_cmd_val} {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default, soundRefSignalIx=repcap.SoundRefSignalIx.Default, subframeIx=repcap.SubframeIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:REFSig:SRS<SRSIDX_OPTIONAL>:SUBF<SUBFIDX> \n
		Sets the subframes in that SRS is transmitted. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param soundRefSignalIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Srs')
			:param subframeIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: subframe: integer Range: 0 to (10*SeqLengthARB - 1)"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		soundRefSignalIx_cmd_val = self._base.get_repcap_cmd_value(soundRefSignalIx, repcap.SoundRefSignalIx)
		subframeIx_cmd_val = self._base.get_repcap_cmd_value(subframeIx, repcap.SubframeIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:REFSig:SRS{soundRefSignalIx_cmd_val}:SUBF{subframeIx_cmd_val}?')
		return Conversions.str_to_int(response)
