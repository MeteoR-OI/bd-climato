# from django.db import transaction
# from app.tools.jsonPlus import JsonPlus
import json

from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto import grpc
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from app.tools.climConstant import TelemetryConf
from opentelemetry.trace.span import INVALID_SPAN, Span
from opentelemetry.trace.propagation import get_current_span
import app.tools.myTools as t
from django.conf import settings


class ContextMok:
    trace_id = None


class SpanMok:
    ctx = ContextMok()

    def __init__(self, name: str = "???", trace_flag: bool = None):
        if hasattr(settings, 'TELEMETRY') is True and settings.TELEMETRY is True:
            raise Exception('SpanMok', 'Calling Mok while telemetry is active')
        self.name = name
        self.trace = trace_flag
        self.atts = []
        self.events = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.trace is False:
            return
        print("Span: " + self.name)
        print_out = ""
        for an_att in self.atts:
            print_out += (str(an_att['k']) + ': ' + str(an_att['v']) + ', ')
        self.atts = []
        if print_out.__len__() > 2:
            print('     attributes: ' + print_out[0:-2])
            print_out = ""
        for an_att in self.events:
            print_out += (str(an_att['en']) + ': ' + str(an_att['e']) + ', ')
        self.atts = []
        if print_out.__len__() > 2:
            print('     events: ' + print_out[0:-2])
            print_out = ""
        return

    def __end__(self):
        self.__exit__(1, 2, 3)
        return

    def end(self):
        self.__exit__(1, 2, 3)
        return

    def record_exception(self, exc: Exception):
        t.LogException(exc, self, 2)
        return

    def set_attribute(self, k: str, v):
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            if k == "file_processed":
                v = str(v).split("/")[-1::1][0]
            self.atts.append({"k": k, "v": v})
        return

    def add_event(self, event_name: str, j_val: json):
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            self.events.append({"en": event_name, "e": j_val})
        return

    def get_span_context(self):
        return self.ctx


class TracerTriage:
    def __init__(self, tracer: Tracer = None):
        self.current_span = None
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            self.real_tracer = self
        else:
            if tracer is None:
                raise Exception('TracerTriage', 'no tracer given')
            self.real_tracer = tracer

    def __enter__(self):
        return self

    def __end__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current_span = None
        return

    def get_current_or_new_span(self, name: str = "???", trace_flag: bool = None):
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            if self.current_span is None:
                return SpanMok(name)
            return self.current_span
        else:
            tmp_span = get_current_span()
            if tmp_span == INVALID_SPAN:
                tmp_span = self.start_as_current_span(name, trace_flag)
            return tmp_span

    def start_as_current_span(self, span_name: str, trace_flag: bool = None) -> Span:
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            self.current_span = SpanMok(span_name, trace_flag)
            self.trace = trace_flag
            if trace_flag is None:
                print('   ** trace_flag is None')
            return self.current_span
        else:
            return self.real_tracer.start_as_current_span(span_name)

    def start_span(self, span_name: str, trace_flag: bool = None) -> Span:
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            self.current_span = SpanMok(span_name, trace_flag)
            self.trace = trace_flag
            if trace_flag is None:
                print('   ** trace_flag is None')
            return self.current_span
        else:
            return self.real_tracer.start_span(span_name)


class Telemetry:
    tracer: Tracer = None

    @staticmethod
    def Start(service_name: str, caller_name: str = __name__):
        if Telemetry.tracer is None:
            if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
                return TracerTriage()

            trace.set_tracer_provider(
                TracerProvider(
                    resource=Resource.create({SERVICE_NAME: "django6"})
                    # resource=Resource.create({SERVICE_NAME: service_name})
                )
            )
            tracer = trace.get_tracer(__name__)

            # Create a JaegerExporter to send spans with gRPC
            # If there is no encryption or authentication set `insecure` to True
            # If server has authentication with SSL/TLS you can set the
            # parameter credentials=ChannelCredentials(...) or the environment variable
            # `EXPORTER_JAEGER_CERTIFICATE` with file containing creds.

            jaeger_exporter = grpc.JaegerExporter(
                collector_endpoint=TelemetryConf.get("collector"),
                insecure=TelemetryConf.get('insecure')
            )

            # create a BatchSpanProcessor and add the exporter to it
            span_processor = BatchSpanProcessor(jaeger_exporter)

            # add to the tracer factory
            trace.get_tracer_provider().add_span_processor(span_processor)
            Telemetry.tracer = tracer

        return TracerTriage(Telemetry.tracer)
