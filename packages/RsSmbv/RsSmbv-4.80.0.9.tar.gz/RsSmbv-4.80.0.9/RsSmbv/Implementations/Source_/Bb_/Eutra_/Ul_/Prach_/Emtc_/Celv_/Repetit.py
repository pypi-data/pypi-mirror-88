from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetit:
	"""Repetit commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repetit", core, parent)

	def set(self, repetitions: enums.EutraRepetitionsNbiot, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:REPetit \n
		Sets the PRACH number of repetitions. \n
			:param repetitions: R1| R2| R4| R8| R16| R32| R64| R128
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')"""
		param = Conversions.enum_scalar_to_str(repetitions, enums.EutraRepetitionsNbiot)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:REPetit {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraRepetitionsNbiot:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:EMTC:CELV<CH>:REPetit \n
		Sets the PRACH number of repetitions. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Celv')
			:return: repetitions: R1| R2| R4| R8| R16| R32| R64| R128"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:EMTC:CELV{channel_cmd_val}:REPetit?')
		return Conversions.str_to_scalar_enum(response, enums.EutraRepetitionsNbiot)
