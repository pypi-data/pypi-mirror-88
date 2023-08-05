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

import proto  # type: ignore


from google.cloud.scheduler_v1beta1.types import target
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as gr_status  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.scheduler.v1beta1", manifest={"Job", "RetryConfig",},
)


class Job(proto.Message):
    r"""Configuration for a job.
    The maximum allowed size for a job is 100KB.

    Attributes:
        name (str):
            Optionally caller-specified in
            [CreateJob][google.cloud.scheduler.v1beta1.CloudScheduler.CreateJob],
            after which it becomes output only.

            The job name. For example:
            ``projects/PROJECT_ID/locations/LOCATION_ID/jobs/JOB_ID``.

            -  ``PROJECT_ID`` can contain letters ([A-Za-z]), numbers
               ([0-9]), hyphens (-), colons (:), or periods (.). For
               more information, see `Identifying
               projects <https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects>`__
            -  ``LOCATION_ID`` is the canonical ID for the job's
               location. The list of available locations can be obtained
               by calling
               [ListLocations][google.cloud.location.Locations.ListLocations].
               For more information, see
               https://cloud.google.com/about/locations/.
            -  ``JOB_ID`` can contain only letters ([A-Za-z]), numbers
               ([0-9]), hyphens (-), or underscores (_). The maximum
               length is 500 characters.
        description (str):
            Optionally caller-specified in
            [CreateJob][google.cloud.scheduler.v1beta1.CloudScheduler.CreateJob]
            or
            [UpdateJob][google.cloud.scheduler.v1beta1.CloudScheduler.UpdateJob].

            A human-readable description for the job. This string must
            not contain more than 500 characters.
        pubsub_target (~.target.PubsubTarget):
            Pub/Sub target.
        app_engine_http_target (~.target.AppEngineHttpTarget):
            App Engine HTTP target.
        http_target (~.target.HttpTarget):
            HTTP target.
        schedule (str):
            Required, except when used with
            [UpdateJob][google.cloud.scheduler.v1beta1.CloudScheduler.UpdateJob].

            Describes the schedule on which the job will be executed.

            The schedule can be either of the following types:

            -  `Crontab <http://en.wikipedia.org/wiki/Cron#Overview>`__
            -  English-like
               `schedule <https://cloud.google.com/scheduler/docs/configuring/cron-job-schedules>`__

            As a general rule, execution ``n + 1`` of a job will not
            begin until execution ``n`` has finished. Cloud Scheduler
            will never allow two simultaneously outstanding executions.
            For example, this implies that if the ``n+1``\ th execution
            is scheduled to run at 16:00 but the ``n``\ th execution
            takes until 16:15, the ``n+1``\ th execution will not start
            until ``16:15``. A scheduled start time will be delayed if
            the previous execution has not ended when its scheduled time
            occurs.

            If
            [retry_count][google.cloud.scheduler.v1beta1.RetryConfig.retry_count]
            > 0 and a job attempt fails, the job will be tried a total
            of
            [retry_count][google.cloud.scheduler.v1beta1.RetryConfig.retry_count]
            times, with exponential backoff, until the next scheduled
            start time.
        time_zone (str):
            Specifies the time zone to be used in interpreting
            [schedule][google.cloud.scheduler.v1beta1.Job.schedule]. The
            value of this field must be a time zone name from the `tz
            database <http://en.wikipedia.org/wiki/Tz_database>`__.

            Note that some time zones include a provision for daylight
            savings time. The rules for daylight saving time are
            determined by the chosen tz. For UTC use the string "utc".
            If a time zone is not specified, the default will be in UTC
            (also known as GMT).
        user_update_time (~.timestamp.Timestamp):
            Output only. The creation time of the job.
        state (~.job.Job.State):
            Output only. State of the job.
        status (~.gr_status.Status):
            Output only. The response from the target for
            the last attempted execution.
        schedule_time (~.timestamp.Timestamp):
            Output only. The next time the job is
            scheduled. Note that this may be a retry of a
            previously failed attempt or the next execution
            time according to the schedule.
        last_attempt_time (~.timestamp.Timestamp):
            Output only. The time the last job attempt
            started.
        retry_config (~.job.RetryConfig):
            Settings that determine the retry behavior.
        attempt_deadline (~.duration.Duration):
            The deadline for job attempts. If the request handler does
            not respond by this deadline then the request is cancelled
            and the attempt is marked as a ``DEADLINE_EXCEEDED``
            failure. The failed attempt can be viewed in execution logs.
            Cloud Scheduler will retry the job according to the
            [RetryConfig][google.cloud.scheduler.v1beta1.RetryConfig].

            The allowed duration for this deadline is:

            -  For [HTTP
               targets][google.cloud.scheduler.v1beta1.Job.http_target],
               between 15 seconds and 30 minutes.
            -  For [App Engine HTTP
               targets][google.cloud.scheduler.v1beta1.Job.app_engine_http_target],
               between 15 seconds and 24 hours.
            -  For [PubSub
               targets][google.cloud.scheduler.v1beta1.Job.pubsub_target],
               this field is ignored.
    """

    class State(proto.Enum):
        r"""State of the job."""
        STATE_UNSPECIFIED = 0
        ENABLED = 1
        PAUSED = 2
        DISABLED = 3
        UPDATE_FAILED = 4

    name = proto.Field(proto.STRING, number=1)

    description = proto.Field(proto.STRING, number=2)

    pubsub_target = proto.Field(
        proto.MESSAGE, number=4, oneof="target", message=target.PubsubTarget,
    )

    app_engine_http_target = proto.Field(
        proto.MESSAGE, number=5, oneof="target", message=target.AppEngineHttpTarget,
    )

    http_target = proto.Field(
        proto.MESSAGE, number=6, oneof="target", message=target.HttpTarget,
    )

    schedule = proto.Field(proto.STRING, number=20)

    time_zone = proto.Field(proto.STRING, number=21)

    user_update_time = proto.Field(
        proto.MESSAGE, number=9, message=timestamp.Timestamp,
    )

    state = proto.Field(proto.ENUM, number=10, enum=State,)

    status = proto.Field(proto.MESSAGE, number=11, message=gr_status.Status,)

    schedule_time = proto.Field(proto.MESSAGE, number=17, message=timestamp.Timestamp,)

    last_attempt_time = proto.Field(
        proto.MESSAGE, number=18, message=timestamp.Timestamp,
    )

    retry_config = proto.Field(proto.MESSAGE, number=19, message="RetryConfig",)

    attempt_deadline = proto.Field(proto.MESSAGE, number=22, message=duration.Duration,)


class RetryConfig(proto.Message):
    r"""Settings that determine the retry behavior.

    By default, if a job does not complete successfully (meaning that an
    acknowledgement is not received from the handler, then it will be
    retried with exponential backoff according to the settings in
    [RetryConfig][google.cloud.scheduler.v1beta1.RetryConfig].

    Attributes:
        retry_count (int):
            The number of attempts that the system will make to run a
            job using the exponential backoff procedure described by
            [max_doublings][google.cloud.scheduler.v1beta1.RetryConfig.max_doublings].

            The default value of retry_count is zero.

            If retry_count is zero, a job attempt will *not* be retried
            if it fails. Instead the Cloud Scheduler system will wait
            for the next scheduled execution time.

            If retry_count is set to a non-zero number then Cloud
            Scheduler will retry failed attempts, using exponential
            backoff, retry_count times, or until the next scheduled
            execution time, whichever comes first.

            Values greater than 5 and negative values are not allowed.
        max_retry_duration (~.duration.Duration):
            The time limit for retrying a failed job, measured from time
            when an execution was first attempted. If specified with
            [retry_count][google.cloud.scheduler.v1beta1.RetryConfig.retry_count],
            the job will be retried until both limits are reached.

            The default value for max_retry_duration is zero, which
            means retry duration is unlimited.
        min_backoff_duration (~.duration.Duration):
            The minimum amount of time to wait before
            retrying a job after it fails.

            The default value of this field is 5 seconds.
        max_backoff_duration (~.duration.Duration):
            The maximum amount of time to wait before
            retrying a job after it fails.

            The default value of this field is 1 hour.
        max_doublings (int):
            The time between retries will double ``max_doublings``
            times.

            A job's retry interval starts at
            [min_backoff_duration][google.cloud.scheduler.v1beta1.RetryConfig.min_backoff_duration],
            then doubles ``max_doublings`` times, then increases
            linearly, and finally retries retries at intervals of
            [max_backoff_duration][google.cloud.scheduler.v1beta1.RetryConfig.max_backoff_duration]
            up to
            [retry_count][google.cloud.scheduler.v1beta1.RetryConfig.retry_count]
            times.

            For example, if
            [min_backoff_duration][google.cloud.scheduler.v1beta1.RetryConfig.min_backoff_duration]
            is 10s,
            [max_backoff_duration][google.cloud.scheduler.v1beta1.RetryConfig.max_backoff_duration]
            is 300s, and ``max_doublings`` is 3, then the a job will
            first be retried in 10s. The retry interval will double
            three times, and then increase linearly by 2^3 \* 10s.
            Finally, the job will retry at intervals of
            [max_backoff_duration][google.cloud.scheduler.v1beta1.RetryConfig.max_backoff_duration]
            until the job has been attempted
            [retry_count][google.cloud.scheduler.v1beta1.RetryConfig.retry_count]
            times. Thus, the requests will retry at 10s, 20s, 40s, 80s,
            160s, 240s, 300s, 300s, ....

            The default value of this field is 5.
    """

    retry_count = proto.Field(proto.INT32, number=1)

    max_retry_duration = proto.Field(
        proto.MESSAGE, number=2, message=duration.Duration,
    )

    min_backoff_duration = proto.Field(
        proto.MESSAGE, number=3, message=duration.Duration,
    )

    max_backoff_duration = proto.Field(
        proto.MESSAGE, number=4, message=duration.Duration,
    )

    max_doublings = proto.Field(proto.INT32, number=5)


__all__ = tuple(sorted(__protobuf__.manifest))
