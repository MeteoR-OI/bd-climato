"""
    Later: need to call only api methods
    sdk (implementation) will be loaded with env variables
    But not fully available at the time of coding
    Then telemetry call directly sdk methods
    And a no-telemetry mode was coded too..
"""
from django.conf import settings
from opentelemetry import trace
from opentelemetry.exporter.jaeger.proto import grpc
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider, Tracer
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation import get_current_span
from opentelemetry.trace.span import INVALID_SPAN, Span
import app.tools.myTools as t
import json
import sys


class ContextMok:
    """
    ContextMok
        Mok class to simulate context class when no telemetry is used
    """
    traceID = None


class SpanMok:
    """
    SpanMok
        Mok class to simulate Span class when no telemetry is used
    """
    ctx = ContextMok()

    def __init__(self, name: str = "???", trace_flag: bool = None):
        """
            __init__

            Parameters:
                name: span name
                trace_flag
        """
        try:
            if hasattr(settings, "TELEMETRY") is True and settings.TELEMETRY is True:
                raise Exception("SpanMok", "Calling Mok while telemetry is active")
            self.name = name
            self.trace = trace_flag
            self.atts = []
            self.events = []
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def __enter__(self):
        """
        __enter__

        start of a with statement support
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__

        end of a with statement. print out data if no telemetry is used
        """
        try:
            if self.trace is False:
                return
            # print("Span: " + self.name)
            # print_out = ""
            # for an_att in self.atts:
            #     print_out += str(an_att["k"]) + ": " + str(an_att["v"]) + ", "
            # self.atts = []
            # if print_out.__len__() > 2:
            #     print("     attributes: " + print_out[0:-2])
            #     print_out = ""
            # for an_att in self.events:
            #     print_out += str(an_att["en"]) + ": " + str(an_att["e"]) + ", "
            # self.atts = []
            # if print_out.__len__() > 2:
            #     print("     events: " + print_out[0:-2])
            #     print_out = ""
            return
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def __end__(self):
        """
        __end__

        Not sure if this method is called...
        """
        self.__exit__(1, 2, 3)
        return

    def end(self):
        """
        end
            Dump of a span
        """
        self.__exit__(1, 2, 3)
        return

    def record_exception(self, exc: Exception):
        """
        record_exception
            add an exception in the Span
        """
        t.LogCritical(exc, self)
        return

    def set_attribute(self, k: str, v):
        """
        set_attribute
            Add an attribute in the span
        """
        try:
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                if k == "file_processed":
                    v = str(v).split("/")[-1::1][0]
                self.atts.append({"k": k, "v": v})
            return
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def add_event(self, event_name: str, j_val: json):
        """
        add_event
            Add event in the span
        """
        try:
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                self.events.append({"en": event_name, "e": j_val})
            return
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def get_span_context(self):
        return self.ctx


class TracerTriage:
    """
    TracerTriage
        Call the real tracer, or our Mok implementation
    """
    current_span = None
    future_attributes = []
    future_attributes_copy = []
    trace = False

    def __init__(self, tracer: Tracer = None):
        try:
            self.current_span = None
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                self.real_tracer = self
            else:
                if tracer is None:
                    raise Exception("TracerTriage", "no tracer given")
                self.real_tracer = tracer
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def __enter__(self):
        return self

    def __end__(self):
        self.end_span()
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_span()
        return

    def end_span(self):
        self.clean_future_attribute()
        self.current_span = None
        self.trace = False
        return

    def load_future_attributes_in_span(self, my_span):
        for an_atr in self.future_attributes:
            my_span.set_attribute(an_atr['k'], an_atr['v'])
        self.future_attributes = []

    def save_future_attribute(self):
        self.future_attributes_copy = []
        for an_atr in self.future_attributes:
            self.future_attributes_copy.append(an_atr)

    def restore_future_attribute(self, delete_copy: bool = True):
        for an_atr in self.future_attributes_copy:
            self.future_attributes.append(an_atr)
        if delete_copy is True:
            self.future_attributes_copy = []

    def clean_future_attribute(self):
        self.future_attributes = []
        self.future_attributes_copy = []

    def add_future_attribute(self, k: str, v):
        """
            add attributes that will be loaded in the next span
        """
        if self.current_span is None:
            self.future_attributes.append({"k": k, "v": v})
        else:
            self.current_span.set_attribute(k, v)

    def get_current_or_new_span(self, name: str = "???", trace_flag: bool = None):
        """
        get_current_or_new_span
            Get current span if one is active, or start a new one

        Parameter:
            name: span name (only used if a new span is started)
            trace_flag(only used if a new span is started)
        """
        try:
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                if self.current_span is None:
                    self.current_span = self.start_as_current_span(name, trace_flag)
                return self.current_span
            else:
                tmp_span = get_current_span()
                if tmp_span == INVALID_SPAN:
                    tmp_span = self.start_as_current_span(name, trace_flag)
                    tmp_span = get_current_span()
                return tmp_span
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def start_as_current_span(self, span_name: str, trace_flag: bool = None) -> Span:
        """
        start_as_current_span
            start a new Span

        Parameter:
            name: span name
            trace_flag
        """
        try:
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                self.current_span = SpanMok(span_name, trace_flag)
                self.trace = trace_flag
                if trace_flag is None:
                    print("   ** trace_flag is None")
                return self.current_span
            else:
                my_span = self.real_tracer.start_as_current_span(span_name)
                self.current_span = get_current_span()
                return my_span
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e

    def start_span(self, span_name: str, trace_flag: bool = None) -> Span:
        """
        start_span
            start a sub span of the current span

        Parameter:
            name: span name
            trace_flag
        """
        try:
            if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                self.current_span = SpanMok(span_name, trace_flag)
                self.trace = trace_flag
                if trace_flag is None:
                    print("   ** trace_flag is None")
                return self.current_span
            else:
                self.current_span = self.real_tracer.start_span(span_name)
                return self.current_span
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e


class Telemetry:
    """
        static class to activate telemetry in a module
    """
    tracer: Tracer = None

    @staticmethod
    def Start(service_name: str, caller_name: str = __name__):
        """
        Start
            Activate telemetry

        Parameters:
            service_name
            called_name (use __name__ in caller)
        """
        try:
            if Telemetry.tracer is None:
                if hasattr(settings, "TELEMETRY") is False or settings.TELEMETRY is False:
                    return TracerTriage()

                trace.set_tracer_provider(
                    TracerProvider(
                        resource=Resource.create({SERVICE_NAME: "Climato"})
                    )
                )
                tracer = trace.get_tracer(__name__)

                collector_endpoint = "localhost:14250"
                if hasattr(settings, "JAEGER_COLLECTOR") is True:
                    collector_endpoint = settings.JAEGER_COLLECTOR
                collector_insecure = True
                if hasattr(settings, "JAEGER_INSECURE") is True:
                    collector_insecure = settings.JAEGER_INSECURE

                jaeger_exporter = grpc.JaegerExporter(
                    collector_endpoint=collector_endpoint,
                    insecure=collector_insecure
                )

                # create a BatchSpanProcessor and add the exporter to it
                span_processor = BatchSpanProcessor(jaeger_exporter)

                # add to the tracer factory
                trace.get_tracer_provider().add_span_processor(span_processor)
                Telemetry.tracer = tracer

            return TracerTriage(Telemetry.tracer)
        except Exception as e:
            if e.__dict__.__len__() == 0 or "done" not in e.__dict__:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                exception_info = e.__repr__()
                filename = exception_traceback.tb_frame.f_code.co_filename
                module = exception_traceback.tb_frame.f_code.co_name
                line_number = exception_traceback.tb_lineno
                e.info = {
                    "i": str(exception_info),
                    "f": filename,
                    "n": module,
                    "l": line_number,
                }
                e.done = True
            raise e
