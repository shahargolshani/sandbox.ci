"""Unit tests for the hello_info module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.sandbox.ci.plugins.modules import hello_info
from ansible.module_utils import basic
from unittest.mock import patch, MagicMock


def run_module(module_args):
    """Helper that runs hello_info with the given args and returns the result dict."""
    with patch.object(basic.AnsibleModule, "exit_json") as mock_exit, \
         patch.object(basic.AnsibleModule, "fail_json") as mock_fail:

        mock_exit.side_effect = SystemExit(0)
        mock_fail.side_effect = SystemExit(1)

        with patch("ansible.module_utils.basic._ANSIBLE_ARGS", None):
            with patch(
                "ansible.module_utils.basic.AnsibleModule._check_arguments",
                return_value=None,
            ):
                module = basic.AnsibleModule(
                    argument_spec=dict(
                        name=dict(type="str", default="World"),
                        uppercase=dict(type="bool", default=False),
                    ),
                    params=module_args,
                )
                try:
                    hello_info.main.__globals__["AnsibleModule"] = lambda **kw: module
                    hello_info.main()
                except SystemExit:
                    pass

        if mock_exit.called:
            return mock_exit.call_args[1]
        return mock_fail.call_args[1]


class TestHelloInfo:
    def test_default_greeting(self):
        """Module returns 'Hello, World!' when no name is provided."""
        with patch(
            "ansible_collections.sandbox.ci.plugins.modules.hello_info.AnsibleModule"
        ) as mock_module_cls:
            mock_module = MagicMock()
            mock_module.params = {"name": "World", "uppercase": False}
            mock_module_cls.return_value = mock_module

            hello_info.main()

            mock_module.exit_json.assert_called_once_with(
                changed=False,
                message="Hello, World!",
                name="World",
                uppercase=False,
            )

    def test_custom_name(self):
        """Module uses the provided name in the greeting."""
        with patch(
            "ansible_collections.sandbox.ci.plugins.modules.hello_info.AnsibleModule"
        ) as mock_module_cls:
            mock_module = MagicMock()
            mock_module.params = {"name": "Ansible", "uppercase": False}
            mock_module_cls.return_value = mock_module

            hello_info.main()

            mock_module.exit_json.assert_called_once_with(
                changed=False,
                message="Hello, Ansible!",
                name="Ansible",
                uppercase=False,
            )

    def test_uppercase_flag(self):
        """Module uppercases the message when uppercase=True."""
        with patch(
            "ansible_collections.sandbox.ci.plugins.modules.hello_info.AnsibleModule"
        ) as mock_module_cls:
            mock_module = MagicMock()
            mock_module.params = {"name": "SCOM", "uppercase": True}
            mock_module_cls.return_value = mock_module

            hello_info.main()

            mock_module.exit_json.assert_called_once_with(
                changed=False,
                message="HELLO, SCOM!",
                name="SCOM",
                uppercase=True,
            )

    def test_never_reports_changed(self):
        """Module is read-only and must never set changed=True."""
        with patch(
            "ansible_collections.sandbox.ci.plugins.modules.hello_info.AnsibleModule"
        ) as mock_module_cls:
            mock_module = MagicMock()
            mock_module.params = {"name": "Test", "uppercase": False}
            mock_module_cls.return_value = mock_module

            hello_info.main()

            call_kwargs = mock_module.exit_json.call_args[1]
            assert call_kwargs["changed"] is False
