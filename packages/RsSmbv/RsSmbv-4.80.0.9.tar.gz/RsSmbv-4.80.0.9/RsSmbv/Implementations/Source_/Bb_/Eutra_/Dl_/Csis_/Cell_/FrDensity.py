from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrDensity:
	"""FrDensity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: FreqDensity, default value after init: FreqDensity.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frDensity", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_freqDensity_get', 'repcap_freqDensity_set', repcap.FreqDensity.Nr0)

	def clone(self) -> 'FrDensity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FrDensity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_freqDensity_set(self, enum_value: repcap.FreqDensity) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FreqDensity.Default
		Default value after init: FreqDensity.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_freqDensity_get(self) -> repcap.FreqDensity:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, csi_rf_freq_density: enums.EutraCsiRsFreqDensity, channel=repcap.Channel.Default, freqDensity=repcap.FreqDensity.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:FRDensity<ST_OPTIONAL> \n
		Sets the parameter NZP-FrequencyDensity. \n
			:param csi_rf_freq_density: D1| D12| D13
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param freqDensity: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrDensity')"""
		param = Conversions.enum_scalar_to_str(csi_rf_freq_density, enums.EutraCsiRsFreqDensity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		freqDensity_cmd_val = self._base.get_repcap_cmd_value(freqDensity, repcap.FreqDensity)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:FRDensity{freqDensity_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, freqDensity=repcap.FreqDensity.Default) -> enums.EutraCsiRsFreqDensity:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:FRDensity<ST_OPTIONAL> \n
		Sets the parameter NZP-FrequencyDensity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param freqDensity: optional repeated capability selector. Default value: Nr0 (settable in the interface 'FrDensity')
			:return: csi_rf_freq_density: D1| D12| D13"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		freqDensity_cmd_val = self._base.get_repcap_cmd_value(freqDensity, repcap.FreqDensity)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:FRDensity{freqDensity_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCsiRsFreqDensity)
