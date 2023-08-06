from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HardCopy:
	"""HardCopy commands group definition. 17 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hardCopy", core, parent)

	def clone(self) -> 'HardCopy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HardCopy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .HardCopy_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	@property
	def file(self):
		"""file commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_file'):
			from .HardCopy_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def image(self):
		"""image commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_image'):
			from .HardCopy_.Image import Image
			self._image = Image(self._core, self._base)
		return self._image

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .HardCopy_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	def get_data(self) -> bytes:
		"""HCOPy:DATA \n
		Transfers the hard copy data directly as a NByte stream to the remote client. \n
			:return: data: block data
		"""
		response = self._core.io.query_bin_block('HCOPy:DATA?')
		return response

	# noinspection PyTypeChecker
	def get_region(self) -> enums.HcOpyRegion:
		"""HCOPy:REGion \n
		Selects the area to be copied. You can create a snapshot of the screen or an active dialog. \n
			:return: region: ALL| DIALog
		"""
		response = self._core.io.query_str('HCOPy:REGion?')
		return Conversions.str_to_scalar_enum(response, enums.HcOpyRegion)

	def set_region(self, region: enums.HcOpyRegion) -> None:
		"""HCOPy:REGion \n
		Selects the area to be copied. You can create a snapshot of the screen or an active dialog. \n
			:param region: ALL| DIALog
		"""
		param = Conversions.enum_scalar_to_str(region, enums.HcOpyRegion)
		self._core.io.write(f'HCOPy:REGion {param}')
