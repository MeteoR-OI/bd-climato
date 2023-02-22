"""
    Later: need to call only api methods
    sdk (implementation) will be loaded with env variables
    But not fully available at the time of coding
    Then telemetry call directly sdk methods
    And a no-telemetry mode was coded too..

    start jaeger:
        docker run -d --name jaeger \
        -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
        -p 5775:5775/udp \
        -p 6831:6831/udp \
        -p 6832:6832/udp \
        -p 5778:5778 \
        -p 16686:16686 \
        -p 14250:14250 \
        -p 14268:14268 \
        -p 14269:14269 \
        -p 9411:9411 \
        jaegertracing/all-in-one

        start loki:
        d run -d --name loki -v $(pwd):/mnt/config -p 3100:3100 grafana/loki -config.file=/mnt/config/loki-config.yaml

    start promtail:
        docker run -d --name promtail \
        -v $(pwd):/mnt/config \
        -v /var/log:/mnt/log \
        -v /tmp:/mnt/tmp \
        -v /home/meteor/bd-climato/data/localStorage/log:/mnt/django \
        grafana/promtail \
        -config.file=/mnt/config/promtail-config.yaml
"""
from django.conf import settings
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.trace.span import Span
import app.tools.myTools as t
import json


class SpanStatus:
    _status_code = 0


class ContextMok:
    """
    ContextMok
        Mok class to simulate context class when no telemetry is used
    """
    trace_id = "012345"
    span_id = "567890"


class SpanMok:
    """
    SpanMok
        Mok class to simulate Span class when no telemetry is used
    """

    def __init__(self, name: str, parent_span, tracer):
        """
            __init__

            Parameters:
                name: span name
                parent_span
        """
        if hasattr(settings, "TELEMETRY") is True and settings.TELEMETRY is True:
            raise Exception("SpanMok", "Calling Mok while telemetry is active")
        self.name = name
        self.parent = parent_span
        self.atts = []
        self.events = []
        self.child_data = []
        self._status = SpanStatus()
        self.ctx = ContextMok()
        self.printed = False
        self.tracer = tracer

    def end(self):
        """
        __exit__

        end of a with statement. print out data if no telemetry is used
        """
        if self.printed is True:
            return
        self.printed = True
        self.tracer.current_span = self.parent
        if self.parent is not None:
            self.parent.child_data.append({
                'name': self.name,
                'events': self.events,
                'atts': self.atts,
                'child_data': self.child_data,
            })
        else:
            self.print_span("", self.name, self.atts, self.events)
            self.print_childs(self.child_data)
            self.a_child_data = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()

    def __end__(self):
        """
        __end__

        Not sure if this method is called...
        """
        self.end()
        return

    def print_childs(self, child_data, prefix="  "):
        for a_child in child_data:
            self.print_span(prefix, a_child['name'], a_child['atts'], a_child['events'])
            if len(a_child['child_data']) > 0:
                self.print_childs(a_child['child_data'], prefix + "  ")

    def print_span(self, prefix, name, atts, events):
        if len(prefix) == 0:
            print(prefix + "Span: " + name)
        else:
            print(prefix + "Sub Span: " + name)
            
        if len(atts) > 0:
            print_out = prefix + "  attributes:"
            print(print_out)
            sub_prefix = " " * len(print_out)
            print_out = sub_prefix
            count = 0
            for an_att in atts:
                count += 1
                if count > 3:
                    print(print_out)
                    print_out = sub_prefix
                    count = 0
                print_out += str(an_att["k"]) + ": " + str(an_att["v"]) + ", "
            print(print_out)
        if len(events) > 0:
            print_out = prefix + "  events:"
            print(print_out)
            sub_prefix = " " * len(print_out)
            for an_att in events:
                print(sub_prefix + str(an_att["en"]) + ": " + str(an_att["e"]))

    def record_exception(self, exc: Exception):
        """
        record_exception
            add an exception in the Span
        """
        t.logException(exc, self)
        return

    def set_attribute(self, k: str, v):
        """
        set_attribute
            Add an attribute in the span
        """
        if k == "file_processed":
            v = str(v).split("/")[-1::1][0]
        self.atts.append({"k": k, "v": v})

    def add_event(self, event_name: str, j_val: json):
        """
        add_event
            Add event in the span
        """
        self.events.append({"en": event_name, "e": j_val})

    def get_span_context(self):
        return self.ctx


class TracerMok:
    """
    TracerMok   Call the real tracer, or our Mok implementation
    """

    def __init__(self):
        self.current_span = None

    def __enter__(self):
        return self

    def __end__(self):
        self.end_span()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_span()

    def end_span(self):
        # self.clean_future_attribute()
        if self.current_span is not None:
            self.current_span.end()

    def get_current_or_new_span(self, name: str = "???"):
        """
        get_current_or_new_span
            Get current span if one is active, or start a new one

        Parameter:
            name: span name (only used if a new span is started)
        """
        self.current_span = SpanMok(name, self.current_span, self)
        return self.current_span

    def start_as_current_span(self, span_name: str = "???") -> Span:
        """
        start_as_current_span
            start a new Span, child of the current Span

        Parameter:
            name: span name
        """
        self.current_span = SpanMok(span_name, self.current_span, self)
        return self.current_span

    def start_span(self, span_name: str = "???") -> Span:
        """
        start_span
            start a new span

        Parameter:
            name: span name
        """
        self.current_span = SpanMok(span_name, None, self)
        return self.current_span

    def get_span_context(self):
        if self.current_span is None:
            return ContextMok()
        return self.current_span.get_span_context()


class Telemetry:
    """
        static class to activate telemetry in a module
    """
    tracer: Tracer = None

    @staticmethod
    def get_ok_status():
        return trace.StatusCode.OK

    @staticmethod
    def get_error_status():
        return trace.StatusCode.ERROR

    @staticmethod
    def get_kind_server():
        return trace.SpanKind.SERVER

    @staticmethod
    def Start(service_name: str, caller_name: str = __name__):
        """
        Start
            Activate telemetry

        Parameters:
            service_name
            called_name (use __name__ in caller)
        """
        if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
            return TracerMok()

        if Telemetry.tracer is None:
            if hasattr(settings, "TELEMETRY_PROVIDER") is True:
                resource = Resource(attributes={
                    SERVICE_NAME: "Climato"
                })
                provider = TracerProvider(resource=resource)

                if settings.TELEMETRY_PROVIDER == "Thrift":
                    telemetry_host = "localhost" if hasattr(settings, "TELEMETRY_HOST") is False else settings.TELEMETRY_HOST
                    thrift_port = 14250 if hasattr(settings, "THRIFT_PORT") is False else settings.THRIFT_PORT
                    thrift_exporter = JaegerExporter(
                        agent_host_name=telemetry_host,
                        agent_port=thrift_port,
                        collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
                    )
                    processor = BatchSpanProcessor(thrift_exporter)
                    provider.add_span_processor(processor)
                    trace.set_tracer_provider(provider)
                    trace.get_tracer_provider().add_span_processor(processor)

                elif settings.TELEMETRY_PROVIDER == "Jaeger":
                    jaeger_port = 14250 if hasattr(settings, "JAEGER_PORT") is False else settings.JAEGER_PORT
                    jaeger_exporter = JaegerExporter(
                        agent_host_name=telemetry_host,
                        agent_port=jaeger_port,
                    )
                    processor = BatchSpanProcessor(jaeger_exporter)
                    trace.get_tracer_provider().add_span_processor(processor)

                else:
                    processor = BatchSpanProcessor(ConsoleSpanExporter())
                    trace.get_tracer_provider().add_span_processor(processor)

            else:
                processor = BatchSpanProcessor(ConsoleSpanExporter())
                trace.get_tracer_provider().add_span_processor(processor)

            Telemetry.tracer = trace.get_tracer(__name__)

        return Telemetry.tracer
