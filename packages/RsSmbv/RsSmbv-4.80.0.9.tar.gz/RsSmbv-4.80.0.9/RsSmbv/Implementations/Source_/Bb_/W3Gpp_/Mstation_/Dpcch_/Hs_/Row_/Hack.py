from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hack:
	"""Hack commands group definition. 3 total commands, 2 Sub-groups, 1 group commands
	Repeated Capability: TwoStreams, default value after init: TwoStreams.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hack", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_twoStreams_get', 'repcap_twoStreams_set', repcap.TwoStreams.Nr0)

	def clone(self) -> 'Hack':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hack(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_twoStreams_set(self, enum_value: repcap.TwoStreams) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TwoStreams.Default
		Default value after init: TwoStreams.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_twoStreams_get(self) -> repcap.TwoStreams:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def fromPy(self):
		"""fromPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fromPy'):
			from .Hack_.FromPy import FromPy
			self._fromPy = FromPy(self._core, self._base)
		return self._fromPy

	@property
	def to(self):
		"""to commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_to'):
			from .Hack_.To import To
			self._to = To(self._core, self._base)
		return self._to

	def set(self, harq_ack: enums.HsRel8HarqMode, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:HACK<DI> \n
		(Release 8 and Later) Sets the information transmitted during the HARQ-ACK slots of the TTIs during the corresponding
		specified HARQ-ACK From/To range. For detailed description, see 'HS-DPCCH 1/2, HARQ-ACK 1/2/3/4'.
		The Table 'Cross-reference between the used GUI terms and abbreviations in the SCPI command' provides the necessary
		cross-reference information. Cross-reference between the used GUI terms and abbreviations in the SCPI command
			Table Header: Value name / Parameter value \n
			- 'DTX' / DTX | D_DTX
			- 'PRE, POST' / PRE | POST
			- 'A, N' / A | N
			- 'AA, AN, NA, NN' / M_A | M_N | M_AA | M_AN | M_NA | M_NN
			- 'A/D, N/A, …' (different combinations possible) / S_A_D | S_N_A | ... (different combinations possible)
			- 'A/D/D, N/D/D, …' (different combinations possible) / S2_N_N_N | S2_N_N_A | ... (different combinations possible)
			- 'AN/NN, D/AA, …' (different combinations possible) / MS_AA_AA | MS_D_AA ... (different combinations possible) \n
			:param harq_ack: DTX| PRE| POST| A| N| M_A| M_N| M_AA| M_AN| M_NA| M_NN| S_A_D| S_N_D| S_D_A| S_D_N| S_A_A| S_A_N| S_N_A| S_N_N| MS_A_D| MS_N_D| MS_AA_D| MS_AN_D| MS_NA_D| MS_NN_D| MS_D_A| MS_D_N| MS_D_AA| MS_D_AN| MS_D_NA| MS_D_NN| MS_A_A| MS_A_N| MS_N_A| MS_N_N| MS_A_AA| MS_A_AN| MS_A_NA| MS_A_NN| MS_N_AA| MS_N_AN| MS_N_NA| MS_N_NN| MS_AA_A| MS_AA_N| MS_AN_A| MS_AN_N| MS_NA_A| MS_NA_N| MS_NN_A| MS_NN_N| MS_AA_AA| MS_AA_AN| MS_AA_NA| MS_AA_NN| MS_AN_AA| MS_AN_AN| MS_AN_NA| MS_AN_NN| MS_NA_AA| MS_NA_AN| MS_NA_NA| MS_NA_NN| MS_NN_AA| MS_NN_AN| MS_NN_NA| MS_NN_NN| S2_A_D_D| S2_N_D_D| S2_D_A_D| S2_D_N_D| S2_D_D_A| S2_D_D_N| S2_A_A_D| S2_A_N_D| S2_N_A_D| S2_N_N_D| S2_A_D_A| S2_A_D_N| S2_N_D_A| S2_N_D_N| S2_D_A_A| S2_D_A_N| S2_D_N_A| S2_D_N_N| S2_A_A_A| S2_A_A_N| S2_A_N_A| S2_A_N_N| S2_N_A_A| S2_N_A_N| S2_N_N_A| S2_N_N_N| D_DTX
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Hack')"""
		param = Conversions.enum_scalar_to_str(harq_ack, enums.HsRel8HarqMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:HACK{twoStreams_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, twoStreams=repcap.TwoStreams.Default) -> enums.HsRel8HarqMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:ROW<CH>:HACK<DI> \n
		(Release 8 and Later) Sets the information transmitted during the HARQ-ACK slots of the TTIs during the corresponding
		specified HARQ-ACK From/To range. For detailed description, see 'HS-DPCCH 1/2, HARQ-ACK 1/2/3/4'.
		The Table 'Cross-reference between the used GUI terms and abbreviations in the SCPI command' provides the necessary
		cross-reference information. Cross-reference between the used GUI terms and abbreviations in the SCPI command
			Table Header: Value name / Parameter value \n
			- 'DTX' / DTX | D_DTX
			- 'PRE, POST' / PRE | POST
			- 'A, N' / A | N
			- 'AA, AN, NA, NN' / M_A | M_N | M_AA | M_AN | M_NA | M_NN
			- 'A/D, N/A, …' (different combinations possible) / S_A_D | S_N_A | ... (different combinations possible)
			- 'A/D/D, N/D/D, …' (different combinations possible) / S2_N_N_N | S2_N_N_A | ... (different combinations possible)
			- 'AN/NN, D/AA, …' (different combinations possible) / MS_AA_AA | MS_D_AA ... (different combinations possible) \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Row')
			:param twoStreams: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Hack')
			:return: harq_ack: DTX| PRE| POST| A| N| M_A| M_N| M_AA| M_AN| M_NA| M_NN| S_A_D| S_N_D| S_D_A| S_D_N| S_A_A| S_A_N| S_N_A| S_N_N| MS_A_D| MS_N_D| MS_AA_D| MS_AN_D| MS_NA_D| MS_NN_D| MS_D_A| MS_D_N| MS_D_AA| MS_D_AN| MS_D_NA| MS_D_NN| MS_A_A| MS_A_N| MS_N_A| MS_N_N| MS_A_AA| MS_A_AN| MS_A_NA| MS_A_NN| MS_N_AA| MS_N_AN| MS_N_NA| MS_N_NN| MS_AA_A| MS_AA_N| MS_AN_A| MS_AN_N| MS_NA_A| MS_NA_N| MS_NN_A| MS_NN_N| MS_AA_AA| MS_AA_AN| MS_AA_NA| MS_AA_NN| MS_AN_AA| MS_AN_AN| MS_AN_NA| MS_AN_NN| MS_NA_AA| MS_NA_AN| MS_NA_NA| MS_NA_NN| MS_NN_AA| MS_NN_AN| MS_NN_NA| MS_NN_NN| S2_A_D_D| S2_N_D_D| S2_D_A_D| S2_D_N_D| S2_D_D_A| S2_D_D_N| S2_A_A_D| S2_A_N_D| S2_N_A_D| S2_N_N_D| S2_A_D_A| S2_A_D_N| S2_N_D_A| S2_N_D_N| S2_D_A_A| S2_D_A_N| S2_D_N_A| S2_D_N_N| S2_A_A_A| S2_A_A_N| S2_A_N_A| S2_A_N_N| S2_N_A_A| S2_N_A_N| S2_N_N_A| S2_N_N_N| D_DTX"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		twoStreams_cmd_val = self._base.get_repcap_cmd_value(twoStreams, repcap.TwoStreams)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:ROW{channel_cmd_val}:HACK{twoStreams_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.HsRel8HarqMode)
