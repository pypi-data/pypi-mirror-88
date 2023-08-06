from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def set(self, structure: PatternStruct, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:PATTern \n
		A marker signal that is defined by a bit pattern is generated. \n
			:param structure: for set value, see the help for PatternStruct structure arguments.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write_struct(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:PATTern', structure)

	def get(self, channel=repcap.Channel.Default) -> PatternStruct:
		"""[SOURce<HW>]:BB:NFC:TRIGger:OUTPut<CH>:PATTern \n
		A marker signal that is defined by a bit pattern is generated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: structure: for return value, see the help for PatternStruct structure arguments."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		return self._core.io.query_struct(f'SOURce<HwInstance>:BB:NFC:TRIGger:OUTPut{channel_cmd_val}:PATTern?', self.__class__.PatternStruct())
