# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.scheduler_v1.services.cloud_scheduler import CloudSchedulerAsyncClient
from google.cloud.scheduler_v1.services.cloud_scheduler import CloudSchedulerClient
from google.cloud.scheduler_v1.services.cloud_scheduler import pagers
from google.cloud.scheduler_v1.services.cloud_scheduler import transports
from google.cloud.scheduler_v1.types import cloudscheduler
from google.cloud.scheduler_v1.types import job
from google.cloud.scheduler_v1.types import job as gcs_job
from google.cloud.scheduler_v1.types import target
from google.oauth2 import service_account
from google.protobuf import any_pb2 as gp_any  # type: ignore
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert CloudSchedulerClient._get_default_mtls_endpoint(None) is None
    assert (
        CloudSchedulerClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudSchedulerClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        CloudSchedulerClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudSchedulerClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        CloudSchedulerClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [CloudSchedulerClient, CloudSchedulerAsyncClient]
)
def test_cloud_scheduler_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "cloudscheduler.googleapis.com:443"


def test_cloud_scheduler_client_get_transport_class():
    transport = CloudSchedulerClient.get_transport_class()
    assert transport == transports.CloudSchedulerGrpcTransport

    transport = CloudSchedulerClient.get_transport_class("grpc")
    assert transport == transports.CloudSchedulerGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudSchedulerClient, transports.CloudSchedulerGrpcTransport, "grpc"),
        (
            CloudSchedulerAsyncClient,
            transports.CloudSchedulerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    CloudSchedulerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudSchedulerClient),
)
@mock.patch.object(
    CloudSchedulerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudSchedulerAsyncClient),
)
def test_cloud_scheduler_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(CloudSchedulerClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(CloudSchedulerClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (CloudSchedulerClient, transports.CloudSchedulerGrpcTransport, "grpc", "true"),
        (
            CloudSchedulerAsyncClient,
            transports.CloudSchedulerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (CloudSchedulerClient, transports.CloudSchedulerGrpcTransport, "grpc", "false"),
        (
            CloudSchedulerAsyncClient,
            transports.CloudSchedulerGrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    CloudSchedulerClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudSchedulerClient),
)
@mock.patch.object(
    CloudSchedulerAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(CloudSchedulerAsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_cloud_scheduler_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudSchedulerClient, transports.CloudSchedulerGrpcTransport, "grpc"),
        (
            CloudSchedulerAsyncClient,
            transports.CloudSchedulerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_scheduler_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (CloudSchedulerClient, transports.CloudSchedulerGrpcTransport, "grpc"),
        (
            CloudSchedulerAsyncClient,
            transports.CloudSchedulerGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_cloud_scheduler_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_cloud_scheduler_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.scheduler_v1.services.cloud_scheduler.transports.CloudSchedulerGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = CloudSchedulerClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_jobs(
    transport: str = "grpc", request_type=cloudscheduler.ListJobsRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudscheduler.ListJobsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.ListJobsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListJobsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_jobs_from_dict():
    test_list_jobs(request_type=dict)


@pytest.mark.asyncio
async def test_list_jobs_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.ListJobsRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudscheduler.ListJobsResponse(next_page_token="next_page_token_value",)
        )

        response = await client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.ListJobsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListJobsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_jobs_async_from_dict():
    await test_list_jobs_async(request_type=dict)


def test_list_jobs_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.ListJobsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        call.return_value = cloudscheduler.ListJobsResponse()

        client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_jobs_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.ListJobsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudscheduler.ListJobsResponse()
        )

        await client.list_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_jobs_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudscheduler.ListJobsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_jobs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_jobs_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_jobs(
            cloudscheduler.ListJobsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_jobs_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = cloudscheduler.ListJobsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            cloudscheduler.ListJobsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_jobs(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_jobs_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_jobs(
            cloudscheduler.ListJobsRequest(), parent="parent_value",
        )


def test_list_jobs_pager():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudscheduler.ListJobsResponse(
                jobs=[job.Job(), job.Job(), job.Job(),], next_page_token="abc",
            ),
            cloudscheduler.ListJobsResponse(jobs=[], next_page_token="def",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(),], next_page_token="ghi",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(), job.Job(),],),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_jobs(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, job.Job) for i in results)


def test_list_jobs_pages():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_jobs), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudscheduler.ListJobsResponse(
                jobs=[job.Job(), job.Job(), job.Job(),], next_page_token="abc",
            ),
            cloudscheduler.ListJobsResponse(jobs=[], next_page_token="def",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(),], next_page_token="ghi",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(), job.Job(),],),
            RuntimeError,
        )
        pages = list(client.list_jobs(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_jobs_async_pager():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudscheduler.ListJobsResponse(
                jobs=[job.Job(), job.Job(), job.Job(),], next_page_token="abc",
            ),
            cloudscheduler.ListJobsResponse(jobs=[], next_page_token="def",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(),], next_page_token="ghi",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(), job.Job(),],),
            RuntimeError,
        )
        async_pager = await client.list_jobs(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, job.Job) for i in responses)


@pytest.mark.asyncio
async def test_list_jobs_async_pages():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_jobs), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            cloudscheduler.ListJobsResponse(
                jobs=[job.Job(), job.Job(), job.Job(),], next_page_token="abc",
            ),
            cloudscheduler.ListJobsResponse(jobs=[], next_page_token="def",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(),], next_page_token="ghi",),
            cloudscheduler.ListJobsResponse(jobs=[job.Job(), job.Job(),],),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_jobs(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_job(transport: str = "grpc", request_type=cloudscheduler.GetJobRequest):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.GetJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


def test_get_job_from_dict():
    test_get_job(request_type=dict)


@pytest.mark.asyncio
async def test_get_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.GetJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=job.Job.State.ENABLED,
            )
        )

        response = await client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.GetJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_get_job_async_from_dict():
    await test_get_job_async(request_type=dict)


def test_get_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.GetJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        call.return_value = job.Job()

        client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.GetJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())

        await client.get_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_get_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_get_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_job(
            cloudscheduler.GetJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_get_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_get_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_job(
            cloudscheduler.GetJobRequest(), name="name_value",
        )


def test_create_job(
    transport: str = "grpc", request_type=cloudscheduler.CreateJobRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=gcs_job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.create_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.CreateJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gcs_job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == gcs_job.Job.State.ENABLED


def test_create_job_from_dict():
    test_create_job(request_type=dict)


@pytest.mark.asyncio
async def test_create_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.CreateJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=gcs_job.Job.State.ENABLED,
            )
        )

        response = await client.create_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.CreateJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == gcs_job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_create_job_async_from_dict():
    await test_create_job_async(request_type=dict)


def test_create_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.CreateJobRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        call.return_value = gcs_job.Job()

        client.create_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.CreateJobRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_job.Job())

        await client.create_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_job(
            parent="parent_value", job=gcs_job.Job(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].job == gcs_job.Job(name="name_value")


def test_create_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_job(
            cloudscheduler.CreateJobRequest(),
            parent="parent_value",
            job=gcs_job.Job(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.create_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_job(
            parent="parent_value", job=gcs_job.Job(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].job == gcs_job.Job(name="name_value")


@pytest.mark.asyncio
async def test_create_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_job(
            cloudscheduler.CreateJobRequest(),
            parent="parent_value",
            job=gcs_job.Job(name="name_value"),
        )


def test_update_job(
    transport: str = "grpc", request_type=cloudscheduler.UpdateJobRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=gcs_job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.UpdateJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, gcs_job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == gcs_job.Job.State.ENABLED


def test_update_job_from_dict():
    test_update_job(request_type=dict)


@pytest.mark.asyncio
async def test_update_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.UpdateJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            gcs_job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=gcs_job.Job.State.ENABLED,
            )
        )

        response = await client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.UpdateJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == gcs_job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_update_job_async_from_dict():
    await test_update_job_async(request_type=dict)


def test_update_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.UpdateJobRequest()
    request.job.name = "job.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        call.return_value = gcs_job.Job()

        client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "job.name=job.name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.UpdateJobRequest()
    request.job.name = "job.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_job.Job())

        await client.update_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "job.name=job.name/value",) in kw["metadata"]


def test_update_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_job(
            job=gcs_job.Job(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].job == gcs_job.Job(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_job(
            cloudscheduler.UpdateJobRequest(),
            job=gcs_job.Job(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


@pytest.mark.asyncio
async def test_update_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.update_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gcs_job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_job(
            job=gcs_job.Job(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].job == gcs_job.Job(name="name_value")

        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


@pytest.mark.asyncio
async def test_update_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_job(
            cloudscheduler.UpdateJobRequest(),
            job=gcs_job.Job(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_job(
    transport: str = "grpc", request_type=cloudscheduler.DeleteJobRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.DeleteJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_job_from_dict():
    test_delete_job(request_type=dict)


@pytest.mark.asyncio
async def test_delete_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.DeleteJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.DeleteJobRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_job_async_from_dict():
    await test_delete_job_async(request_type=dict)


def test_delete_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.DeleteJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        call.return_value = None

        client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.DeleteJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_delete_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_delete_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_job(
            cloudscheduler.DeleteJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_delete_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.delete_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_delete_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_job(
            cloudscheduler.DeleteJobRequest(), name="name_value",
        )


def test_pause_job(
    transport: str = "grpc", request_type=cloudscheduler.PauseJobRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.pause_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.PauseJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


def test_pause_job_from_dict():
    test_pause_job(request_type=dict)


@pytest.mark.asyncio
async def test_pause_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.PauseJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=job.Job.State.ENABLED,
            )
        )

        response = await client.pause_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.PauseJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_pause_job_async_from_dict():
    await test_pause_job_async(request_type=dict)


def test_pause_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.PauseJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        call.return_value = job.Job()

        client.pause_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_pause_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.PauseJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())

        await client.pause_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_pause_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.pause_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_pause_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.pause_job(
            cloudscheduler.PauseJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_pause_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.pause_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.pause_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_pause_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.pause_job(
            cloudscheduler.PauseJobRequest(), name="name_value",
        )


def test_resume_job(
    transport: str = "grpc", request_type=cloudscheduler.ResumeJobRequest
):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.resume_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.ResumeJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


def test_resume_job_from_dict():
    test_resume_job(request_type=dict)


@pytest.mark.asyncio
async def test_resume_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.ResumeJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=job.Job.State.ENABLED,
            )
        )

        response = await client.resume_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.ResumeJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_resume_job_async_from_dict():
    await test_resume_job_async(request_type=dict)


def test_resume_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.ResumeJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        call.return_value = job.Job()

        client.resume_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_resume_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.ResumeJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())

        await client.resume_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_resume_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.resume_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_resume_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.resume_job(
            cloudscheduler.ResumeJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_resume_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.resume_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.resume_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_resume_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.resume_job(
            cloudscheduler.ResumeJobRequest(), name="name_value",
        )


def test_run_job(transport: str = "grpc", request_type=cloudscheduler.RunJobRequest):
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job(
            name="name_value",
            description="description_value",
            schedule="schedule_value",
            time_zone="time_zone_value",
            state=job.Job.State.ENABLED,
            pubsub_target=target.PubsubTarget(topic_name="topic_name_value"),
        )

        response = client.run_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.RunJobRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


def test_run_job_from_dict():
    test_run_job(request_type=dict)


@pytest.mark.asyncio
async def test_run_job_async(
    transport: str = "grpc_asyncio", request_type=cloudscheduler.RunJobRequest
):
    client = CloudSchedulerAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            job.Job(
                name="name_value",
                description="description_value",
                schedule="schedule_value",
                time_zone="time_zone_value",
                state=job.Job.State.ENABLED,
            )
        )

        response = await client.run_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == cloudscheduler.RunJobRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, job.Job)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.schedule == "schedule_value"

    assert response.time_zone == "time_zone_value"

    assert response.state == job.Job.State.ENABLED


@pytest.mark.asyncio
async def test_run_job_async_from_dict():
    await test_run_job_async(request_type=dict)


def test_run_job_field_headers():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.RunJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        call.return_value = job.Job()

        client.run_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_run_job_field_headers_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = cloudscheduler.RunJobRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())

        await client.run_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value",) in kw["metadata"]


def test_run_job_flattened():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.run_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


def test_run_job_flattened_error():
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.run_job(
            cloudscheduler.RunJobRequest(), name="name_value",
        )


@pytest.mark.asyncio
async def test_run_job_flattened_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.run_job), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = job.Job()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(job.Job())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.run_job(name="name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].name == "name_value"


@pytest.mark.asyncio
async def test_run_job_flattened_error_async():
    client = CloudSchedulerAsyncClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.run_job(
            cloudscheduler.RunJobRequest(), name="name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.CloudSchedulerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudSchedulerClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.CloudSchedulerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudSchedulerClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.CloudSchedulerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = CloudSchedulerClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudSchedulerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = CloudSchedulerClient(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.CloudSchedulerGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.CloudSchedulerGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudSchedulerGrpcTransport,
        transports.CloudSchedulerGrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = CloudSchedulerClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.CloudSchedulerGrpcTransport,)


def test_cloud_scheduler_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.CloudSchedulerTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_cloud_scheduler_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.scheduler_v1.services.cloud_scheduler.transports.CloudSchedulerTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.CloudSchedulerTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_jobs",
        "get_job",
        "create_job",
        "update_job",
        "delete_job",
        "pause_job",
        "resume_job",
        "run_job",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_cloud_scheduler_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.scheduler_v1.services.cloud_scheduler.transports.CloudSchedulerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CloudSchedulerTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_scheduler_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.scheduler_v1.services.cloud_scheduler.transports.CloudSchedulerTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.CloudSchedulerTransport()
        adc.assert_called_once()


def test_cloud_scheduler_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        CloudSchedulerClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_cloud_scheduler_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.CloudSchedulerGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_cloud_scheduler_host_no_port():
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudscheduler.googleapis.com"
        ),
    )
    assert client.transport._host == "cloudscheduler.googleapis.com:443"


def test_cloud_scheduler_host_with_port():
    client = CloudSchedulerClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="cloudscheduler.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "cloudscheduler.googleapis.com:8000"


def test_cloud_scheduler_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.CloudSchedulerGrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_cloud_scheduler_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that channel is used if provided.
    transport = transports.CloudSchedulerGrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudSchedulerGrpcTransport,
        transports.CloudSchedulerGrpcAsyncIOTransport,
    ],
)
def test_cloud_scheduler_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.CloudSchedulerGrpcTransport,
        transports.CloudSchedulerGrpcAsyncIOTransport,
    ],
)
def test_cloud_scheduler_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel", autospec=True
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=("https://www.googleapis.com/auth/cloud-platform",),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_job_path():
    project = "squid"
    location = "clam"
    job = "whelk"

    expected = "projects/{project}/locations/{location}/jobs/{job}".format(
        project=project, location=location, job=job,
    )
    actual = CloudSchedulerClient.job_path(project, location, job)
    assert expected == actual


def test_parse_job_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "job": "nudibranch",
    }
    path = CloudSchedulerClient.job_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_job_path(path)
    assert expected == actual


def test_topic_path():
    project = "cuttlefish"
    topic = "mussel"

    expected = "projects/{project}/topics/{topic}".format(project=project, topic=topic,)
    actual = CloudSchedulerClient.topic_path(project, topic)
    assert expected == actual


def test_parse_topic_path():
    expected = {
        "project": "winkle",
        "topic": "nautilus",
    }
    path = CloudSchedulerClient.topic_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_topic_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "scallop"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = CloudSchedulerClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "abalone",
    }
    path = CloudSchedulerClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "squid"

    expected = "folders/{folder}".format(folder=folder,)
    actual = CloudSchedulerClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "clam",
    }
    path = CloudSchedulerClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "whelk"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = CloudSchedulerClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "octopus",
    }
    path = CloudSchedulerClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "oyster"

    expected = "projects/{project}".format(project=project,)
    actual = CloudSchedulerClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nudibranch",
    }
    path = CloudSchedulerClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "cuttlefish"
    location = "mussel"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = CloudSchedulerClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
    }
    path = CloudSchedulerClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = CloudSchedulerClient.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.CloudSchedulerTransport, "_prep_wrapped_messages"
    ) as prep:
        client = CloudSchedulerClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.CloudSchedulerTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = CloudSchedulerClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
