import abc
import logging
from collections import deque
from typing import List, Union

from flywheel_gear_toolkit.utils.datatypes import Container

log = logging.getLogger(__name__)


class Walker:
    """A class to walk the container hierarchically

    example usage:

    .. code-block:: python

        proj = fw.lookup('test/test_proj')
        proj_walker = walker.Walker(proj, depth_first=True)
        for container in proj.walk():
            if container.container_type == 'session':
                print('Found a session')
        proj = fw.lookup('test/test_proj')
    # TODO: demonstrate adding colletion to walker
    ```
    """

    def __init__(self, root: Container, depth_first: bool = True):
        """
        Args:
            root (Container):
                The root container, one of `flywheel.Project,flywheel.Subject, flywheel.Session, flywheel.Acquisition, flywheel.FileEntry, flywheel.AnalysisOutput`
            depth_first (bool): Depth first of breadth first traversal, True for depth first, False fo breadth first

        """
        self.deque = deque([root])
        self.depth_first = depth_first

    def next(self):
        """Returns the next element from the walker and adds its children.

        Returns:
            Container|FileEntry
        """
        if self.depth_first:
            next_element = self.deque.pop()
        else:
            next_element = self.deque.popleft()

        log.debug(f"Element returned is {next_element.container_type}")

        self.queue_children(next_element)

        return next_element

    def add(self, element: Union[List[Container], Container]):
        """Adds an element to the walker.

        Args:
            element (List[Container] or Container): Element or list of elements to add to deque
        """
        try:
            self.deque.extend(element)
        except TypeError:
            # element not an iterable
            self.deque.append(element)
        except AttributeError:
            #
            self.deque.append(element)

    def queue_children(self, element: Container):
        """Returns children of the element.

        Args:
            element (Container): contianer to find children of.

        Returns:
            list: the children of the element
        """
        container_type = element.container_type

        # No children of files
        if container_type == "file":
            return

        log.info(f"Queueing children for container {element.label or element.code}")

        self.deque.extend(element.files or [])

        # Make sure that the analyses attribute is a list before iterating
        if container_type != "analysis" and isinstance(element.analyses, list):
            # TODO: Determine what containers have non-list element.analyses
            self.deque.extend(element.analyses)
            if container_type == "project":
                self.deque.extend(element.subjects())
            elif container_type == "subject":
                self.deque.extend(element.sessions())
            elif container_type == "session":
                self.deque.extend(element.acquisitions())

    def is_empty(self):
        """Returns True if the walker is empty.

        Returns:
            bool
        """
        return len(self.deque) == 0

    def walk(self):
        """Walks the hierarchy from a root container.

        Yields:
            Container|FileEntry
        """

        while not self.is_empty():
            yield self.next()
