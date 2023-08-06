from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............Internal.RepeatedCapability import RepeatedCapability
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TmiValue:
	"""TmiValue commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: IndicatorNr, default value after init: IndicatorNr.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmiValue", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_indicatorNr_get', 'repcap_indicatorNr_set', repcap.IndicatorNr.Nr0)

	def clone(self) -> 'TmiValue':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TmiValue(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_indicatorNr_set(self, enum_value: repcap.IndicatorNr) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to IndicatorNr.Default
		Default value after init: IndicatorNr.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_indicatorNr_get(self) -> repcap.IndicatorNr:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, user_ul_bwp_pucch_d: float, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, indicatorNr=repcap.IndicatorNr.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUCCh:PDSHarq:TMIValue<GR> \n
		Sets the individual timing values. \n
			:param user_ul_bwp_pucch_d: float Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param indicatorNr: optional repeated capability selector. Default value: Nr0 (settable in the interface 'TmiValue')"""
		param = Conversions.decimal_value_to_str(user_ul_bwp_pucch_d)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		indicatorNr_cmd_val = self._base.get_repcap_cmd_value(indicatorNr, repcap.IndicatorNr)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUCCh:PDSHarq:TMIValue{indicatorNr_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default, indicatorNr=repcap.IndicatorNr.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUCCh:PDSHarq:TMIValue<GR> \n
		Sets the individual timing values. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:param indicatorNr: optional repeated capability selector. Default value: Nr0 (settable in the interface 'TmiValue')
			:return: user_ul_bwp_pucch_d: float Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		indicatorNr_cmd_val = self._base.get_repcap_cmd_value(indicatorNr, repcap.IndicatorNr)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUCCh:PDSHarq:TMIValue{indicatorNr_cmd_val}?')
		return Conversions.str_to_float(response)
