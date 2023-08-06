from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, datasource: enums.C5Gds, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:DATA \n
		Selects the data source for the selected allocation. \n
			:param datasource: USER1| USER2| USER3| USER4| PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE| USER5| USER0
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(datasource, enums.C5Gds)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:DATA {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.C5Gds:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:DATA \n
		Selects the data source for the selected allocation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: datasource: USER1| USER2| USER3| USER4| PN9| PN11| PN15| PN16| PN20| PN21| PN23| PATTern| DLISt| ZERO| ONE| USER5| USER0"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.C5Gds)
