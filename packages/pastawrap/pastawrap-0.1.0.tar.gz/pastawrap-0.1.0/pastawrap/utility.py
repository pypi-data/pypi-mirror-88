from rpy2.robjects.packages import importr
import rpy2.robjects as ro


def r_ggsave(*args, **kwargs):
    """A wrapper for R ggplot2's ggsave function.

    All parameters are passed to the respective R function.
    For more information, please refer to the ggplot2 documentation.

    :param *args: Arguments, passed verbatim to the respective R function.
    :param *kwargs: Keyword arguments, passed verbatim to the respective R function.

    :return: None"""
    ro.r.ggsave(*args, **kwargs)
    return


def r_install_packages(package):
    """A wrapper for R utils install.packages function.

    All parameters are passed to the respective R function.
    For more information, please refer to the R utils documentation.

    :param *args: Arguments, passed verbatim to the respective R function.
    :param *kwargs: Keyword arguments, passed verbatim to the respective R function.

    :return: None"""
    utils = importr("utils")
    utils.install_packages(package)
    return
