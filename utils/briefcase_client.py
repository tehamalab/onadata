import os
import requests
from requests.auth import HTTPDigestAuth
from urlparse import urljoin

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from odk_logger.xform_instance_parser import clean_and_parse_xml


class BriefcaseClient(object):
    def __init__(self, url, username, password, user):
        self.url = url
        self.user = user
        self.auth = HTTPDigestAuth(username, password)
        self.form_list_url = urljoin(self.url, 'formList')
        self.submission_list_url = urljoin(self.url, 'view/submissionList')
        self.download_submission_url = urljoin(self.url,
                                               'view/downloadSubmission')
        self.resumption_cursor = 0

    def download_xforms(self):
        # fetch formList
        response = requests.get(self.form_list_url, auth=self.auth)
        xmlDoc = clean_and_parse_xml(response.content)
        forms = []
        for childNode in xmlDoc.childNodes:
            if childNode.nodeName == 'xforms':
                for xformNode in childNode.childNodes:
                    if xformNode.nodeName == 'xform':
                        form_id = xformNode.getElementsByTagName('formID')[0]
                        id_string = form_id.childNodes[0].nodeValue
                        d = xformNode.getElementsByTagName('downloadUrl')[0]
                        download_url = d.childNodes[0].nodeValue
                        m = xformNode.getElementsByTagName('manifestUrl')[0]
                        manifest_url = m.childNodes[0].nodeValue
                        forms.append((id_string, download_url, manifest_url))
        # download each xform
        if forms:
            path = os.path.join(self.user.username, 'briefcase', 'forms')
            for id_string, download_url, manifest_url in forms:
                form_path = os.path.join(path, id_string, '%s.xml' % id_string)
                form_res = requests.get(download_url, auth=self.auth)
                content = ContentFile(form_res.content.strip())
                default_storage.save(form_path, content)
                manifest_res = requests.get(manifest_url, auth=self.auth)
                manifest_doc = clean_and_parse_xml(manifest_res.content)
                manifest_path = os.path.join(path, id_string, 'form-media')
                self.download_media_files(manifest_doc, manifest_path)

    def download_media_files(self, xml_doc, media_path):
        for media_node in xml_doc.getElementsByTagName('mediaFile'):
            filename_node = media_node.getElementsByTagName('filename')
            url_node = media_node.getElementsByTagName('downloadUrl')
            if filename_node and url_node:
                filename = filename_node[0].childNodes[0].nodeValue
                download_url = url_node[0].childNodes[0].nodeValue
                download_res = requests.get(download_url, auth=self.auth)
                media_content = ContentFile(download_res.content)
                path = os.path.join(media_path, filename)
                default_storage.save(path, media_content)

    def download_instances(self, form_id, cursor=0, num_entries=100):
        response = requests.get(self.submission_list_url, auth=self.auth,
                                params={'formId': form_id})
        xml_doc = clean_and_parse_xml(response.content)
        instances = []
        for child_node in xml_doc.childNodes:
            if child_node.nodeName == 'idChunk':
                for id_node in child_node.getElementsByTagName('id'):
                    if id_node.childNodes:
                        instance_id = id_node.childNodes[0].nodeValue
                        instances.append(instance_id)
        path = os.path.join(self.user.username, 'briefcase', 'forms',
                            form_id, 'instances')
        for uuid in instances:
            form_str = u'%(formId)s[@version=null and @uiVersion=null]/'\
                u'%(formId)s[@key=%(instanceId)s]' % {
                    'formId': form_id,
                    'instanceId': uuid
                }
            instance_res = requests.get(self.download_submission_url,
                                        auth=self.auth,
                                        params={'formId': form_str})
            instance_path = os.path.join(path, uuid.replace(':', ''),
                                         'submission.xml')
            content = instance_res.content.strip()
            default_storage.save(instance_path, ContentFile(content))
            instance_doc = clean_and_parse_xml(content)
            media_path = os.path.join(path, uuid.replace(':', ''))
            self.download_media_files(instance_doc, media_path)
        if xml_doc.getElementsByTagName('resumptionCursor'):
            rs_node = xml_doc.getElementsByTagName('resumptionCursor')[0]
            cursor = rs_node.childNodes[0].nodeValue
            if self.resumption_cursor != cursor:
                self.resumption_cursor = cursor
                self.download_instances(form_id, cursor)
