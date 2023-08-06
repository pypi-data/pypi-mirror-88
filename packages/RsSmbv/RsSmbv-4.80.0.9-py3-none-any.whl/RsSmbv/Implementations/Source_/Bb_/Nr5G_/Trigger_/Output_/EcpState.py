from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EcpState:
	"""EcpState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ecpState", core, parent)

	def set(self, scs_ecp_state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:ECPState \n
		Enables/disables the extended cyclic prefix (ECP) for a UL/DL pattern containing a marker. \n
			:param scs_ecp_state: 0| 1| OFF| ON 0|OFF Disables the ECP. 1|ON Enables the ECP.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.bool_to_str(scs_ecp_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:ECPState {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:ECPState \n
		Enables/disables the extended cyclic prefix (ECP) for a UL/DL pattern containing a marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: scs_ecp_state: 0| 1| OFF| ON 0|OFF Disables the ECP. 1|ON Enables the ECP."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:ECPState?')
		return Conversions.str_to_bool(response)
