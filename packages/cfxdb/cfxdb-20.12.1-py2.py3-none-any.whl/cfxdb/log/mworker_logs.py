##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from zlmdb import table, MapTimestampUuidStringFlatBuffers

from cfxdb.log.mworker_log import MWorkerLog


@table('5ceaa500-4832-451c-adf4-4fc4968cece0', build=MWorkerLog.build, cast=MWorkerLog.cast)
class MWorkerLogs(MapTimestampUuidStringFlatBuffers):
    """
    Persisted managed node worker heartbeat log records.

    * Table type :class:`zlmdb.MapTimestampUuidStringFlatBuffers`
    * Key ``(timestamp, node_id, worker_id)`` type :class:`typing.Tuple[int, uuid.UUID, uuid.UUID]`
    * Record type :class:`cfxdb.log.mworker_log.MWorkerLog`
    """
