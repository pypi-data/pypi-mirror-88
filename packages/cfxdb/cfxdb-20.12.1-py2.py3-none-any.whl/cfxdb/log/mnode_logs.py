##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from zlmdb import table, MapTimestampUuidFlatBuffers

from cfxdb.log.mnode_log import MNodeLog


@table('256a071f-5aeb-47f3-8786-97cd8281bdb7', build=MNodeLog.build, cast=MNodeLog.cast)
class MNodeLogs(MapTimestampUuidFlatBuffers):
    """
    Persisted managed node heartbeat log records.

    * Table type :class:`zlmdb.MapTimestampUuidFlatBuffers`
    * Key ``(timestamp, node_id)`` type :class:`typing.Tuple[int, uuid.UUID]`
    * Record type :class:`cfxdb.log.mnode_log.MNodeLog`
    """
