import time
import logging
from res.job_queue import JobStatusType
from res.job_queue import ForwardModelStatus
from res.util import ResLog
from ecl.util.util import BoolVector
from ert_shared import ERT

# A method decorated with the @job_queue decorator implements the following logic:
#
# 1. If self._job_queue is assigned a valid value the method is run normally.
# 2. If self._job_queue is None - the decorator argument is returned.

def job_queue(default):

    def job_queue_decorator(method):

        def dispatch(self , *args, **kwargs):

            if self._job_queue is None:
                return default
            else:
                return method( self, *args , **kwargs)

        return dispatch

    return job_queue_decorator


class ErtRunError(Exception):
    pass

class BaseRunModel(object):

    def __init__(self, queue_config, phase_count=1):
        super(BaseRunModel, self).__init__()
        self._phase = 0
        self._phase_count = phase_count
        self._phase_name = "Starting..."

        self._job_start_time  = 0
        self._job_stop_time = 0
        self._indeterminate = False
        self._fail_message = ""
        self._failed = False
        self._queue_config = queue_config
        self._job_queue = None
        self.realization_progress = {}
        self.initial_realizations_mask = []
        self.completed_realizations_mask = []
        self.support_restart = True
        self._run_context = None
        self._last_run_iteration = -1
        self.reset( )

    def ert(self):
        """ @rtype: res.enkf.EnKFMain"""
        return ERT.ert

    @property
    def _ensemble_size(self):
        return self.initial_realizations_mask.count(True)

    def reset(self):
        self._failed = False


    def startSimulations(self, arguments):
        try:
            self.initial_realizations_mask = arguments["active_realizations"]
            run_context = self.runSimulations(arguments)
            self.updateDetailedProgress()
            self.completed_realizations_mask = run_context.get_mask()
        except ErtRunError as e:
            self.completed_realizations_mask = BoolVector(default_value = False)
            self._failed = True
            self._fail_message = str(e)
            self._simulationEnded()
        except UserWarning as e:
            self._fail_message = str(e)
            self._simulationEnded()

        self._run_context = None #delete last active run_context to notify fs_manager that storage is not being written to

    def runSimulations(self, job_queue, run_context):
        raise NotImplementedError("Method must be implemented by inheritors!")


    def create_context(self, arguments):
        raise NotImplementedError("Method must be implemented by inheritors!")


    @job_queue(None)
    def killAllSimulations(self):
        self._job_queue.kill_all_jobs()


    @job_queue(False)
    def userExitCalled(self):
        """ @rtype: bool """
        return self._job_queue.getUserExit( )


    def phaseCount(self):
        """ @rtype: int """
        return self._phase_count


    def setPhaseCount(self, phase_count):
        self._phase_count = phase_count
        self.setPhase(0, "")


    def currentPhase(self):
        """ @rtype: int """
        return self._phase


    def setPhaseName(self, phase_name, indeterminate=None):
        self._phase_name = phase_name
        self.setIndeterminate(indeterminate)


    def getPhaseName(self):
        """ @rtype: str """
        return self._phase_name


    def setIndeterminate(self, indeterminate):
        if indeterminate is not None:
            self._indeterminate = indeterminate


    def isFinished(self):
        """ @rtype: bool """
        return self._phase == self._phase_count or self.hasRunFailed()


    def hasRunFailed(self):
        """ @rtype: bool """
        return self._failed


    def getFailMessage(self):
        """ @rtype: str """
        return self._fail_message


    def _simulationEnded(self):
        self._job_stop_time = int(time.time())


    def setPhase(self, phase, phase_name, indeterminate=None):
        self.setPhaseName(phase_name)
        if not 0 <= phase <= self._phase_count:
            raise ValueError("Phase must be an integer from 0 to less than %d." % self._phase_count)

        self.setIndeterminate(indeterminate)

        if phase == 0:
            self._job_start_time = int(time.time())

        if phase == self._phase_count:
            self._simulationEnded()

        self._phase = phase

    def stop_time(self):
        return self._job_stop_time

    def start_time(self):
        return self._job_start_time

    @job_queue(1)
    def getQueueSize(self):
        """ @rtype: int """
        queue_size = len(self._job_queue)

        if queue_size == 0:
            queue_size = 1

        return queue_size

    @job_queue({})
    def getQueueStatus(self):
        """ @rtype: dict of (JobStatusType, int) """
        queue_status = {}

        for job_number in range(len(self._job_queue)):
            status = self._job_queue.getJobStatus(job_number)

            if not status in queue_status:
                queue_status[status] = 0

            queue_status[status] += 1

        return queue_status

    @job_queue(False)
    def isQueueRunning(self):
        """ @rtype: bool """
        return self._job_queue.isRunning()

    @staticmethod
    def is_forward_model_finished(progress):
        return not (any((job.status != 'Success' for job in progress)))

    def update_progress_for_index(self, iteration, idx, run_arg):
        if not self._run_context.is_active(idx):
            return
        try:
            # will throw if not yet submitted (is in a limbo state)
            queue_index = run_arg.getQueueIndex()
        except ValueError:
            return

        status = None
        if self._job_queue:
            status = self._job_queue.getJobStatus(queue_index)

        if status in [
                JobStatusType.JOB_QUEUE_PENDING,
                JobStatusType.JOB_QUEUE_SUBMITTED,
                JobStatusType.JOB_QUEUE_WAITING
                ]:
            return

        fms = self.realization_progress[iteration].get(run_arg.iens, None)

        #Dont load from file if you are finished
        if fms and BaseRunModel.is_forward_model_finished(fms[0]):
            jobs = self.realization_progress[iteration][run_arg.iens][0]
        else:
            fms = ForwardModelStatus.load(run_arg.runpath, num_retry=1)
            if not fms:
                return

            jobs = fms.jobs
        self.realization_progress[iteration][run_arg.iens] = jobs, status


    @job_queue({})
    def updateDetailedProgress(self):
        if not self._run_context:
            return

        iteration = self._run_context.get_iter()
        if iteration not in self.realization_progress:
            self.realization_progress[iteration] = {}

        try:
            # Run context might be set to None by concurrent threads,
            # which will results in an Attribute Error
            for idx, run_arg in enumerate(self._run_context):
                self.update_progress_for_index(iteration, idx, run_arg)
        except AttributeError as e:
            if self._run_context is None:
                logging.debug(
                    "Ignoring exception in run model (run_context is None): {}".format(
                        str(e)
                    )
                )
            else:
                raise

    def getDetailedProgress(self):
        self.updateDetailedProgress()

        if self._run_context and self._run_context.get_iter() in self.realization_progress:
            return self.realization_progress, self._run_context.get_iter()

        elif self._last_run_iteration in self.realization_progress:
            return self.realization_progress, self._last_run_iteration

        else:
            return {}, -1

    def isIndeterminate(self):
        """ @rtype: bool """
        return not self.isFinished() and self._indeterminate

    def checkHaveSufficientRealizations(self, num_successful_realizations):
        if num_successful_realizations == 0:
            raise ErtRunError("Simulation failed! All realizations failed!")
        elif not self.ert().analysisConfig().haveEnoughRealisations(num_successful_realizations, self._ensemble_size):
            raise ErtRunError("Too many simulations have failed! You can add/adjust MIN_REALIZATIONS to allow failures in your simulations.\n\n"
                              "Check ERT log file '%s' or simulation folder for details." % ResLog.getFilename())

    def checkMinimumActiveRealizations(self, run_context):
        active_realizations = self.count_active_realizations( run_context )
        if not self.ert().analysisConfig().haveEnoughRealisations(active_realizations, self._ensemble_size):
            raise ErtRunError("Number of active realizations is less than the specified MIN_REALIZATIONS in the config file")

    def count_active_realizations(self, run_context):
        return sum(run_context.get_mask( ))
