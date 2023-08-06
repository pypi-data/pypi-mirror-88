from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Predefined:
	"""Predefined commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("predefined", core, parent)

	def clone(self) -> 'Predefined':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Predefined(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Predefined_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	def load(self, filename: str, frameIx=repcap.FrameIx.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:PREDefined:LOAD \n
		This command loads the selected file with predefined frame settings. The directory is pre-set, therefore a path cannot be
		specified. \n
			:param filename: string
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')"""
		param = Conversions.value_to_quoted_str(filename)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:PREDefined:LOAD {param}')
