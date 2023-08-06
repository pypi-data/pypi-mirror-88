from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Config:
	"""Config commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: ConfigIx, default value after init: ConfigIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("config", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_configIx_get', 'repcap_configIx_set', repcap.ConfigIx.Nr0)

	def clone(self) -> 'Config':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Config(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_configIx_set(self, enum_value: repcap.ConfigIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to ConfigIx.Default
		Default value after init: ConfigIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_configIx_get(self) -> repcap.ConfigIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, csi_rs_config: int, channel=repcap.Channel.Default, configIx=repcap.ConfigIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:CONFig<ST_OPTIONAL> \n
		Defines the CSI-RS configuration used for the current cell and for which the UE assumes non-zero transmission power. \n
			:param csi_rs_config: integer Range: 0 to 31
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param configIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Config')"""
		param = Conversions.decimal_value_to_str(csi_rs_config)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		configIx_cmd_val = self._base.get_repcap_cmd_value(configIx, repcap.ConfigIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:CONFig{configIx_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, configIx=repcap.ConfigIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:CONFig<ST_OPTIONAL> \n
		Defines the CSI-RS configuration used for the current cell and for which the UE assumes non-zero transmission power. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param configIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Config')
			:return: csi_rs_config: integer Range: 0 to 31"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		configIx_cmd_val = self._base.get_repcap_cmd_value(configIx, repcap.ConfigIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:CONFig{configIx_cmd_val}?')
		return Conversions.str_to_int(response)
