from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Content:
	"""Content commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("content", core, parent)

	def set(self, content_type: enums.C5GcontentType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:CONTent \n
		Sets the content type. \n
			:param content_type: DATA| PREamble| PILot| REServed DATA Default value for FBMC and GFDM modulations. PREamble Default value for the first allocation of the UFMC modulation. DATA|PILot|REServed Selects the content type for f-OFDM/OFDM modulations.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(content_type, enums.C5GcontentType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:CONTent {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.C5GcontentType:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:CONTent \n
		Sets the content type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: content_type: DATA| PREamble| PILot| REServed DATA Default value for FBMC and GFDM modulations. PREamble Default value for the first allocation of the UFMC modulation. DATA|PILot|REServed Selects the content type for f-OFDM/OFDM modulations."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:CONTent?')
		return Conversions.str_to_scalar_enum(response, enums.C5GcontentType)
