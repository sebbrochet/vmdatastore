#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
from pyVim import connect
from pyVmomi import vim, vmodl
import time

import requests
requests.packages.urllib3.disable_warnings()

def myprint(unicodeobj):
    import sys
    print unicodeobj.encode(sys.stdout.encoding or 'utf-8')


def get_service_instance(args):
    service_instance = None

    try:
        service_instance = connect.SmartConnect(host=args.target,
                                                user=args.user,
                                                pwd=args.password,
                                                port=int(args.port))
        atexit.register(connect.Disconnect, service_instance)
    except IOError as e:
        pass
    except vim.fault.InvalidLogin, e:
        raise SystemExit("Error: %s" % e.msg)
    except TypeError, e:
        raise SystemExit("Error: %s" % e.message) 

    if not service_instance:
        raise SystemExit("Error: unable to connect to target with supplied info.")

    return service_instance


def print_fs(host_fs):
    """
    Prints the host file system volume info

    :param host_fs:
    :return:
    """
    print "Path           %s" % host_fs.mountInfo.path
    print "Access Mode     %s" % host_fs.mountInfo.accessMode
    print "Mounted        %s" % host_fs.mountInfo.mounted
    print "Accessible     %s" % host_fs.mountInfo.accessible
    print "Inaccessible Reason %s" % host_fs.mountInfo.inaccessibleReason
    print "Datastore:     %s" % host_fs.volume.name
    print "UUID:          %s" % host_fs.volume.uuid
    print "Capacity:      %s" % host_fs.volume.capacity
    print "VMFS Version:  %s" % host_fs.volume.version
    print "Is Local VMFS: %s" % host_fs.volume.local
    print "SSD:           %s" % host_fs.volume.ssd


def cmd_list_datastore(args):
    service_instance = get_service_instance(args)
    content = service_instance.RetrieveContent()

    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()

    for esxi_host in esxi_hosts:
       print "Checking ESXi Host: %s" % esxi_host.name

       # All Filesystems on ESXi host
       storage_system = esxi_host.configManager.storageSystem
       host_file_sys_vol_mount_info = storage_system.fileSystemVolumeInfo.mountInfo

       # Map all filesystems
       for host_mount_info in host_file_sys_vol_mount_info:
          # Extract only VMFS volumes
          if host_mount_info.volume.type == "VMFS":
             extents = host_mount_info.volume.extent
             print_fs(host_mount_info)

             extent_arr = []
             extent_count = 0
             for extent in extents:
                print "Extent[%s] = %s" % (extent_count, extent.diskName)
                extent_count += 1
                print

def cmd_resolve_volumes(args):
    service_instance = get_service_instance(args)
    content = service_instance.RetrieveContent()

    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()


    spec_list = []

    for esxi_host in esxi_hosts:
       print "Checking ESXi Host: %s" % esxi_host.name

       storage_system = esxi_host.configManager.storageSystem
       unresolved_vmfs_volumes = storage_system.QueryUnresolvedVmfsVolume()
       unresolved_spec_list = []
       for vol in unresolved_vmfs_volumes:
          unresolved_vmfs_resolution_spec = vim.host.UnresolvedVmfsResolutionSpec()

          print "Examining %s (%s)..." % (vol.vmfsLabel, vol.vmfsUuid)

          extend_device_path = []
          for extend in vol.extent:
             print "Resolving extend %s..." % extend.devicePath
             extend_device_path.append(extend.devicePath)

          unresolved_vmfs_resolution_spec.extentDevicePath = extend_device_path
          unresolved_vmfs_resolution_spec.uuidResolution = 'forceMount' # 'forceMount' or 'resignature'
          unresolved_spec_list.append(unresolved_vmfs_resolution_spec)

       if unresolved_spec_list:
          result = storage_system.ResolveMultipleUnresolvedVmfsVolumes(unresolved_spec_list)    
          print "ResolutionResult = %s" % result

       storage_system.RescanVmfs()

def cmd_list_unresolved_volumes2(args):
    service_instance = get_service_instance(args)
    content = service_instance.RetrieveContent()

    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()


    spec_list = []

    for esxi_host in esxi_hosts:
       print "Checking ESXi Host: %s" % esxi_host.name

       unresolved_vmfs_volumes =  esxi_host.configManager.storageSystem.QueryUnresolvedVmfsVolume()

       for vol in unresolved_vmfs_volumes:
          print "Unresolved datastore: %s (%s) [%s]..." % (vol.vmfsLabel, vol.vmfsUuid, vol.resolveStatus)

def cmd_list_unresolved_volumes(args):
    service_instance = get_service_instance(args)
    content = service_instance.RetrieveContent()

    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()


    spec_list = []

    for esxi_host in esxi_hosts:
       print "Checking ESXi Host: %s" % esxi_host.name

       unresolved_vmfs_volumes = esxi_host.configManager.datastoreSystem.QueryUnresolvedVmfsVolumes()

       for vol in unresolved_vmfs_volumes:
          print "Unresolved datastore: %s (%s) [%s]..." % (vol.vmfsLabel, vol.vmfsUuid, vol.resolveStatus)

def cmd_resignature_volumes(args):
    service_instance = get_service_instance(args)
    content = service_instance.RetrieveContent()

    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()


    spec_list = []

    for esxi_host in esxi_hosts:
       print "Checking ESXi Host: %s" % esxi_host.name

       # All Filesystems on ESXi host
       datastore_system = esxi_host.configManager.datastoreSystem
       unresolved_vmfs_volumes = datastore_system.QueryUnresolvedVmfsVolumes()

       for vol in unresolved_vmfs_volumes:
          print "Examining %s (%s)..." % (vol.vmfsLabel, vol.vmfsUuid)

          extend_device_path = []
          for extend in vol.extent:
             print "Resolving extend %s..." % extend.devicePath
             extend_device_path.append(extend.devicePath)

          unresolved_vmfs_resignature_spec = vim.host.UnresolvedVmfsResignatureSpec()
          unresolved_vmfs_resignature_spec.extentDevicePath = extend_device_path
          task = datastore_system.ResignatureUnresolvedVmfsVolume(unresolved_vmfs_resignature_spec)
          while task.info.state == 'running' or task.info.state == 'queued':
              import time
              time.sleep(0.5)
