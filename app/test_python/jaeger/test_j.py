from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "test_j !!!"})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=14250,
    collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
)
# provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "my-helloworld-service"}))
processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(processor)

# trace.get_tracer_provider().add_span_processor(
#     BatchSpanProcessor(jaeger_exporter)
# )

tracer = trace.get_tracer(__name__)

idx = 0
while idx < 50:
    with tracer.start_as_current_span("nivo1",  kind=trace.SpanKind.SERVER):
        with tracer.start_as_current_span("nivo2"):
            with tracer.start_as_current_span("nico3"):
                print("Hello world " + str(idx) + " from OpenTelemetry Python!")
    idx += 1
