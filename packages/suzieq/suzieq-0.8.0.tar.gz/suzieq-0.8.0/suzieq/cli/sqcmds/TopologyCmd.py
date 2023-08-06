import time
import pandas as pd
from nubia import command, argument

from suzieq.cli.sqcmds.command import SqCommand
from suzieq.sqobjects.topology import TopologyObj


@command("topology", help="build and act on topology data")
class TopologyCmd(SqCommand):
    def __init__(
        self,
        engine: str = "",
        hostname: str = "",
        start_time: str = "",
        end_time: str = "",
        view: str = "latest",
        namespace: str = "",
        format: str = "",
        columns: str = "default",
    ) -> None:
        super().__init__(
            engine=engine,
            hostname=hostname,
            start_time=start_time,
            end_time=end_time,
            view=view,
            namespace=namespace,
            columns=columns,
            format=format,
            sqobj=TopologyObj
        )

    @command("show")
    @argument("polled_neighbor", description="Is the neighbor a device Suzieq polls")
    def show(self, polled_neighbor: bool = ''):
        """show table of topology information"""
        # Get the default display field names
        if self.columns is None:
            return

        now = time.time()
        if self.columns != ["default"]:
            self.ctxt.sort_fields = None
        else:
            self.ctxt.sort_fields = []

        try:
            df = self.sqobj.get(
                namespace=self.namespace, 
                polled_neighbor=polled_neighbor,
                hostname=self.hostname,
            )
        except Exception as e:
            df = pd.DataFrame({'error': ['ERROR: {}'.format(str(e))]})

        self.ctxt.exec_time = "{:5.4f}s".format(time.time() - now)
        if not df.empty:
            return self._gen_output(df)

    @command("summarize")
    @argument("polled_neighbor", description="Is the neighbor a device Suzieq polls")
    def summarize(self, src: str = "", dest: str = "", 
                    polled_neighbor: bool = ''):
        """Summarize topologys topology information"""
        # Get the default display field names
        if self.columns is None:
            return

        now = time.time()
        if self.columns != ["default"]:
            self.ctxt.sort_fields = None
        else:
            self.ctxt.sort_fields = []

        try:
            df = self.sqobj.summarize(
                namespace=self.namespace, 
                polled_neighbor=polled_neighbor
            )
        except Exception as e:
            df = pd.DataFrame({'error': ['ERROR: {}'.format(str(e))]})

        self.ctxt.exec_time = "{:5.4f}s".format(time.time() - now)
        if not df.empty:
            return self._gen_output(df)
        
    @command("unique", help="find the list of unique items in a column")
    def unique(self, **kwargs):

        msg = 'ERROR: Unique not supported for this object'
        df = pd.DataFrame({'error': [msg]})
        return self._gen_output(df, dont_strip_cols=True)