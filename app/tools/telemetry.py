import json

from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto import grpc
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from app.tools.climConstant import TelemetryConf
from opentelemetry.trace.propagation import get_current_span, Span
from django.conf import settings


class ContextMok:
    span_id = None


class SpanMok:
    ctx = ContextMok()

    def __init__(self):
        if hasattr(settings, 'TELEMETRY') is True and settings.TELEMETRY is True:
            raise Exception('SpanMok', 'Calling Mok while telemetry is active')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def __end__(self):
        return

    def end(self):
        return

    def record_exception(exc: Exception):
        return

    def set_attribute(self, k: str, v):
        return

    def add_event(event_name: str, j_val: json):
        return

    def get_span_context(self):
        return self.ctx


class TracerTriage:
    def __init__(self, tracer: Tracer = None):
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
        return

    def get_current_span(self):
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            return SpanMok()
        else:
            return get_current_span()

    def start_as_current_span(self, span_name: str) -> Span:
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            return SpanMok()
        else:
            return self.real_tracer.start_as_current_span(span_name)

    def start_span(self, span_name: str) -> Span:
        if hasattr(settings, 'TELEMETRY') is False or settings.TELEMETRY is False:
            return SpanMok()
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
