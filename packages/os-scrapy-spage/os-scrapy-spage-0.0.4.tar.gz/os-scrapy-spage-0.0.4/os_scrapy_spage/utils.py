import time
from hashlib import md5
from io import BytesIO
from typing import Type, Union

from os_scrapy_record.fetch_status import Group
from os_scrapy_record.items import FetchRecord, fetch_record
from os_spage import write
from os_spage.common import TIME_FORMAT
from os_spage.default_schema import InnerHeaderKeys, RecordTypes
from scrapy.http.response import Response
from twisted.python.failure import Failure


def get_value(key, *objs, default=None):
    for obj in objs:
        if key in obj:
            return obj[key]
    return default


def spage(response: Union[Type[Response], Failure, FetchRecord], **kwargs) -> bytes:
    if not isinstance(response, FetchRecord):
        response = fetch_record(response)
    return _spage(response, **kwargs)


def _spage(item: FetchRecord, **kwargs) -> bytes:
    request = item["request"]
    response = item["response"]
    meta = item["meta"]

    url = get_value("url", request, kwargs)
    inner_header = {}

    for ik, k, objs, dft in (
        (InnerHeaderKeys.VERSION, "spage_version", (meta, kwargs), "1.2"),
        (InnerHeaderKeys.BATCH_ID, "batch_id", (meta, kwargs), None),
        (InnerHeaderKeys.IP_ADDRESS, "ip_address", (response, kwargs), None),
        (InnerHeaderKeys.FETCH_IP, "spider_ip", (meta, kwargs), None),
    ):
        v = get_value(k, *objs, default=dft)
        if v is not None:
            inner_header[ik] = v

    inner_header[InnerHeaderKeys.DIGEST] = get_value(
        "spage_digest", meta, kwargs, default=md5(url.encode()).hexdigest().upper()
    )

    v = get_value("download_latency", meta, kwargs)
    if v is not None:
        inner_header["Download-Latency"] = round(v)

    v = get_value("fetch_time", meta, kwargs)
    if v is not None:
        inner_header[InnerHeaderKeys.FETCH_TIME] = time.strftime(
            TIME_FORMAT, time.localtime(v)
        )

    v = get_value("redirect_urls", meta)
    if v is not None:
        inner_header["Redirect-Count"] = len(v)
        inner_header["Final-Redirect"] = v[-1]

    status = response["status"]
    body = get_value("body", response)
    if not (status.group == Group.HTTP and (status.code == 200 or status.code == 206)):
        inner_header[InnerHeaderKeys.TYPE] = RecordTypes.DELETED
        inner_header["DeadDelete"] = "0"
        inner_header[
            InnerHeaderKeys.ERROR_REASON
        ] = f"{Group(status.group).name} {status.code}"
        size = 0 if not body else len(body)
        inner_header[InnerHeaderKeys.ORIGINAL_SIZE] = size

    v = get_value("headers", request)
    if v is not None:
        v = v.to_unicode_dict()
        if InnerHeaderKeys.USER_AGENT in v:
            inner_header[InnerHeaderKeys.USER_AGENT] = v[InnerHeaderKeys.USER_AGENT]

    http_header = None
    v = get_value("headers", response)
    if v is not None:
        http_header = v.to_unicode_dict()

    spage = BytesIO()
    write(
        spage,
        url,
        inner_header=inner_header,
        http_header=http_header,
        data=body,
    )
    spage.seek(0)
    o = spage.read()
    spage.close()
    return o
