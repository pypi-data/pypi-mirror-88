from typing import Any, Dict, List, Optional

# from typeguard import typechecked
import typer

from devinstaller_core import lib
from devinstaller_core import dependency_graph as dg
from devinstaller_core import common_models as m


def get_req_list(
    dependency_graph: dg.DependencyGraph, requirements_list: List[str]
) -> List[str]:
    """Get the requirement list
    """
    list_of_deps = list(dependency_graph.graph.keys())
    if len(list_of_deps) == 1:
        return list_of_deps
    elif requirements_list is not None and requirements_list != []:
        return requirements_list
    else:
        return lib.get_requirement_list(dependency_graph.module_list())


class Devinstaller:
    def install(
        self,
        spec_file_path: Optional[str] = None,
        prog_file_path: Optional[str] = None,
        spec_object: Optional[Dict[Any, Any]] = None,
        platform_codename: Optional[str] = None,
        requirements_list: Optional[List[str]] = None,
    ) -> None:
        """Install the default preset and the modules which it requires."""
        validated_schema_object: m.TypeFullDocument = lib.core(
            file_path=spec_file_path, spec_object=spec_object
        )
        dependency_graph: dg.DependencyGraph = lib.create_dependency_graph(
            schema_object=validated_schema_object, platform_codename=platform_codename
        )
        req_list: List[str] = get_req_list(
            dependency_graph=dependency_graph, requirements_list=requirements_list
        )
        dependency_graph.install(req_list)
        orphan_modules_names = dependency_graph.orphan_modules
        if orphan_modules_names != set() and lib.get_user_confirmation(
            orphan_modules_names
        ):
            dependency_graph.uninstall_orphan_modules()

    def show(self, spec_file_path: Optional[str] = None,) -> None:
        """Install the default preset and the modules which it requires."""
        validated_schema_object: m.TypeFullDocument = lib.core(file_path=spec_file_path)
        dependency_graph: dg.DependencyGraph = lib.create_dependency_graph(
            schema_object=validated_schema_object, platform_codename=None
        )
        available_modules = list(dependency_graph.graph.keys())
        print("All the modules available\n")
        for i in available_modules:
            typer.secho(i, fg="cyan")

    # @typechecked
    # def run(
    #     self,
    #     interface_name: Optional[str] = None,
    #     spec_file_path: Optional[str] = None,
    #     prog_file_path: Optional[str] = None,
    #     spec_object: Optional[Dict[Any, Any]] = None,
    #     platform_codename: Optional[str] = None,
    # ) -> None:
    #     """The `run` function.

    #     This function is used for the interface block.
    #     """
    #     schema_object = self.hook.core(spec_file_path, spec_object)
    #     dev_module = self.hook.load_devfile(
    #         schema_object=schema_object, prog_file_path=prog_file_path
    #     )
    #     interface = m.get_interface(
    #         interface_list=schema_object["interfaces"], interface_name=interface_name
    #     )
    #     dependency_graph = self.hook.create_dependency_graph(
    #         schema_object=schema_object, platform_codename=platform_codename
    #     )
