#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright &copy; 2014-2016 NetApp, Inc. All Rights Reserved.
#
# DO NOT EDIT THIS CODE BY HAND! It has been generated with jsvcgen.
#

import click

from element.cli import utils as cli_utils
from element.cli import parser
from element.cli.cli import pass_context
from element import utils
import jsonpickle
import simplejson
from solidfire.models import *
from solidfire.custom.models import *
from uuid import UUID
from element import exceptions
from solidfire import common
from element.cli.cli import SolidFireOption, SolidFireCommand

class ProtectionSchemeVisibility(data_model.DataObject):
    """ProtectionSchemeVisibility  
    The public visibility of the protection scheme.

    """
    enum_values = ("customer", "testOnly", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class ProtectionSchemeCategory(data_model.DataObject):
    """ProtectionSchemeCategory  
    The category of the protection scheme.

    """
    enum_values = ("helix", "erasureCoded", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class DriveEncryptionCapabilityType(data_model.DataObject):
    """DriveEncryptionCapabilityType  
    This specifies a drive's encryption capability.

    """
    enum_values = ("none", "sed", "fips", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class ProtectionDomainType(data_model.DataObject):
    """ProtectionDomainType  
    A Protection Domain is a set of one or more components whose simultaneous failure is protected
    from causing data unavailability or loss. This specifies one of the types of Protection Domains
    recognized by this cluster.

    """
    enum_values = ("node", "chassis", "custom", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class RemoteClusterSnapshotStatus(data_model.DataObject):
    """RemoteClusterSnapshotStatus  
    Status of the remote snapshot on the target cluster as seen on the source cluster

    """
    enum_values = ("Present", "Not Present", "Syncing", "Deleted", "Unknown", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class ProposedNodeErrorCode(data_model.DataObject):
    """ProposedNodeErrorCode  
    This specifies error code for a proposed node addition.

    """
    enum_values = ("nodesNoCapacity", "nodesTooLarge", "nodesConnectFailed", "nodesQueryFailed", "nodesClusterMember", "nonFipsNodeCapable", "nonFipsDrivesCapable", "nodeTypeUnsupported", "nodeTypesHeterogeneous", "nodeTypeInvalid", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class ProtectionScheme(data_model.DataObject):
    """ProtectionScheme  
    The method of protecting data on the cluster

    """
    enum_values = ("singleHelix", "doubleHelix", "tripleHelix", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class FipsDrivesStatusType(data_model.DataObject):
    """FipsDrivesStatusType  
    This specifies a node's FIPS 140-2 compliance status.

    """
    enum_values = ("None", "Partial", "Ready", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class AuthMethod(data_model.DataObject):
    """AuthMethod  
    This type qualifies a ClusterAdmin with its authentication method.

    """
    enum_values = ("Cluster", "Ldap", "Idp", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class AuthConfigType(data_model.DataObject):
    """AuthConfigType  
    This type indicates the configuration data which will be accessed or modified by the element auth container.

    """
    enum_values = ("mNode", "element", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class VolumeAccess(data_model.DataObject):
    """VolumeAccess  
    Describes host access for a volume.

    """
    enum_values = ("locked", "readOnly", "readWrite", "replicationTarget", "snapMirrorTarget", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

class MaintenanceMode(data_model.DataObject):
    """MaintenanceMode  
    Which mode a node is in when it is having maintenenace peformed.

    """
    enum_values = ("Disabled", "FailedToRecover", "Unexpected", "RecoveringFromMaintenance", "PreparingForMaintenance", "ReadyForMaintenance", )

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

@click.group()
@pass_context
def cli(ctx):
    """getremotehosts getloginsessioninfo setremotehosts setloginsessioninfo """

@cli.command('getremotehosts', short_help="""GetRemoteLoggingHosts enables you to retrieve the current list of log servers. """, cls=SolidFireCommand)
@pass_context
def getremotehosts(ctx):
    """GetRemoteLoggingHosts enables you to retrieve the current list of log servers."""

    

    cli_utils.establish_connection(ctx)
    

    

    ctx.logger.info(""": """+""";"""+"")
    try:
        _GetRemoteLoggingHostsResult = ctx.element.get_remote_logging_hosts()
    except common.ApiServerError as e:
        ctx.logger.error(e.message)
        exit()
    except BaseException as e:
        ctx.logger.error(e.__str__())
        exit()
    if ctx.json:
        print(simplejson.dumps(simplejson.loads(_GetRemoteLoggingHostsResult), indent=4))
        return
    else:
        cli_utils.print_result(_GetRemoteLoggingHostsResult, ctx.logger, as_json=ctx.json, as_pickle=ctx.pickle, depth=ctx.depth, filter_tree=ctx.filter_tree)



@cli.command('getloginsessioninfo', short_help="""GetLoginSessionInfo enables you to return the period of time a log in authentication session is valid for both log in shells and the TUI. """, cls=SolidFireCommand)
@pass_context
def getloginsessioninfo(ctx):
    """GetLoginSessionInfo enables you to return the period of time a log in authentication session is valid for both log in shells and the TUI."""

    

    cli_utils.establish_connection(ctx)
    

    

    ctx.logger.info(""": """+""";"""+"")
    try:
        _GetLoginSessionInfoResult = ctx.element.get_login_session_info()
    except common.ApiServerError as e:
        ctx.logger.error(e.message)
        exit()
    except BaseException as e:
        ctx.logger.error(e.__str__())
        exit()
    if ctx.json:
        print(simplejson.dumps(simplejson.loads(_GetLoginSessionInfoResult), indent=4))
        return
    else:
        cli_utils.print_result(_GetLoginSessionInfoResult, ctx.logger, as_json=ctx.json, as_pickle=ctx.pickle, depth=ctx.depth, filter_tree=ctx.filter_tree)



@cli.command('setremotehosts', short_help="""SetRemoteLoggingHosts enables you to configure remote logging from the nodes in the storage cluster to a centralized log server or servers. Remote logging is performed over TCP using the default port 514. This API does not add to the existing logging hosts. Rather, it replaces what currently exists with new values specified by this API method. You can use GetRemoteLoggingHosts to determine what the current logging hosts are, and then use SetRemoteLoggingHosts to set the desired list of current and new logging hosts. """, cls=SolidFireCommand)
@click.option('--remotehosts',
              cls=SolidFireOption,
              is_flag=True,
              multiple=True,
              subparameters=["host", "port", ],
              required=True,
              help="""A list of hosts to send log messages to.  Has the following subparameters: --host --port """)
@click.option('--host',
              required=True,
              prompt=True,
              multiple=True,
              type=str,
              default=None,
              is_sub_parameter=True,
              help="""[subparameter] Hostname or IP address of the log server. """,
              cls=SolidFireOption)
@click.option('--port',
              required=True,
              prompt=True,
              multiple=True,
              type=int,
              default=None,
              is_sub_parameter=True,
              help="""[subparameter] Port number that the log server is listening on. """,
              cls=SolidFireOption)
@pass_context
def setremotehosts(ctx,
           # Mandatory main parameter
           remotehosts,
           # Mandatory subparameter of a mandatory main parameter (Not fully decomposed)
           host,
           # Mandatory subparameter of a mandatory main parameter (Not fully decomposed)
           port):
    """SetRemoteLoggingHosts enables you to configure remote logging from the nodes in the storage cluster to a centralized log server or servers. Remote logging is performed over TCP using the default port 514. This API does not add to the existing logging hosts. Rather, it replaces what currently exists with new values specified by this API method. You can use GetRemoteLoggingHosts to determine what the current logging hosts are, and then use SetRemoteLoggingHosts to set the desired list of current and new logging hosts."""

    

    cli_utils.establish_connection(ctx)
    

    remotehostsArray = None
    if len(remotehosts) == 1 and host[0] is None and port[0] is None:
        remotehostsArray = []
    elif(remotehosts is not None and remotehosts != ()):
        remotehostsArray = []
        try:
            for i, _remotehosts in enumerate(remotehosts):
                remotehostsArray.append(LoggingServer(host=host[i], port=port[i], ))
        except Exception as e:
            ctx.logger.error(e.__str__())
            exit(1)
    

    

    ctx.logger.info(""": """"""remotehosts = """ + str(remotehostsArray)+""";"""+"")
    try:
        _SetRemoteLoggingHostsResult = ctx.element.set_remote_logging_hosts(remote_hosts=remotehostsArray)
    except common.ApiServerError as e:
        ctx.logger.error(e.message)
        exit()
    except BaseException as e:
        ctx.logger.error(e.__str__())
        exit()
    if ctx.json:
        print(simplejson.dumps(simplejson.loads(_SetRemoteLoggingHostsResult), indent=4))
        return
    else:
        cli_utils.print_result(_SetRemoteLoggingHostsResult, ctx.logger, as_json=ctx.json, as_pickle=ctx.pickle, depth=ctx.depth, filter_tree=ctx.filter_tree)



@cli.command('setloginsessioninfo', short_help="""You can use SetLoginSessionInfo to set the period of time that a session's login authentication is valid. After the log in period elapses without activity on the system, the authentication expires. New login credentials are required for continued access to the cluster after the timeout period has elapsed. """, cls=SolidFireCommand)
@click.option('--timeout',
              type=str,
              required=False,
              help="""Cluster authentication expiration period. Formatted in HH:mm:ss. For example, 01:30:00, 00:90:00, and 00:00:5400 can be used to equal a 90 minute timeout period. The default value is 30 minutes. The minimum value is 1 minute. """)
@pass_context
def setloginsessioninfo(ctx,
           # Optional main parameter
           timeout = None):
    """You can use SetLoginSessionInfo to set the period of time that a session's login authentication is valid. After the log in period elapses without activity on the system, the authentication expires. New login credentials are required for continued access to the cluster after the timeout period has elapsed."""

    

    cli_utils.establish_connection(ctx)
    
    

    

    ctx.logger.info(""": """"""timeout = """+str(timeout)+""";"""+"")
    try:
        _SetLoginSessionInfoResult = ctx.element.set_login_session_info(timeout=timeout)
    except common.ApiServerError as e:
        ctx.logger.error(e.message)
        exit()
    except BaseException as e:
        ctx.logger.error(e.__str__())
        exit()
    if ctx.json:
        print(simplejson.dumps(simplejson.loads(_SetLoginSessionInfoResult), indent=4))
        return
    else:
        cli_utils.print_result(_SetLoginSessionInfoResult, ctx.logger, as_json=ctx.json, as_pickle=ctx.pickle, depth=ctx.depth, filter_tree=ctx.filter_tree)


