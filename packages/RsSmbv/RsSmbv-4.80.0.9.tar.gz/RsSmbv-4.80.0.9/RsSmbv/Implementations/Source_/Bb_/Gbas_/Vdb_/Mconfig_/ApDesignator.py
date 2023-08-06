from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApDesignator:
	"""ApDesignator commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apDesignator", core, parent)

	def set(self, ap_per_des: enums.GbasAppPerDes, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:APDesignator \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the approach performance designator. \n
			:param ap_per_des: GAB| GC| GCD
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(ap_per_des, enums.GbasAppPerDes)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:APDesignator {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasAppPerDes:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:APDesignator \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the approach performance designator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: ap_per_des: GAB| GC| GCD"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:APDesignator?')
		return Conversions.str_to_scalar_enum(response, enums.GbasAppPerDes)
