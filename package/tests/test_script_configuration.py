from unittest import TestCase

from cloudshell.cm.customscript.domain.script_configuration import ScriptConfigurationParser


class TestScriptConfiguration(TestCase):

    def test_cannot_parse_json_without_repository_details(self):
        json = '{}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing "repositoryDetails" node.', context.exception.message)

    def test_cannot_parse_json_without_repository_url(self):
        json = '{"repositoryDetails":{}}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "repositoryDetails.url" node.', context.exception.message)

    def test_cannot_parse_json_with_an_empty_repository_url(self):
        json = '{"repositoryDetails":{"url":""}}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "repositoryDetails.url" node.', context.exception.message)

    def test_cannot_parse_json_without_hosts_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"}}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails" node.', context.exception.message)

    def test_cannot_parse_json_with_empty_host_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails" node.', context.exception.message)

    def test_cannot_parse_json_with_multiple_hosts_detalis(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{},{}]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Node "hostsDetails" must contain only one item.', context.exception.message)

    def test_cannot_parse_json_with_host_without_an_ip(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"someNode":""}]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].ip" node.', context.exception.message)

    def test_cannot_parse_json_with_host_with_an_empty_ip(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":""}]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].ip" node.', context.exception.message)

    def test_cannot_parse_json_with_host_without_an_connection_method(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":"x.x.x.x"}]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].connectionMethod" node.', context.exception.message)

    def test_cannot_parse_json_with_host_with_an_empty_connection_method(self):
        json = '{"repositoryDetails":{"url":"someurl"},"hostsDetails":[{"ip":"x.x.x.x", "connectionMethod":""}]}'
        with self.assertRaises(SyntaxError) as context:
            ScriptConfigurationParser.json_to_object(json)
        self.assertIn('Missing/Empty "hostsDetails[0].connectionMethod" node.', context.exception.message)

    def test_sanity(self):
        json = """
{
    "repositoryDetails" : {
        "url": "B",
        "username": "C",
        "password": "D"
    },
    "hostsDetails": [{
        "ip": "E",
        "username": "F",
        "password": "G",
        "accessKey": "H",
        "connectionMethod": "IiIiI",
        "parameters": [{"name":"K11","value":"K12"}, {"name":"K21","value":"K22"}]
    }]
}"""
        conf = ScriptConfigurationParser.json_to_object(json)
        self.assertEquals("B", conf.script_repo.url)
        self.assertEquals("C", conf.script_repo.username)
        self.assertEquals("D", conf.script_repo.password)
        self.assertEquals("F", conf.host_conf.username)
        self.assertEquals("G", conf.host_conf.password)
        self.assertEquals("H", conf.host_conf.access_key)
        self.assertEquals("iiiii", conf.host_conf.connection_method)
        self.assertItemsEqual('K12', conf.host_conf.parameters['K11'])
        self.assertItemsEqual('K22', conf.host_conf.parameters['K21'])