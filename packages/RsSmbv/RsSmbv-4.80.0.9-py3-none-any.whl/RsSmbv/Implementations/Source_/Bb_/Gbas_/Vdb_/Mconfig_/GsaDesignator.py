from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GsaDesignator:
	"""GsaDesignator commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gsaDesignator", core, parent)

	def set(self, gsad: enums.GbasGrdStAcDes, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GSADesignator \n
		Sets the ground station accuracy designator. \n
			:param gsad: GADA| GADB| GADC
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(gsad, enums.GbasGrdStAcDes)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GSADesignator {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasGrdStAcDes:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:GSADesignator \n
		Sets the ground station accuracy designator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: gsad: GADA| GADB| GADC"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:GSADesignator?')
		return Conversions.str_to_scalar_enum(response, enums.GbasGrdStAcDes)
