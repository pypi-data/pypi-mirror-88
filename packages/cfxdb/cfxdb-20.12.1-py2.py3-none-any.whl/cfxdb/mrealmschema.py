##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

from zlmdb import table
from zlmdb import MapStringUuid, MapUuidCbor, MapUuidStringUuid, MapUuidUuidUuid
from zlmdb import MapUuidUuidCbor, MapUuidUuidUuidStringUuid, MapStringStringStringUuid, MapUuidTimestampUuid

from cfxdb.mrealm import RouterCluster, WebCluster, WebService, WebClusterNodeMembership, RouterClusterNodeMembership, RouterWorkerGroup, RouterWorkerGroupClusterPlacement
from cfxdb.mrealm import ApplicationRealm, Role, ApplicationRealmRoleAssociation, Permission, Credential, Principal
from cfxdb.log import MNodeLogs, MWorkerLogs

__all__ = ('MrealmSchema', )


#
# Application Realms
#
@table('7099565b-7b44-4891-a0c8-83c7dbb60883', marshal=ApplicationRealm.marshal, parse=ApplicationRealm.parse)
class ApplicationRealms(MapUuidCbor):
    """
    * Database table: ``arealm_oid -> arealm``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.ApplicationRealm`
    """


@table('89f3073a-32d5-497e-887d-7e930e9c26e6')
class IndexApplicationRealmByName(MapStringUuid):
    """
    * Database index table ``arealm_name -> arealm_oid``
    * Table type :class:`zlmdb.MapStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.ApplicationRealms`
    """


@table('0275b858-890c-4879-945c-720235b093d7')
class IndexApplicationRealmByWebCluster(MapUuidStringUuid):
    """
    * Database index table ``(webcluster_oid, arealm_name) -> arealm_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.ApplicationRealms`
    """


#
# Principals
#
@table('9808cb0b-1b55-4b3f-858e-39004cb11135', marshal=Principal.marshal, parse=Principal.parse)
class Principals(MapUuidCbor):
    """
    * Database table: ``principal_oid -> principal``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.Principal`.
    """


@table('212f3455-6d4c-43ec-843d-53cd17e31974')
class IndexPrincipalByName(MapUuidStringUuid):
    """
    * Database index table ``(arealm_oid, principal_name) -> principal_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.Principals`
    """


#
# Credentials
#
@table('251c8620-425a-4eeb-ade9-4284e8670080', marshal=Credential.marshal, parse=Credential.parse)
class Credentials(MapUuidCbor):
    """
    * Database table: ``credential_oid -> credential``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.Credential`.
    """


@table('45490b42-b167-4df6-ab1c-41d434390397')
class IndexCredentialsByAuth(MapStringStringStringUuid):
    """
    * Database index table ``(authmethod, realm_name, authid) -> credential_oid``
    * Table type :class:`zlmdb.MapStringStringStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.Credentials`
    """


@table('ed0da771-e331-4d93-b50c-d371391cd7b9')
class IndexCredentialsByPrincipal(MapUuidTimestampUuid):
    """
    * Database index table ``(principal_oid, modified) -> credential_oid``
    * Table type :class:`zlmdb.MapUuidIntUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.Credentials`
    """


#
# Roles
#
@table('341083bb-edeb-461c-a6d4-38dddcda6ec9', marshal=Role.marshal, parse=Role.parse)
class Roles(MapUuidCbor):
    """
    * Database table: ``role_oid -> role``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.Role`.
    """


@table('71b990d1-4525-44cd-9ef8-3569de8b4c80')
class IndexRoleByName(MapStringUuid):
    """
    * Database index table ``role_name -> role_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.Roles`
    """


#
# Permissions
#
@table('f98ed35b-f8fb-47ba-81e1-3c014101464d', marshal=Permission.marshal, parse=Permission.parse)
class Permissions(MapUuidCbor):
    """
    * Database table: ``permission_oid -> permission``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealm.Permission`.
    """


@table('6cdc21bf-353d-4477-8631-8eb039142ae9')
class IndexPermissionByUri(MapUuidStringUuid):
    """
    * Database index table ``(role_oid, uri) -> permission_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.Permissions`
    """


#
# Application Realm Role Associations
#
@table('5eabdb63-9c31-4c97-b514-7e8fbac7e143',
       marshal=ApplicationRealmRoleAssociation.marshal,
       parse=ApplicationRealmRoleAssociation.parse)
class ApplicationRealmRoleAssociations(MapUuidUuidCbor):
    """
    * Database table: ``(arealm_oid, role_oid) -> arealm_role_association``
    * Table type :class:`zlmdb.MapUuidUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealm.ApplicationRealmRoleAssociation`.
    """


#
# Router clusters
#
@table('b054a230-c370-4c29-b5de-7e0148321b0a', marshal=RouterCluster.marshal, parse=RouterCluster.parse)
class RouterClusters(MapUuidCbor):
    """
    * Database table: ``routercluster_oid -> routercluster``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.RouterCluster`.
    """


@table('0c80c7a8-7536-4a74-8916-4922c0b72cb7')
class IndexRouterClusterByName(MapStringUuid):
    """
    * Database index table ``routercluster_name -> routercluster_oid``
    * Table type :class:`zlmdb.MapStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.RouterClusters`
    """


#
# Router cluster node memberships
#
@table('a091bad6-f14c-437c-8e30-e9be84380658',
       marshal=RouterClusterNodeMembership.marshal,
       parse=RouterClusterNodeMembership.parse)
class RouterClusterNodeMemberships(MapUuidUuidCbor):
    """
    * Database table: ``(cluster_oid, node_oid) -> cluster_node_membership``
    * Table type :class:`zlmdb.MapUuidUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.RouterClusterNodeMemberships`.
    """


#
# Router worker groups
#
@table('c019457b-d499-454f-9bf2-4f7e85079d8f',
       marshal=RouterWorkerGroup.marshal,
       parse=RouterWorkerGroup.parse)
class RouterWorkerGroups(MapUuidCbor):
    """
    * Database table: ``workergroup_oid -> workergroup``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.RouterWorkerGroup`.
    """


@table('4bb8ec14-4820-4061-8b2c-d1841e2686e1')
class IndexWorkerGroupByCluster(MapUuidStringUuid):
    """
    * Database index table ``(cluster_oid, workergroup_name) -> workergroup_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.RouterWorkerGroups`
    """


#
# Router worker groups to cluster node placements
#
@table('e3d326d2-6140-47a9-adf9-8e93b832717b',
       marshal=RouterWorkerGroupClusterPlacement.marshal,
       parse=RouterWorkerGroupClusterPlacement.parse)
class RouterWorkerGroupClusterPlacements(MapUuidCbor):
    """
    * Database table: ``placement_oid -> placement``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.RouterWorkerGroupClusterPlacement`.
    """


@table('1a18739f-7224-4459-a446-6f1fedd760a7')
class IndexClusterPlacementByWorkerName(MapUuidUuidUuidStringUuid):
    """
    * Database index table ``(workergroup_oid, cluster_oid, node_oid, worker_name) -> placement_oid``
    * Table type :class:`zlmdb.MapUuidUuidUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.RouterWorkerGroupClusterPlacements`
    """


#
# Web clusters
#
@table('719d029f-e9d5-4b25-98e0-cf04d5a2648b', marshal=WebCluster.marshal, parse=WebCluster.parse)
class WebClusters(MapUuidCbor):
    """
    * Database table: ``webcluster_oid -> webcluster``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.WebCluster`.
    """


@table('296c7d17-4769-4e40-8cb7-e6c394b93335')
class IndexWebClusterByName(MapStringUuid):
    """
    * Database index table ``webcluster_name -> webcluster_oid``
    * Table type :class:`zlmdb.MapStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.WebClusters`
    """


#
# Web cluster node memberships
#
@table('e9801077-a629-470b-a4c9-4292a1f00d43',
       marshal=WebClusterNodeMembership.marshal,
       parse=WebClusterNodeMembership.parse)
class WebClusterNodeMemberships(MapUuidUuidCbor):
    """
    * Database table: ``(webcluster_oid, node_oid) -> webcluster_node_membership``
    * Table type :class:`zlmdb.MapUuidUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.WebClusterNodeMembership`.
    """


#
# Web cluster services
#
@table('a8803ca3-09a0-4d72-8728-2469de8d50ac', marshal=WebService.marshal, parse=WebService.parse)
class WebServices(MapUuidCbor):
    """
    * Database table: ``webservice_oid -> webservice``
    * Table type :class:`zlmdb.MapUuidCbor`
    * Key type :class:`uuid.UUID`
    * Record type :class:`cfxdb.mrealmschema.WebService`.
    """


@table('d23d4dbb-5d5c-4ccc-b72a-0ff18363169f')
class IndexWebClusterWebServices(MapUuidUuidUuid):
    """
    * Database index table ``(webcluster_oid, webservice_oid) -> webservice_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.WebServices`
    """


@table('f0b05bcf-f682-49bb-929e-ac252e9867fa')
class IndexWebServiceByPath(MapUuidStringUuid):
    """
    * Database index table ``(webcluster_oid, webservice_name) -> webservice_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.WebServices`
    """


@table('62d0841c-602e-473e-a6d5-3d8ce01e9e06')
class IndexWebClusterPathToWebService(MapUuidStringUuid):
    """
    * Database index table ``(webcluster_oid, path) -> webservice_oid``
    * Table type :class:`zlmdb.MapUuidStringUuid`
    * Key type :class:`uuid.UUID`
    * Indexed table :class:`cfxdb.mrealmschema.WebClusters`
    """


class MrealmSchema(object):
    """
    Management realm database schema.
    """
    def __init__(self, db):
        self.db = db

    principals: Principals
    """
    Application realm client principals.

    * Database table :class:`cfxdb.mrealmschema.Principals`
    """

    idx_principals_by_name: IndexPrincipalByName
    """
    Index on principals (by name).

    * Database table :class:`cfxdb.mrealmschema.IndexPrincipalByName`
    """

    credentials: Credentials
    """
    WAMP client authentication credentials, used for mapping ``(authmethod, realm, authid) -> principal``.

    * Database table :class:`cfxdb.mrealmschema.Credentials`
    """

    idx_credentials_by_auth: IndexCredentialsByAuth
    """
    Index on credentials (by WAMP auth information).

    * Database table :class:`cfxdb.mrealmschema.IndexCredentialsByAuth`
    """

    idx_credentials_by_principal: IndexCredentialsByPrincipal
    """
    Index on credentials (by principal_oid, modified).

    * Database table :class:`cfxdb.mrealmschema.IndexCredentialsByPrincipal`
    """

    roles: Roles
    """
    Roles for used in authorization with application routing.

    * Database table :class:`cfxdb.mrealmschema.Roles`
    """

    idx_roles_by_name: IndexRoleByName
    """
    Index on roles (by name).

    * Database table :class:`cfxdb.mrealmschema.IndexRoleByName`
    """

    permissions: Permissions
    """
    Permissions defined on roles.

    * Database table :class:`cfxdb.mrealmschema.Permissions`
    """

    idx_permissions_by_uri: IndexPermissionByUri
    """
    Index on permissions: by URI.

    * Database table :class:`cfxdb.mrealmschema.IndexPermissionByUri`
    """

    arealms: ApplicationRealms
    """
    Application realms defined in this management realm.

    * Database table :class:`cfxdb.mrealmschema.ApplicationRealms`
    """

    idx_arealms_by_name: IndexApplicationRealmByName
    """
    Index on application realms: by name.

    * Database table :class:`cfxdb.mrealmschema.IndexApplicationRealmByName`
    """

    idx_arealm_by_webcluster: IndexApplicationRealmByWebCluster
    """
    Index on application realms: by web cluster.

    * Database table :class:`cfxdb.mrealmschema.IndexApplicationRealmByWebCluster`
    """

    arealm_role_associations: ApplicationRealmRoleAssociation
    """
    Association of roles to application realms.

    * Database table :class:`cfxdb.mrealmschema.ApplicationRealmRoleAssociation`
    """

    routerclusters: RouterClusters
    """
    Router clusters defined in this management realm.

    * Database table :class:`cfxdb.mrealmschema.RouterClusters`
    """

    idx_routerclusters_by_name: IndexRouterClusterByName
    """
    Index on router clusters: by name.

    * Database table :class:`cfxdb.mrealmschema.IndexRouterClusterByName`
    """

    routercluster_node_memberships: RouterClusterNodeMemberships
    """
    Node membership in router clusters.

    * Database table :class:`cfxdb.mrealmschema.RouterClusterNodeMemberships`
    """

    router_workergroups: RouterWorkerGroups
    """
    Router worker groups.

    * Database table :class:`cfxdb.mrealmschema.RouterWorkerGroups`
    """

    idx_workergroup_by_cluster: IndexWorkerGroupByCluster
    """
    Index on worker groups: by cluster.

    * Database table :class:`cfxdb.mrealmschema.IndexWorkerGroupByCluster`
    """

    router_workergroup_placements: RouterWorkerGroupClusterPlacements
    """
    Router worker cluster placements.

    * Database table :class:`cfxdb.mrealmschema.RouterWorkerGroupClusterPlacements`
    """

    idx_clusterplacement_by_workername: IndexClusterPlacementByWorkerName
    """
    Index on router worker placements: by worker name.

    * Database table :class:`cfxdb.mrealmschema.IndexClusterPlacementByWorkerName`
    """

    webclusters: WebClusters
    """
    Web clusters.

    * Database table :class:`cfxdb.mrealmschema.WebClusters`
    """

    idx_webclusters_by_name: IndexWebClusterByName
    """
    Index of web clusters: by name.

    * Database table :class:`cfxdb.mrealmschema.IndexWebClusterByName`
    """

    webcluster_node_memberships: WebClusterNodeMemberships
    """
    Node membership in web clusters.

    * Database table :class:`cfxdb.mrealmschema.WebClusterNodeMemberships`
    """

    webservices: WebServices
    """
    Web service added to web clusters.

    * Database table :class:`cfxdb.mrealmschema.WebServices`
    """

    idx_webservices_by_path: IndexWebServiceByPath
    """
    Index on web services: by HTTP path.

    * Database table :class:`cfxdb.mrealmschema.IndexWebServiceByPath`
    """

    idx_webcluster_webservices: IndexWebClusterWebServices
    """
    Index on web service: by ...

    * Database table :class:`cfxdb.mrealmschema.IndexWebClusterWebServices`
    """

    mnode_logs: MNodeLogs
    """
    Managed node log records.

    * Database table :class:`cfxdb.mrealmschema.MNodeLogs`
    """

    mworker_logs: MWorkerLogs
    """
    Managed node worker log records.

    * Database table :class:`cfxdb.mrealmschema.MWorkerLogs`
    """

    @staticmethod
    def attach(db):
        """
        Factory to create a schema from attaching to a database. The schema tables
        will be automatically mapped as persistant maps and attached to the
        database slots.

        :param db: zlmdb.Database
        :return: object of Schema
        """
        schema = MrealmSchema(db)

        # application realms
        schema.arealms = db.attach_table(ApplicationRealms)

        schema.idx_arealms_by_name = db.attach_table(IndexApplicationRealmByName)
        schema.arealms.attach_index('idx1', schema.idx_arealms_by_name, lambda arealm: arealm.name)

        schema.idx_arealm_by_webcluster = db.attach_table(IndexApplicationRealmByWebCluster)
        schema.arealms.attach_index('idx2',
                                    schema.idx_arealm_by_webcluster,
                                    lambda arealm: (arealm.webcluster_oid, arealm.name),
                                    nullable=True)

        # principals
        schema.principals = db.attach_table(Principals)

        schema.idx_principals_by_name = db.attach_table(IndexPrincipalByName)
        schema.principals.attach_index('idx1', schema.idx_principals_by_name, lambda principal:
                                       (principal.arealm_oid, principal.authid))

        # credentials
        schema.credentials = db.attach_table(Credentials)

        schema.idx_credentials_by_auth = db.attach_table(IndexCredentialsByAuth)
        schema.credentials.attach_index(
            'idx1', schema.idx_credentials_by_auth, lambda credential:
            (credential.authmethod, credential.realm, credential.authid))

        schema.idx_credentials_by_principal = db.attach_table(IndexCredentialsByPrincipal)
        schema.credentials.attach_index('idx2', schema.idx_credentials_by_principal, lambda credential:
                                        (credential.principal_oid, credential.created))

        # roles
        schema.roles = db.attach_table(Roles)

        schema.idx_roles_by_name = db.attach_table(IndexRoleByName)
        schema.roles.attach_index('idx1', schema.idx_roles_by_name, lambda role: role.name)

        schema.arealm_role_associations = db.attach_table(ApplicationRealmRoleAssociations)

        # permissions
        schema.permissions = db.attach_table(Permissions)

        schema.idx_permissions_by_uri = db.attach_table(IndexPermissionByUri)
        schema.permissions.attach_index('idx1', schema.idx_permissions_by_uri, lambda permission:
                                        (permission.role_oid, permission.uri))

        # router clusters
        schema.routerclusters = db.attach_table(RouterClusters)

        schema.idx_routerclusters_by_name = db.attach_table(IndexRouterClusterByName)
        schema.routerclusters.attach_index('idx1', schema.idx_routerclusters_by_name,
                                           lambda routercluster: routercluster.name)

        schema.routercluster_node_memberships = db.attach_table(RouterClusterNodeMemberships)

        # router worker groups
        schema.router_workergroups = db.attach_table(RouterWorkerGroups)

        schema.idx_workergroup_by_cluster = db.attach_table(IndexWorkerGroupByCluster)
        schema.router_workergroups.attach_index('idx1', schema.idx_workergroup_by_cluster, lambda wg:
                                                (wg.cluster_oid, wg.name))

        # router worker group placements
        schema.router_workergroup_placements = db.attach_table(RouterWorkerGroupClusterPlacements)

        schema.idx_clusterplacement_by_workername = db.attach_table(IndexClusterPlacementByWorkerName)
        schema.router_workergroup_placements.attach_index(
            'idx1', schema.idx_clusterplacement_by_workername, lambda p:
            (p.worker_group_oid, p.cluster_oid, p.node_oid, p.worker_name))

        # web clusters
        schema.webclusters = db.attach_table(WebClusters)

        schema.idx_webclusters_by_name = db.attach_table(IndexWebClusterByName)
        schema.webclusters.attach_index('idx1', schema.idx_webclusters_by_name,
                                        lambda webcluster: webcluster.name)

        schema.webcluster_node_memberships = db.attach_table(WebClusterNodeMemberships)

        # web services
        schema.webservices = db.attach_table(WebServices)

        schema.idx_webservices_by_path = db.attach_table(IndexWebServiceByPath)
        schema.webservices.attach_index('idx1', schema.idx_webservices_by_path, lambda webservice:
                                        (webservice.webcluster_oid, webservice.path))

        schema.idx_webcluster_webservices = db.attach_table(IndexWebClusterWebServices)
        schema.webservices.attach_index('idx2', schema.idx_webcluster_webservices, lambda webservice:
                                        (webservice.webcluster_oid, webservice.oid))

        schema.mnode_logs = db.attach_table(MNodeLogs)
        schema.mworker_logs = db.attach_table(MWorkerLogs)

        return schema
