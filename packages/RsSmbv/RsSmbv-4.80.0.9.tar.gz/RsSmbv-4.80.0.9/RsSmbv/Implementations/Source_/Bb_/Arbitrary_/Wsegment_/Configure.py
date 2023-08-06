from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 14 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configure", core, parent)

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def blank(self):
		"""blank commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_blank'):
			from .Configure_.Blank import Blank
			self._blank = Blank(self._core, self._base)
		return self._blank

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_clock'):
			from .Configure_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Configure_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_marker'):
			from .Configure_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def segment(self):
		"""segment commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_segment'):
			from .Configure_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:CATalog \n
		Queries the available configuration files in the default directory. See also 'File Concept'. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_comment(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:COMMent \n
		Enters a comment for the selected configuration file. \n
			:return: comment: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:COMMent?')
		return trim_str_response(response)

	def set_comment(self, comment: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:COMMent \n
		Enters a comment for the selected configuration file. \n
			:param comment: string
		"""
		param = Conversions.value_to_quoted_str(comment)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:COMMent {param}')

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:DELete \n
		Deletes the selected configuration file. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:DELete {param}')

	def get_ofile(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:OFILe \n
		Defines the file name of the output multi-segment waveform. \n
			:return: ofile: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:OFILe?')
		return trim_str_response(response)

	def set_ofile(self, ofile: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:OFILe \n
		Defines the file name of the output multi-segment waveform. \n
			:param ofile: string
		"""
		param = Conversions.value_to_quoted_str(ofile)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:OFILe {param}')

	def get_select(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SELect \n
		Selects a configuration file from the default directory. If a configuration file with the specified name does not yet
		exist, it is created. The file extension *.inf_mswv may be omitted. \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:SELect \n
		Selects a configuration file from the default directory. If a configuration file with the specified name does not yet
		exist, it is created. The file extension *.inf_mswv may be omitted. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:SELect {param}')
