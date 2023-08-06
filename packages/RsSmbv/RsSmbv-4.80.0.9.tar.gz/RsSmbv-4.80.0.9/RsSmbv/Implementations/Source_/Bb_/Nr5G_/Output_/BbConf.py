from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BbConf:
	"""BbConf commands group definition. 7 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bbConf", core, parent)

	def clone(self) -> 'BbConf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BbConf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def row(self):
		"""row commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .BbConf_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row

	def get_conflict(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:BBConf:CONFlict \n
		Queries if there are existing output conflicts caused by mismatch between the nominal sample rate, playback rate and
		sample rate in all set output blocks. \n
			:return: any_outp_conflict: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:BBConf:CONFlict?')
		return Conversions.str_to_bool(response)
