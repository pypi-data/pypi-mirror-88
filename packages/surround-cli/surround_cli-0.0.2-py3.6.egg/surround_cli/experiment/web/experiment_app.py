import os
import tornado.web

from ..experiment_reader import ExperimentReader
from ..experiment_writer import ExperimentWriter
from .project_explorer import ProjectExplorer
from .experiment_explorer import ExperimentExplorer
from .results import Results
from .delete import Delete
from .view_logs import ViewLogs
from .edit_notes import EditNotes
from .download import Download
from .getter_experiment import GetterExperiment

class ExperimentApp(tornado.web.Application):
    def __init__(self, storage_url=None):
        reader = ExperimentReader(storage_url)
        writer = ExperimentWriter(storage_url)

        handlers = [
            (r'/', ProjectExplorer, {'experiment_reader': reader}),
            (r'/experiment', ExperimentExplorer, {'experiment_reader': reader}),
            (r'/results', Results, {'experiment_reader': reader}),
            (r'/view_logs', ViewLogs, {'experiment_reader': reader}),
            (r'/delete', Delete, {'experiment_reader': reader, 'experiment_writer': writer}),
            (r'/notes', EditNotes, {'experiment_reader': reader, 'experiment_writer': writer}),
            (r'/download', Download, {'experiment_reader': reader}),
            (r'/(favicon.ico|[a-z_]+\.js)', tornado.web.StaticFileHandler, {"path": os.path.dirname(__file__)}),
            (r'/getter/experiment', GetterExperiment, {'experiment_reader': reader})
        ]

        tornado.web.Application.__init__(self, handlers)
