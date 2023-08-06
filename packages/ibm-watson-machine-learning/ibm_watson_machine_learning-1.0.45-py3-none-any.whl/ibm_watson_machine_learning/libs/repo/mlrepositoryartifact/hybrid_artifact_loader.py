#  (C) Copyright IBM Corp. 2020.
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#       http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from  ibm_watson_machine_learning.libs.repo.util.unique_id_gen import uid_generate
import os, shutil


class HybridArtifactLoader(object):
    def load(self, artifact_queryparam):
        if artifact_queryparam is None:
           return self.extract_content(artifact_queryparam, lambda content_dir: self.load_content(content_dir))

        if artifact_queryparam is not None and artifact_queryparam == "full":
            return self.extract_content(artifact_queryparam, lambda content_dir: self.load_content(content_dir))

        if artifact_queryparam is not None and artifact_queryparam == "pipeline_model":
            return self.extract_content_json(lambda content_dir: self.load_content(content_dir))

    def extract_content(self, queryparam_val, callback):
        directory_name = 'artifact'
        try:
            shutil.rmtree(directory_name)
        except:
            pass

        try:
            id_length = 20
            dir_id = uid_generate(id_length)
            model_dir_name = directory_name + dir_id

            tar_file_name = '{}/artifact_content.tar'.format(model_dir_name)
            gz_file_name = '{}/artifact_content.tar.gz'.format(model_dir_name)

            input_stream = None
            os.makedirs(model_dir_name)
            if queryparam_val is None:
                input_stream = self.reader().read()
            if queryparam_val is not None and queryparam_val == 'full':
                input_stream = self._content_reader_gzip()
            file_content = input_stream.read()
            gz_f = open(gz_file_name, 'wb+')
            gz_f.write(file_content)
            gz_f.close()
            if queryparam_val is None:
               self.reader().close()
            return gz_file_name
        except Exception as ex:
            shutil.rmtree(model_dir_name)
            raise ex

    def extract_content_json(self, callback):
        directory_name = 'artifact'
        try:
            shutil.rmtree(directory_name)
        except:
            pass

        try:
            id_length = 20
            dir_id = uid_generate(id_length)
            model_dir_name = directory_name + dir_id

            output_file_name = '{}/pipeline_model.json'.format(model_dir_name)

            os.makedirs(model_dir_name)
            input_stream = self._content_reader_json()
            file_content = input_stream.read()
            gz_f = open(output_file_name, 'wb+')
            gz_f.write(file_content)
            gz_f.close()
            return output_file_name
        except Exception as ex:
            shutil.rmtree(model_dir_name)
            raise ex

    def _content_reader_gzip(self):
        if self._content_href is not None:
            if self._content_href.__contains__("models"):
                content_url = self._content_href + "?artifact=full"
                return self.client.repository_api.download_artifact_content(content_url, 'false', accept='application/gzip')

    def _content_reader_json(self):
        if self._content_href is not None:
            if self._content_href.__contains__("models"):
                content_url = self._content_href + "?artifact=pipeline_model"
                return self.client.repository_api.download_artifact_content(content_url, 'false', accept='application/json')
