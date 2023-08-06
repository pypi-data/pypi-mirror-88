from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Point:
	"""Point commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("point", core, parent)

	def clone(self) -> 'Point':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Point(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def configuration(self):
		"""configuration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_configuration'):
			from .Point_.Configuration import Configuration
			self._configuration = Configuration(self._core, self._base)
		return self._configuration

	def get_catalog(self) -> List[str]:
		"""DIAGnostic<HW>:POINt:CATalog \n
		Queries the test points available in the instrument. For more information, see R&S SMBV100B Service Manual. \n
			:return: catalog: string List of comma-separated values, each representing a test point
		"""
		response = self._core.io.query_str('DIAGnostic<HwInstance>:POINt:CATalog?')
		return Conversions.str_to_str_list(response)
