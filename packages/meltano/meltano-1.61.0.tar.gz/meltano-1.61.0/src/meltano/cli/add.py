import os
import yaml
import json
import click
import sys
import logging
from urllib.parse import urlparse
from typing import List

from . import cli
from .params import project
from .utils import CliError, add_plugin, add_related_plugins, install_plugins
from meltano.core.plugin import PluginType
from meltano.core.project_plugins_service import ProjectPluginsService
from meltano.core.project_add_service import ProjectAddService
from meltano.core.project_add_custom_service import ProjectAddCustomService
from meltano.core.plugin_install_service import PluginInstallReason


@cli.command()
@click.argument("plugin_type", type=click.Choice(PluginType.cli_arguments()))
@click.argument("plugin_name", nargs=-1, required=True)
@click.option("--variant")
@click.option("--custom", is_flag=True)
@click.option("--include-related", is_flag=True)
@project()
@click.pass_context
def add(ctx, project, plugin_type, plugin_name, variant=None, **flags):
    plugin_type = PluginType.from_cli_argument(plugin_type)
    plugin_names = plugin_name  # nargs=-1

    plugins_service = ProjectPluginsService(project)

    if flags["custom"]:
        if plugin_type in (
            PluginType.TRANSFORMERS,
            PluginType.TRANSFORMS,
            PluginType.ORCHESTRATORS,
        ):
            raise CliError(f"--custom is not supported for {ctx.invoked_subcommand}")

        add_service_class = ProjectAddCustomService
    else:
        add_service_class = ProjectAddService

    add_service = add_service_class(project, plugins_service=plugins_service)

    plugins = [
        add_plugin(
            project, plugin_type, plugin_name, variant=variant, add_service=add_service
        )
        for plugin_name in plugin_names
    ]

    related_plugin_types = [PluginType.FILES]
    if flags["include_related"]:
        related_plugin_types = list(PluginType)

    related_plugins = add_related_plugins(
        project, plugins, add_service=add_service, plugin_types=related_plugin_types
    )
    plugins.extend(related_plugins)

    # We will install the plugins in reverse order, since dependencies
    # are listed after their dependents in `related_plugins`, but should
    # be installed first.
    plugins.reverse()

    success = install_plugins(project, plugins, reason=PluginInstallReason.ADD)

    if not success:
        raise CliError("Failed to install plugin(s)")

    printed_empty_line = False
    for plugin in plugins:
        docs_url = plugin.docs or plugin.repo
        if not docs_url:
            continue

        if not printed_empty_line:
            click.echo()
            printed_empty_line = True

        click.echo(
            f"To learn more about {plugin.type.descriptor} '{plugin.name}', visit {docs_url}"
        )
