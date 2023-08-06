#!/usr/bin/python

"""
this script is for UFES L7policy Validator automation build and get its artifacts
"""
import os
import sys
import argparse

from io import StringIO
from jenkinsapi.custom_exceptions import ArtifactBroken
from jenkinsapi.jenkins import Jenkins


class JenkinsApplication:
    def __init__(self, url, job_name, verbose=True):
        self.url = url
        self.job_name = job_name
        self.params = {}
        self.files = {}
        self.jenkins = None
        self.job = None
        self.invoker = None
        self.verbose = verbose

    def __trace(self, message):
        if self.verbose:
            print(message)

    def add_param(self, param_name, param_value):
        self.params[param_name] = param_value
        self.__trace("add param: name=%s, value=%s" % (param_name, param_value))

    def add_params(self, param_dict):
        for name, value in param_dict.items():
            self.add_param(name, value)

    def add_file(self, remote_file_name, local_file_name):
        with open(local_file_name, "rb") as f:
            self.files[remote_file_name] = StringIO(f.read().decode())
            self.__trace("add file: remote=%s, local=%s" % (remote_file_name, local_file_name))

    def add_files(self, file_dict):
        for remote, local in file_dict.items():
            self.add_file(remote, local)

    def init_job(self):
        if self.job is not None:
            return
        self.__trace("start init job ...")
        self.jenkins = Jenkins(self.url)
        self.job = self.jenkins[self.job_name]
        self.__trace("init job done")

    def last_build_number(self):
        if self.job is None:
            self.init_job()
        return self.job.get_last_good_buildnumber()

    def invoke(self, delay=1):
        if self.job is None:
            self.init_job()
        self.__trace("start invoke new build ...")
        self.invoker = self.job.invoke(block=True, build_params=self.params, files=self.files, delay=delay)
        self.__trace("new build was invoked")

    def wait_complete(self, timeout=60):
        if self.invoker is None:
            return
        if self.invoker.is_queued() or self.invoker.is_running():
            self.__trace("start wait build done ...")
            self.invoker.block_until_complete(delay=timeout)
            self.__trace("wait build done")

    def invoke_and_wait_complete(self, timeout=60):
        self.invoke()
        self.wait_complete(timeout=timeout)

    def download_artifacts(self, local_dir, force_download=True):
        if self.invoker is None:
            return

        artifacts = self.invoker.get_build().get_artifact_dict()

        for name, _ in artifacts.items():
            self.__trace("try to download remote file: %s" % name)

            local_file = os.path.sep.join([local_dir, os.path.basename(name)])

            if force_download and os.path.exists(local_file):
                os.remove(local_file)
                self.__trace("remove local file: %s" % local_file)
            try:
                artifacts[name].save_to_dir(local_dir)
            except ArtifactBroken:
                pass

            if os.path.exists(local_file):
                self.__trace("download local file success")
            else:
                self.__trace("download local file failed")


def jenkins_validate(clustername, web_type, localpath_to_artifact_dir, timeout='2', pull_method="STATIC", total_request="1000",
                     file_filter=None, token=None, jenkins_server=None):
    clustername_list = ["AMS", "DUS", "FRA", "LHR", "LAX", "SJC", "MDW", "DFW", "MIA", "EWR", "Wave2", "SIN", "HKG",
                        "SYD", "MEL", "LVSAZ01", "RNOAZ03", "SLCAZ01","MRS"]
    if clustername not in clustername_list:
        print("\033[1;35m%s is not a valid cluster name, please use one of them: %s!\033[0m" % (clustername, clustername_list))
        sys.exit("sorry, goodbye")

    jobname_list = ['UFES', web_type, "L7PolicyValidator"]
    job_name = "-".join(jobname_list)
    print("job name:", job_name)

    validator = JenkinsApplication(jenkins_server, job_name)

    if web_type == "DWEB":
        validator.add_param("Timeout", timeout)
        validator.add_param("POP", clustername)
        validator.add_params({"Total_Requests": total_request, "L7_Rules_Pull_Method": pull_method})
        if pull_method == "LBMS":
            if token == "None":
                print("please upload your token file.")
                sys.exit(1)
            validator.add_file("EnvoyConfigGenerator/keystone_token.txt", token)

    elif web_type == "MWEB":
        if pull_method != "LBMS":
            if token == "None":
               print("please set pull_method to 'LBMS', and upload your keystone tokens")
               sys.exit()
            else:
                print("please set pull_method to 'LBMS'")
                sys.exit()
        if pull_method == "LBMS":
            if token is None:
                print("plese uplaod your token file.")
                sys.exit()

        validator.add_file("EnvoyConfigGenerator/keystone_token.txt", token)
        validator.add_params({"Total_Requests": total_request, "Timeout": timeout, "POP": clustername, "L7_Rules_Pull_Method": pull_method})
    else:
        print("\033[1;35m%s is invalid web type,please use DWEB or MWEB\033[0m!" % web_type)
        sys.exit("sorry, goodbye")

    validator.invoke_and_wait_complete(200)
    validator.download_artifacts(localpath_to_artifact_dir)


#jenkins_validate(clustername='AMS', web_type='scd', localpath_to_artifact_dir='/Users/xuenwang/validator_test/20201203')
if __name__ == '__main__':
    jenkins_validate(clustername='AMS', web_type='DWEB', jenkins_server='http://10.148.183.183:8080', localpath_to_artifact_dir='/Users/xuenwang/validator_test/20201203/', total_request="500")
