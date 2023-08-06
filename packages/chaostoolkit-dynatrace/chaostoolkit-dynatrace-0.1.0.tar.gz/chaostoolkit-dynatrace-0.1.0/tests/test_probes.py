# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock

from chaoslib.exceptions import ActivityFailed
from chaosdynatrace.probes import failure_rate


def test_failed_when_not_exist_configuration():
    with pytest.raises(ActivityFailed) as exc:
        failure_rate(
            entity="service_1", relative_time="10mins",
            failed_percentage="0.5", configuration={})
    assert "To run commands" in str(exc.value)

def test_failed_when_api_return_400():
    with requests_mock.mock() as m:
        m.get(
            "https://xxxxx.live.dynatrace.com/api/v1/timeseries",
            status_code=400,
            text="Bad Request")

        with pytest.raises(ActivityFailed) as ex:
            failure_rate(
                entity="service_1", relative_time="10mins",
                failed_percentage="0.5",
                configuration={
                    "dynatrace":{
                        "dynatrace_base_url": "https://xxxxx.live.dynatrace.com",
                        "dynatrace_token": "c04P6LBfQO-I9svqCXu3q"
                    }
                }
            )
    assert "Dynatrace query" in str(ex.value)