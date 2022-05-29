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
