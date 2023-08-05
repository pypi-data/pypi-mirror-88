

import radical.utils as ru


# ------------------------------------------------------------------------------
#
class ClusterConfig(ru.Config):

    _schema = {
            'description'    : str,
            'lrms'           : str,

            'cores_per_node' : int,
            'gpus_per_node'  : int,
            'mem_per_node'   : int,
            'lfs_per_node'   : int,
            'lfs_path'       : str,
            }

    _defaults = {
            'description'    : '',
            'lrms'           : 'FORK',

            'cores_per_node' : 1,
            'gpus_per_node'  : 0,
            'mem_per_node'   : 0,
            'lfs_per_node'   : 0,
            'lfs_path'       : '/tmp/',
            }


# ------------------------------------------------------------------------------
#
class AccessConfigOption(ru.Config):

    _schema = {
            'job_manager'    : str,
            'job_manager_hop': str,
            'filesystem'     : str,
            }

    _defaults = {
            'job_manager'    : 'fork://localhost/',
            'job_manager_hop': None,
            'filesystem'     : 'file://localhost/',
            }


# ------------------------------------------------------------------------------
#
class AccessConfig(ru.Config):

    _schema = {
            'default'        : str,
            'options'        : {str: AccessConfigOption}
            }

    _defaults = {
            'default'        : 'fork',
            'options'        : {'fork' : AccessConfigOption()}
            }


# ------------------------------------------------------------------------------
#
class SystemConfigOption(ru.Config):

    _schema = {
            'pre_bootstrap_0': [str],
            'pre_bootstrap_1': [str],
            'pre_bootstrap_2': [str],
            'export_to_cu'   : [str],
            'cu_pre_exec'    : [str],
            }

    _defaults = {
            'pre_bootstrap_0': None,
            'pre_bootstrap_1': None,
            'pre_bootstrap_2': None,
            'export_to_cu'   : None,
            'cu_pre_exec'    : None,
            }


# ------------------------------------------------------------------------------
#
class SystemConfig(ru.Config):

    _schema = {
            'valid_roots'    : [str],
            'sandbox_base'   :  str,
            'python_dist'    :  str,
            'virtenv'        :  str,
            'virtenv_mode'   :  str,
            'rp_version'     :  str,
            'pre_bootstrap_0': [str],
            'pre_bootstrap_1': [str],
            'pre_bootstrap_2': [str],
            'export_to_cu'   : [str],
            'cu_pre_exec'    : [str],
            'options'        : {str: SystemConfigOption}
            }


    _defaults = {
            'valid_roots'    : ['/'],
            'sandbox_base'   : '$HOME',
            'python_dist'    : 'default',
            'virtenv'        : None,
            'virtenv_mode'   : 'create',
            'rp_version'     : 'local',
            'pre_bootstrap_0': None,
            'pre_bootstrap_1': None,
            'pre_bootstrap_2': None,
            'export_to_cu'   : None,
            'cu_pre_exec'    : None,
            'options'        : None,
            }


class AgentConfig(ru.Config):

    _schema = {
            'layout'         : str,
            'config'         : str,
            }

    _defaults = {
            'layout'         : 'default',
            'config'         : 'default',
            }


# ------------------------------------------------------------------------------
#
class ResourceConfig(ru.Config):

    _schema = {
            'agent'          : AgentConfig,
            'cluster'        : ClusterConfig,
            'access'         : AccessConfig,
            'system'         : SystemConfig,
            }

    _defaults = {
            'agent'          : AgentConfig(),
            'cluster'        : ClusterConfig(),
            'access'         : AccessConfig(),
            'system'         : SystemConfig(),
            }


# ------------------------------------------------------------------------------

