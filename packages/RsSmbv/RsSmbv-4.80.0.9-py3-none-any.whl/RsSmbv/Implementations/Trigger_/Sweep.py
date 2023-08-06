from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def immediate(self):
		"""immediate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_immediate'):
			from .Sweep_.Immediate import Immediate
			self._immediate = Immediate(self._core, self._base)
		return self._immediate

	def set_source(self, source: enums.SingExtAuto) -> None:
		"""TRIGger<HW>:[SWEep]:SOURce \n
			INTRO_CMD_HELP: Selects the trigger source for the corresponding sweeps: \n
			- FSWeep - RF frequency
			- LFFSweep - LF frequency
			- PSWeep - RF level
			- SWEep - all sweeps
		The source names of the parameters correspond to the values provided in manual control of the instrument. They differ
		from the SCPI-compliant names, but the instrument accepts both variants. Use the SCPI name, if compatibility is an
		important issue. Find the corresponding SCPI-compliant commands in Cross-reference between the manual and remote control. \n
			:param source: AUTO| IMMediate | SINGle| BUS | EXTernal | EAUTo AUTO [IMMediate] Executes a sweep automatically. In this free-running mode, the trigger condition is met continuously. I.e. when a sweep is completed, the next one starts immediately. SINGle [BUS] Executes one complete sweep cycle. The following commands initiate a trigger event: *TRG method RsSmbv.Source.Sweep.Power.Execute.set EXECute :​TRIGgerhw[:​SWEep][:​IMMediate], method RsSmbv.Trigger.Sweep.Immediate.set and method RsSmbv.Trigger.Sweep.Immediate.set. Set the sweep mode with the commands: method RsSmbv.Source.Sweep.Power.Mode.valueAUTO|STEP MODEAUTO|STEP LFOutput:MODEAUTO|STEP In step mode (STEP) , the instrument executes only one step. EXTernal An external signal triggers the sweep. EAUTo An external signal triggers the sweep. When one sweep is finished, the next sweep starts. A second trigger event stops the sweep at the current frequency, a third trigger event starts the trigger at the start frequency, and so on.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SingExtAuto)
		self._core.io.write(f'TRIGger<HwInstance>:SWEep:SOURce {param}')
