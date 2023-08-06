from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bfsdd:
	"""Bfsdd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bfsdd", core, parent)

	def set(self, bf_sdd: enums.NfcBitFrmSdd, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BFSDd \n
		Determines Bit frame SDD. \n
			:param bf_sdd: SDD0| SDD2| SDD1| SDD4| SDD8| SDD16
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(bf_sdd, enums.NfcBitFrmSdd)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BFSDd {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcBitFrmSdd:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:BFSDd \n
		Determines Bit frame SDD. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: bf_sdd: SDD0| SDD2| SDD1| SDD4| SDD8| SDD16"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:BFSDd?')
		return Conversions.str_to_scalar_enum(response, enums.NfcBitFrmSdd)
