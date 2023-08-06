from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duplexing:
	"""Duplexing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duplexing", core, parent)

	def set(self, duplexing: enums.EutraDuplexMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:DUPLexing \n
		Defines the duplexing mode for a UL/DL pattern containing a marker. \n
			:param duplexing: TDD| FDD TDD Sets TDD (time division duplex) as the duplexing mode. FDD Sets FDD (frequency division duplex) as the duplexing mode.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(duplexing, enums.EutraDuplexMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDuplexMode:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:DUPLexing \n
		Defines the duplexing mode for a UL/DL pattern containing a marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: duplexing: TDD| FDD TDD Sets TDD (time division duplex) as the duplexing mode. FDD Sets FDD (frequency division duplex) as the duplexing mode."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)
