def get_logger():
    import logging, sys
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logger = logging.getLogger(__name__)
    return logger


def log_event(level, start, end, status, process_type, payload, attributes=None, failure_classification=None):
    import json
    assert isinstance(payload, dict)
    assert isinstance(attributes, dict) or attributes is None
    assert status in {'success', 'anomalous', 'failure', 're-queued'}
    level_mapping = dict(
        critical=50,
        error=40,
        warning=30,
        info=20,
        debug=10
    )
    log_message = {
        "process_start_utc": start.timestamp(),
        "process_end_utc": end.timestamp(),
        "process_type": process_type,
        "status": status,
        "failure_classification": failure_classification if failure_classification is not None else "",
        "attributes": attributes if attributes is not None else {},
        "payload": payload
    }
    get_logger().log(level=level_mapping[level.lower()], msg=json.dumps(log_message))
    return log_message
