from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Transcomb:
	"""Transcomb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: TransComb, default value after init: TransComb.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("transcomb", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_transComb_get', 'repcap_transComb_set', repcap.TransComb.Nr0)

	def clone(self) -> 'Transcomb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Transcomb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_transComb_set(self, enum_value: repcap.TransComb) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TransComb.Default
		Default value after init: TransComb.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_transComb_get(self) -> repcap.TransComb:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, csi_rs_trans_comb: enums.EutraCsiRsTransComb, channel=repcap.Channel.Default, transComb=repcap.TransComb.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:TRANscomb<ST_OPTIONAL> \n
		Sets the parameter NZP-TransmissionComb. \n
			:param csi_rs_trans_comb: 0| 1| 2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param transComb: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Transcomb')"""
		param = Conversions.enum_scalar_to_str(csi_rs_trans_comb, enums.EutraCsiRsTransComb)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transComb_cmd_val = self._base.get_repcap_cmd_value(transComb, repcap.TransComb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:TRANscomb{transComb_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, transComb=repcap.TransComb.Default) -> enums.EutraCsiRsTransComb:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:TRANscomb<ST_OPTIONAL> \n
		Sets the parameter NZP-TransmissionComb. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param transComb: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Transcomb')
			:return: csi_rs_trans_comb: 0| 1| 2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transComb_cmd_val = self._base.get_repcap_cmd_value(transComb, repcap.TransComb)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:TRANscomb{transComb_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCsiRsTransComb)
