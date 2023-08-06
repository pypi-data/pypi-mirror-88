from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spcsi:
	"""Spcsi commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spcsi", core, parent)

	def set(self, sp_csi_rnti: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:SPCSi \n
		Sets the SP-CSI-RNTI of the user. It is a unique UE identification used for semi-persistent CSI reporting on PUSCH. \n
			:param sp_csi_rnti: integer Range: 1 to 65519
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(sp_csi_rnti)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:SPCSi {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:RNTI:SPCSi \n
		Sets the SP-CSI-RNTI of the user. It is a unique UE identification used for semi-persistent CSI reporting on PUSCH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: sp_csi_rnti: integer Range: 1 to 65519"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:RNTI:SPCSi?')
		return Conversions.str_to_int(response)
