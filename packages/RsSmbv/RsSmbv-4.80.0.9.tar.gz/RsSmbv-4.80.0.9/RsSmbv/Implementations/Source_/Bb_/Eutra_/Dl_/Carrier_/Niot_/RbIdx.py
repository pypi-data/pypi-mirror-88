from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RbIdx:
	"""RbIdx commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rbIdx", core, parent)

	def set(self, rb_index: enums.EutraDlNbiotRbIndex, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:RBIDx \n
		Sets the resource block number in that the NB-IoT transmissions are allocated. \n
			:param rb_index: 2| 4| 7| 9| 12| 14| 17| 19| 22| 27| 24| 29| 30| 32| 34| 35| 39| 42| 44| 40| 45| 47| 52| 55| 57| 60| 62| 65| 67| 70| 72| 75| 80| 85| 90| 95| USER
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.enum_scalar_to_str(rb_index, enums.EutraDlNbiotRbIndex)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:RBIDx {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDlNbiotRbIndex:
		"""[SOURce<HW>]:BB:EUTRa:DL:CARRier<CH>:NIOT:RBIDx \n
		Sets the resource block number in that the NB-IoT transmissions are allocated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: rb_index: 2| 4| 7| 9| 12| 14| 17| 19| 22| 27| 24| 29| 30| 32| 34| 35| 39| 42| 44| 40| 45| 47| 52| 55| 57| 60| 62| 65| 67| 70| 72| 75| 80| 85| 90| 95| USER"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CARRier{channel_cmd_val}:NIOT:RBIDx?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDlNbiotRbIndex)
