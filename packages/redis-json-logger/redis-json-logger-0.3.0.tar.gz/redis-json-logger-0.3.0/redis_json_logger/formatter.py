import json
import logging
import traceback as tb


class JSONFormatter(logging.Formatter):
    required_fields = '__all__'
    exclude_fields = None

    def __init__(self, required_fields=None, exclude_fields=None, datefmt=None):
        if required_fields:
            self.required_fields = required_fields

        if exclude_fields:
            self.exclude_fields = exclude_fields

        if not datefmt:
            self.datefmt = self.default_time_format
        else:
            self.datefmt = datefmt

    def validate_field(self):
        assert not (self.required_fields and self.exclude_fields), ("Cannot set both 'required_fields' and 'exclude_fields' options",)

    def usesTime(self):
        """
        Check if the format uses the creation time of the record.
        """
        if self.required_fields == '__all__':
            return True
        else:
            return 'asctime' in self.required_fields

    def formatMessage(self, record):
        return record.__dict__.copy()

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        log_dict = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            log_dict['exc_text'] = record.exc_text
        if record.stack_info:
            log_dict['stack_info'] = self.formatStack(record.stack_info)
        json_string = self.convert_to_json_string(log_dict)
        return json_string

    def formatException(self, ei):
        return tb.format_exception(*ei)

    def get_required_fields(self):
        return self.required_fields

    def get_exclude_fields(self):
        return self.exclude_fields

    def optimize_required_log_fields(self, log_dict, fields):
        return {field: log_dict.get(field, '') for field in fields}

    def optimize_exclude_log_fields(self, log_dict, fields):
        for field in fields:
            log_dict.pop(field, None)
        return log_dict

    def optimize_log_fields(self, python_log_dict):
        required_fields = self.get_required_fields()
        if required_fields:
            if required_fields == '__all__':
                return python_log_dict
            else:
                return self.optimize_required_log_fields(python_log_dict, required_fields)
        else:
            exclude_fields = self.get_exclude_fields()
            if exclude_fields is None:
                return python_log_dict
            else:
                return self.optimize_exclude_log_fields(python_log_dict, required_fields)

    def convert_to_json_string(self, log_dict):
        optimized_log_dict = self.optimize_log_fields(log_dict)
        return json.dumps(optimized_log_dict)


class LogStashJSONFormatter(JSONFormatter):
    default_time_format = '%Y-%m-%dT%H:%M:%SZ'  # ISO format with UTC notation

    def usesTime(self):
        return True

    def optimize_log_fields(self, python_log_dict):
        python_log_dict = super().optimize_log_fields(python_log_dict)
        python_log_dict['@timestamp'] = python_log_dict.pop('asctime')
        return python_log_dict
