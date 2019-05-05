import os
import shutil



import requests
from ptest.assertion import assert_equals
from ptest.plogger import preporter

JENKINS_HOST_ANDROID = "http://10.128.42.168:8080"
USERNAME = 'mobileauto'
PASSWORD = 'password'


class Jenkins:
    def __init__(self):
        self._session = self.get_login_session()

        self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-ec-testing/lastSuccessfulBuild/api/json"
        #self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-android-release/lastSuccessfulBuild/api/json"

        #self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-android-release/154/api/json"
        #self.Jenkins_build_url = JENKINS_HOST_ANDROID +  "/view/Engage/job/engage-android-webcn1us1/23/api/json"



        # if type == "release":
        #
        #     self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-android-release/lastSuccessfulBuild/api/json"
        # elif type == "daily":
        #     self.Jenkins_build_url = JENKINS_HOST_ANDROID + "/view/Engage/job/engage-ec-testing/lastSuccessfulBuild/api/json"

    def get_login_session(self):
        data = {
            'j_username': USERNAME,
            'j_password': PASSWORD,
            'from': '/',
            'Submit': 'log in',
            'json': '{"j_username": "mobileauto", "j_password": "password", "remember_me": false, "from": "/"}'
        }

        session = requests.Session()
        response = session.post(JENKINS_HOST_ANDROID + '/j_acegi_security_check', data=data)

        try:
            assert_equals(response.status_code, 200)

            return session
        except:
            raise ("cannot login jenkins server!")

    def get_build_url(self):
        preporter.info(self.Jenkins_build_url)

        try:
            builds_urls = self._session.get(self.Jenkins_build_url)

            builds = [each_build['relativePath'] for each_build in builds_urls.json()['artifacts']]

            #preporter.info("build detail info: \n %s " % builds)


            apk_url = [builds_urls.json()['url'].replace("165","168") + "artifact/" + build for build in builds]

            preporter.info("build detail info url: \n %s " % apk_url[0])

            return apk_url


        except:
            preporter.info(
                "cannot access the {url} of jenkins, please check your jenkins!".format(url=self.Jenkins_build_url))

    def check_folder(sef, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    def is_apk_exist(self, path):
        if os.path.isfile(path) and path.endswith('apk'):
            preporter.info("{file} exist".format(file=path))
            return True

        else:
            preporter.info("{file} does't exist".format(file=path))
            return False

    def download_file(self, url, path):
        try:
            file = self._session.get(url).content
            with open(path, 'wb') as f:
                f.write(file)
        except:
            preporter.info("Download file from jenkins {url} fail, please check your jenkins".format(url=url))

    def download_build(self, apk_local_path):
        apk_url = self.get_build_url()
        self.check_folder(apk_local_path)
        for url in apk_url:
            file_path = os.path.join(apk_local_path, url.split("/")[-1])
            self.download_file(url, file_path)

            if self.is_apk_exist(file_path):
                preporter.info("Download file {file} success!".format(file=file_path))

            else:
                preporter.info("Download file {file} fail!".format(file=file_path))


if __name__ == '__main__':
    apk_path = "/Users/anderson/backup/ec_daily"
    jen = Jenkins()
    jen.download_build(apk_path)
