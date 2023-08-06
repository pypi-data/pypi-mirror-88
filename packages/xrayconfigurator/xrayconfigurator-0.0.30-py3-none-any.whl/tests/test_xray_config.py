import logging
import unittest
from unittest import TestCase

from unittest.mock import Mock, patch, call

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core import xray_recorder

from libs.xray.xray_configurator.xray_configurator import XRayConfigurator


class ConfigTestCase(TestCase):
    @patch("libs.xray.xray_configurator.xray_configurator.patch_all")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayMiddleware")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    def test_no_xray_section(self, mock_alchemy, mock_middleware, mock_patch_all):
        class ConfigMock:
            XRAY_ENABLED = False
            XRAY_SERVICE_NAME = "test-service-name"
            XRAY_PLUGINS = "test"
            XRAY_SAMPLING = True
            XRAY_STREAM_SQL = True
            XRAY_DAEMON = "daemon:200"
            XRAY_PATCH_MODULES = None
            XRAY_LOGGING_ENABLED = False
            XRAY_SQLALCHEMY = False
            XRAY_MIDDLEWARE = False
            XRAY_SENTRY_LOGGING = False

        XRayConfigurator(ConfigMock(), Mock())
        self.assertFalse(global_sdk_config.sdk_enabled())
        mock_alchemy.assert_not_called()
        mock_middleware.assert_not_called()
        mock_patch_all.assert_not_called()

    @patch("libs.xray.xray_configurator.xray_configurator.xray_recorder.configure")
    @patch("libs.xray.xray_configurator.xray_configurator.patch")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayMiddleware")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    @patch("libs.xray.xray_configurator.xray_configurator.ignore_logger")
    def test_xray(self, mock_ignore_logger, mock_alchemy, mock_middleware, mock_patch, mock_configure):
        app_mock = Mock()
        class ConfigMock:
            XRAY_ENABLED = True
            XRAY_SERVICE_NAME = 'test-service-name'
            XRAY_DAEMON = '129.0.0.0:5000'
            XRAY_PLUGINS = "'ECSPlugin', 'EC2Plugin', 'ElasticBeanstalkPlugin'"
            XRAY_SAMPLING = True
            XRAY_STREAM_SQL = True
            XRAY_SQLALCHEMY = True
            XRAY_LOGGING_ENABLED = True
            XRAY_PATCH_MODULES = "'boto3','requests'"
            XRAY_MIDDLEWARE = True
            XRAY_SENTRY_LOGGING = True

        XRayConfigurator(ConfigMock(), app_mock)
        self.assertTrue(global_sdk_config.sdk_enabled())
        mock_configure.assert_called_once_with(context_missing='LOG_ERROR', daemon_address='129.0.0.0:5000', plugins=('ECSPlugin', 'EC2Plugin', 'ElasticBeanstalkPlugin'), sampling=True, service='test-service-name', stream_sql=True)
        self.assertEqual(logging.getLogger("aws_xray_sdk").level, logging.DEBUG)

        mock_alchemy.assert_called_once_with(app_mock)
        mock_middleware.assert_called_once_with(app_mock, xray_recorder)
        mock_patch.assert_called_once_with(('boto3', 'requests'))
        mock_ignore_logger.assert_not_called()

    @patch("libs.xray.xray_configurator.xray_configurator.xray_recorder.configure")
    @patch("libs.xray.xray_configurator.xray_configurator.patch_all")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayMiddleware")
    @patch("libs.xray.xray_configurator.xray_configurator.XRayFlaskSqlAlchemy")
    @patch("libs.xray.xray_configurator.xray_configurator.ignore_logger")
    def test_xray_extensions_disabled(self, mock_ignore_logger, mock_alchemy, mock_middleware, mock_patch, mock_configure):
        app_mock = Mock()

        class ConfigMock:
            XRAY_ENABLED = True
            XRAY_SERVICE_NAME = 'test-service-name'
            XRAY_DAEMON = None
            XRAY_PLUGINS = "'ECSPlugin', 'EC2Plugin'"
            XRAY_SAMPLING = False
            XRAY_STREAM_SQL = False
            XRAY_SQLALCHEMY = False
            XRAY_LOGGING_ENABLED = False
            XRAY_PATCH_MODULES = None
            XRAY_MIDDLEWARE = False
            XRAY_SENTRY_LOGGING = False

        XRayConfigurator(ConfigMock(), app_mock)
        self.assertTrue(global_sdk_config.sdk_enabled())
        mock_configure.assert_called_once_with(context_missing='LOG_ERROR', daemon_address=None,
                                               plugins=('ECSPlugin', 'EC2Plugin'),
                                               sampling=False, service='test-service-name', stream_sql=False)
        self.assertEqual(logging.getLogger("aws_xray_sdk").level, logging.NOTSET)

        mock_alchemy.assert_not_called()
        mock_middleware.assert_not_called()
        mock_patch.assert_called_once_with()
        mock_ignore_logger.assert_has_calls([call('aws_xray_sdk'), call('aws_xray_sdk.core.emitters.udp_emitter'), call('aws_xray_sdk.core.sampling.rule_poller'), call('aws_xray_sdk.core.sampling.target_poller')])


if __name__ == "__main__":
    unittest.main()
