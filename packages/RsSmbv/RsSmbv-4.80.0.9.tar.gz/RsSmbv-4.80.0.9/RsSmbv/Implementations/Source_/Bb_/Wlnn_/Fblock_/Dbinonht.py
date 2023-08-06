from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dbinonht:
	"""Dbinonht commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dbinonht", core, parent)

	def set(self, dbi_nonht: enums.WlannFbDynBwInNonHt, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DBINonht \n
		(available only for VHT Tx mode) Modifys the first 7 bits of the scrambling sequence to indicate if the transmitter is
		capable of 'Static' or 'Dynamic' bandwidth operation. \n
			:param dbi_nonht: STAT| DYN| OFF STAT The transmitter is capable of static bandwidth operation. DYN The transmitter is capable of dynamic bandwidth operation. OFF Dynamic bandwidth in Non HT is not present.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(dbi_nonht, enums.WlannFbDynBwInNonHt)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DBINonht {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbDynBwInNonHt:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DBINonht \n
		(available only for VHT Tx mode) Modifys the first 7 bits of the scrambling sequence to indicate if the transmitter is
		capable of 'Static' or 'Dynamic' bandwidth operation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: dbi_nonht: STAT| DYN| OFF STAT The transmitter is capable of static bandwidth operation. DYN The transmitter is capable of dynamic bandwidth operation. OFF Dynamic bandwidth in Non HT is not present."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DBINonht?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbDynBwInNonHt)
