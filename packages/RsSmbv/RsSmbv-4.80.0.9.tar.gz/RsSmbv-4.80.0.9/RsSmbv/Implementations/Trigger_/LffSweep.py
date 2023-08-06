from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LffSweep:
	"""LffSweep commands group definition. 4 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lffSweep", core, parent)

	def clone(self) -> 'LffSweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LffSweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .LffSweep_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_source'):
			from .LffSweep_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	def set(self) -> None:
		"""TRIGger<HW>:LFFSweep \n
			INTRO_CMD_HELP: Executes an LF frequency sweep in the following configuration: \n
			- method RsSmbv.Trigger.LffSweep.Source.value SING
			- method RsSmbv.Source.LfOutput.Sweep.Frequency.Mode.value AUTO \n
		"""
		self._core.io.write(f'TRIGger<HwInstance>:LFFSweep')

	def set_with_opc(self) -> None:
		"""TRIGger<HW>:LFFSweep \n
			INTRO_CMD_HELP: Executes an LF frequency sweep in the following configuration: \n
			- method RsSmbv.Trigger.LffSweep.Source.value SING
			- method RsSmbv.Source.LfOutput.Sweep.Frequency.Mode.value AUTO \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'TRIGger<HwInstance>:LFFSweep')
