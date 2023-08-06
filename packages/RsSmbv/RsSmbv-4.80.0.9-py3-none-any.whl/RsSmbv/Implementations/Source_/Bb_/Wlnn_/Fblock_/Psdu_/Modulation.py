from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.ModulationF:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:PSDU:MODulation \n
		(available only for CCK and PBCC Tx modes) Queries the modulation type. The modulation mode depends on the selected PSDU
		bit rate which depends on the selected physical layer mode (SOUR:BB:WLNN:MODE) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: modulation: BPSK| QPSK| DBPSK| DQPSK| CCK| PBCC"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PSDU:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationF)
