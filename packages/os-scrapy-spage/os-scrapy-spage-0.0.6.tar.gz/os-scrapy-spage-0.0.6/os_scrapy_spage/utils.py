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
from scrapy.utils.python import to_unicode
from twisted.python.failure import Failure


def get_value(key, *objs, rvs=False, default=None):
    r = 1 if not rvs else -1
    for obj in objs[::r]:
        if key in obj:
            return obj[key]
    return default


def spage(
    response: Union[Type[Response], Failure, FetchRecord], rvs=False, **kwargs
) -> bytes:
    if not isinstance(response, FetchRecord):
        response = fetch_record(response)
    return _spage(response, rvs=rvs, **kwargs)


def _spage(item: FetchRecord, rvs=False, **kwargs) -> bytes:
    request = item["request"]
    response = item["response"]
    meta = item["meta"]

    url = get_value("url", request, kwargs, rvs=rvs)
    inner_headers = {}

    for ik, k, objs, dft in (
        (InnerHeaderKeys.VERSION, "spage_version", (meta, kwargs), "1.2"),
        (InnerHeaderKeys.BATCH_ID, "batch_id", (meta, kwargs), None),
        (InnerHeaderKeys.IP_ADDRESS, "ip_address", (response, kwargs), None),
        (InnerHeaderKeys.FETCH_IP, "spider_ip", (meta, kwargs), None),
    ):
        v = get_value(k, *objs, rvs=rvs, default=dft)
        if v is not None:
            inner_headers[ik] = v

    inner_headers[InnerHeaderKeys.DIGEST] = get_value(
        "spage_digest",
        meta,
        kwargs,
        rvs=rvs,
        default=md5(url.encode()).hexdigest().upper(),
    )

    v = get_value("download_latency", meta, kwargs, rvs=rvs)
    if v is not None:
        inner_headers["Download-Latency"] = round(v, 5)

    v = get_value("fetch_time", meta, kwargs, rvs=rvs)
    if v is not None:
        inner_headers[InnerHeaderKeys.FETCH_TIME] = time.strftime(
            TIME_FORMAT, time.localtime(v)
        )

    v = get_value("redirect_urls", meta, kwargs, rvs=rvs)
    if v is not None:
        inner_headers["Redirect-Count"] = len(v)
        inner_headers["Final-Redirect"] = v[-1]

    status = get_value("status", response, kwargs, rvs=rvs)
    body = kwargs.get("response_body", get_value("body", response))
    if not (status.group == Group.HTTP and (status.code == 200 or status.code == 206)):
        inner_headers[InnerHeaderKeys.TYPE] = RecordTypes.DELETED
        inner_headers["DeadDelete"] = "0"
        inner_headers[
            InnerHeaderKeys.ERROR_REASON
        ] = f"{Group(status.group).name} {status.code}"
        size = 0 if not body else len(body)
        inner_headers[InnerHeaderKeys.ORIGINAL_SIZE] = size

    ua = kwargs.get("user_agent")
    if not ua:
        headers = request["headers"]
        if b"User-Agent" in headers:
            ua = to_unicode(headers.get(b"User-Agent"), encoding=headers.encoding)
    if ua:
        inner_headers[InnerHeaderKeys.USER_AGENT] = ua

    http_headers = kwargs.get("http_headers", get_value("headers", response))
    if http_headers is not None:
        if hasattr(http_headers, "to_unicode_dict"):
            http_headers = http_headers.to_unicode_dict()

    spage = BytesIO()
    write(
        spage,
        url,
        inner_header=inner_headers,
        http_header=http_headers,
        data=body,
    )
    spage.seek(0)
    o = spage.read()
    spage.close()
    return o
