from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SENSe<CH>:[POWer]:FILTer:LENGth:AUTO \n
		Queries the current filter length in filter mode AUTO (FILTer:TYPE) \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: auto: float Range: 1 to 65536"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:LENGth:AUTO?')
		return Conversions.str_to_float(response)
