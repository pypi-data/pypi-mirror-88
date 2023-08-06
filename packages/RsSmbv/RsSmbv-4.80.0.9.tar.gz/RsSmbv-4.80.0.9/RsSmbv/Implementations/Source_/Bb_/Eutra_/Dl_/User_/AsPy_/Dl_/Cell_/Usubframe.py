from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usubframe:
	"""Usubframe commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: DlSubframeIx, default value after init: DlSubframeIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usubframe", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_dlSubframeIx_get', 'repcap_dlSubframeIx_set', repcap.DlSubframeIx.Nr0)

	def clone(self) -> 'Usubframe':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Usubframe(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_dlSubframeIx_set(self, enum_value: repcap.DlSubframeIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to DlSubframeIx.Default
		Default value after init: DlSubframeIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_dlSubframeIx_get(self) -> repcap.DlSubframeIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, use_subfr: bool, channel=repcap.Channel.Default, carrierComponent=repcap.CarrierComponent.Nr1, dlSubframeIx=repcap.DlSubframeIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:[CELL<CCIDX>]:USUBframe<DIR> \n
		Sets the downlink subframes to be used for the HARQ transmission. \n
			:param use_subfr: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param dlSubframeIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Usubframe')"""
		param = Conversions.bool_to_str(use_subfr)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		dlSubframeIx_cmd_val = self._base.get_repcap_cmd_value(dlSubframeIx, repcap.DlSubframeIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{carrierComponent_cmd_val}:USUBframe{dlSubframeIx_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, carrierComponent=repcap.CarrierComponent.Nr1, dlSubframeIx=repcap.DlSubframeIx.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:AS:DL:[CELL<CCIDX>]:USUBframe<DIR> \n
		Sets the downlink subframes to be used for the HARQ transmission. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param dlSubframeIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Usubframe')
			:return: use_subfr: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		dlSubframeIx_cmd_val = self._base.get_repcap_cmd_value(dlSubframeIx, repcap.DlSubframeIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:AS:DL:CELL{carrierComponent_cmd_val}:USUBframe{dlSubframeIx_cmd_val}?')
		return Conversions.str_to_bool(response)
