from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Config:
	"""Config commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("config", core, parent)

	def set(self, auto_config_state: enums.AutoManualMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:CONFig \n
		Defines how noise bandwidth and noise center frequency are set. \n
			:param auto_config_state: AUTO| MANual AUTO Sets bandwidth and center frequency automatically. MANual Enables configuration of noise and CW parameters.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.enum_scalar_to_str(auto_config_state, enums.AutoManualMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:CONFig {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AutoManualMode:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:CONFig \n
		Defines how noise bandwidth and noise center frequency are set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: auto_config_state: AUTO| MANual AUTO Sets bandwidth and center frequency automatically. MANual Enables configuration of noise and CW parameters."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:CONFig?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)
