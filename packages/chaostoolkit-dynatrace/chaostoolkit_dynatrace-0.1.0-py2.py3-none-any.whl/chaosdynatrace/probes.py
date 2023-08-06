# -*- coding: utf-8 -*-
from logzero import logger
import requests
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

__all__ = ["failure_rate"]


def failure_rate(entity: str, relative_time: str,
                 failed_percentage: int, configuration: Configuration,
                 secrets: Secrets = None) -> bool:
    """
    Validates the failure rate of a specific service.
    Returns true if the failure rate is less than the expected failure rate
    For more information check the api documentation.
    https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v1/
    """
    dynatrace = configuration.get("dynatrace")
    if not any([dynatrace]):
        raise ActivityFailed('To run commands,'
                             'you must specify the dynatrace api and token '
                             'in the configuration section')

    base = dynatrace.get("dynatrace_base_url")
    url = "{base}/api/v1/timeseries".format(base=base)

    params = {"timeseriesId": "com.dynatrace.builtin:service.failurerate",
              "relativeTime": relative_time,
              "aggregationType": "AVG",
              "entity": entity}

    r = requests.get(url,
                     headers={"Content-Type": "application/json",
                              "Authorization": "Api-Token " +
                              dynatrace.get("dynatrace_token")},
                     params=params)

    if r.status_code != 200:
        raise ActivityFailed(
            "Dynatrace query {q} failed: {m}".format(q=str(params), m=r.text))
    acum = 0
    count = 0
    for x in r.json().get("result").get("dataPoints").get(entity):
        if x[1] is not None:
            acum = acum + x[1]
            count = count+1

    logger.debug("faile rate percentage '{}'".format((acum/count)))
    if (acum/count) < failed_percentage:
        return True
    return False
