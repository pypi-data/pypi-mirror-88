from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CdmType:
	"""CdmType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cdmType", core, parent)

	def set(self, cdm_type: enums.EutraCsiRsCdmType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:CDMType \n
		Sets the higher-level parameter CDMType that influence the antenna port mapping of the CSI-RS. \n
			:param cdm_type: 2| 4| 8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(cdm_type, enums.EutraCsiRsCdmType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:CDMType {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraCsiRsCdmType:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSIS:[CELL<CH>]:CDMType \n
		Sets the higher-level parameter CDMType that influence the antenna port mapping of the CSI-RS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: cdm_type: 2| 4| 8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:CSIS:CELL{channel_cmd_val}:CDMType?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCsiRsCdmType)
