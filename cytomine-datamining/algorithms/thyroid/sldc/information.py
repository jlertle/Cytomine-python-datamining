# -*- coding: utf-8 -*-

from timing import WorkflowTiming

__author__ = "Mormont Romain <romain.mormont@gmail.com>"
__version__ = "0.1"


class ChainInformation(object):
    """ Stores information gathered at various stages of execution of the workflow.
    """
    def __init__(self):
        self._runs = dict()
        self._next_id = 1
        self._image2ids = dict()

    def __len__(self):
        """Return the number of workflow info registered till then
        Returns
        -------
        count: int
            The number of workflow info registered
        """
        return len(self._runs)

    def get_workflow_info(self, id_workflow):
        """Return the workflow info having a given id
        Parameters
        ----------
        id_workflow: int
            The id of the workflow info object to get

        Returns
        -------
        run: WorkflowInformation
            The workflow info object
        """
        return self._runs[id_workflow]

    def register_workflow_info(self, workflow_info, image):
        """Register a new run to the execution information object
        Parameters
        ----------
        workflow_info: WorkflowInformation
            The workflow information object
        image: int
            A unique identifier for the image on which the workflow was executed

        Returns
        -------
        result: WorkflowInformation
            The workflow information object with its id set
        """
        workflow_info.id = self._next_id
        self._image2ids[workflow_info.id] = self._image2ids.get(image, []) + [workflow_info.id]
        self._runs[workflow_info.id] = workflow_info
        self._next_id += 1  # increment the next run id
        return workflow_info

    def register_workflow_collection(self, collection, image):
        """Register a new run to the execution information object
        Parameters
        ----------
        collection: WorkflowInformationCollection
            The collection of workflow information objects
        image: int
            A unique identifier for the image on which the workflow was executed
        """
        for workflow_info in collection:
            self.register_workflow_info(workflow_info, image)

    def get_workflow_infos_by_image(self, image):
        """Return all the workflow information objects registered for the given image
        Parameters
        ----------
        image: int
            The unique identifier of the image (used when the workflows were registered)

        Returns
        -------
        list: list of WorkflowInformation
            The workflow information objects registered for the given image
        """
        return WorkflowInformationCollection([self.get_workflow_info(id_workflow)
                                              for id_workflow in self._image2ids.get(image, [])])


class WorkflowInformation(object):
    """Workflow information : execution about a workflow run. A run is a complete execution
    (segment, locate, dispatch and classify) of a single workflow and comprises the following information :
        - id : runs are assigned unique ids as they are notified to the ChainInformation object)
        - polygons : the polygons generated by a given run
        - dispatch : list of which the ith element matches the index of the dispatching rule that matched
            the ith polygon, -1 if none did
        - class : list of which the ith integer is the class predicted by the classifier to
            which was dispatched the ith polygon, -1 if none did
        - probas : list of which the ith float (in [0,1]) is the probability of the ith predicted class if the
            corresponding polygon was dispatched, 0 if it wasn't dispatched
        - timing : the information about the execution time of the workflow
        - metadata : a comment from the implementor of the workflow to document how the previous data were generated
    """
    def __init__(self, polygons, dispatch, classes, probas, timing, id_workflow=None, metadata=""):
        """Construct a run object
        Parameters
        ----------
        polygons: list
            The polygons generated by the run
        dispatch: list
            Their dispatch indexes
        classes: list
            Their predicted classes
        probas: list
            The probabilities of the predicted classes
        timing: SLDCTiming
            Execution time information
        id_workflow: int, (optional, default: None)
            The run id, None if to assign it later
        metadata: string, (optional, default: "")
            String data/comment to associate with the workflow generated data
        """
        self._id = id_workflow
        self._polygons = polygons
        self._dispatch = dispatch
        self._classes = classes
        self._metadata = metadata
        self._timing = timing
        self._probas = probas

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def polygons(self):
        return self._polygons

    @property
    def dispatch(self):
        return self._dispatch

    @property
    def classes(self):
        return self._classes

    @property
    def probas(self):
        return self._probas

    @property
    def metadata(self):
        return self._metadata

    @property
    def timing(self):
        return self._timing

    def __iter__(self):
        self.iterator()

    def iterator(self, filter_dispatch=None, filter_classes=None):
        """Yields an iterator that goes through the list of polygons of the workflow information
        The result is a tuple containing in this order the polygon, the dispatch index and the class

        Parameters
        ----------
        filter_dispatch: list of int (optional, default: [-1])
            The dispatch indexes to exclude from the iterated list
        filter_classes: list of int (optional, default: [])
            The classes number to exclude from the iterated list
        """
        if filter_dispatch is None:
            filter_dispatch = [-1]
        for polygon, dispatch, cls, proba in zip(self.polygons, self.dispatch, self.classes, self.probas):
            if (filter_dispatch is None or dispatch not in filter_dispatch) and \
                    (filter_classes is None or cls not in filter_classes):
                yield polygon, dispatch, cls, proba
        return

    def merge(self, other):
        """Merge the other workflow information object into the current one. The id and metadata of the first are kept
        if they are set. Otherwise, the metadata and id of the other object are also merged

        Parameters
        ----------
        other: WorkflowInformation
            The workflow information object to merge
        """
        if other is None:
            return

        self._polygons += other.polygons
        self._dispatch += other.dispatch
        self._classes += other.classes
        self._timing = WorkflowTiming.merge_timings(self._timing, other.timing)

        if self._metadata is None:
            self._metadata = other.metadata
        if self._id is None:
            self._id = other.id


class WorkflowInformationCollection(object):
    """An collection for storing workflow information objects
    """
    def __init__(self, items=None):
        """
        Parameters
        ----------
        items: list of WorlflowInformation
            Object to insert in the list, if not provided the collection is initialized empty
        """
        self._items = items if items is not None else []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    def __setitem__(self, key, value):
        self._items[key] = value

    def __iter__(self):
        for item in self._items:
            yield item

    def append(self, value):
        """Append the workflow information at the end of the collection
        Parameters
        ----------
        value: WorkflowInformation
            The object to append
        """
        self._items.append(value)

    def polygons(self, filter_classes=None, filter_dispatch=None):
        """An iterator that goes through all the polygons stored in the collection
        The yielded value is a tuple containing the polygon, the dispatch index, the predicted
        class and the probability

        Parameters
        ----------
        filter_dispatch: list of int (optional, default: [-1])
            The dispatch indexes to exclude from the iterated list. By default unmatched polygon are excluded.
        filter_classes: list of int (optional, default: [])
            The classes number to exclude from the iterated list
        """
        for workflow_info in self._items:
            for polygon, dispatch, cls, proba in workflow_info.iterator(filter_classes=filter_classes,
                                                                        filter_dispatch=filter_dispatch):
                yield polygon, dispatch, cls, proba
        return
