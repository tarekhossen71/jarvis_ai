
import os
import importlib.util


class PluginManager:

    def __init__(self, plugins_folder="plugins"):

        self.plugins_folder = plugins_folder
        self.plugins = []

        self.load_plugins()

    # =========================
    # Load All Plugins
    # =========================

    def load_plugins(self):

        if not os.path.exists(self.plugins_folder):
            os.makedirs(self.plugins_folder)

        for filename in os.listdir(self.plugins_folder):

            if not filename.endswith(".py"):
                continue

            if filename == "__init__.py":
                continue

            plugin_path = os.path.join(
                self.plugins_folder,
                filename
            )

            try:

                spec = importlib.util.spec_from_file_location(
                    filename[:-3],
                    plugin_path
                )

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                if hasattr(module, "get_plugin"):

                    plugin = module.get_plugin()

                    self.plugins.append(plugin)

                    print(
                        f"🔌 Plugin loaded: "
                        f"{plugin.get('name', filename)}"
                    )

            except Exception as e:

                print(
                    f"❌ Plugin failed: "
                    f"{filename} - {e}"
                )


    # =========================
    # Execute Plugin
    # =========================

    def execute(self, command):

        for plugin in self.plugins:

            # Skip disabled plugin
            if not plugin.get("enabled", True):
                continue

            keywords = plugin.get("keywords", [])

            for keyword in keywords:

                if keyword in command:

                    function = plugin.get("function")

                    if function:
                        return function(command)

        return None



    # =========================
    # List Plugins
    # =========================

    def list_plugins(self):

        return [
            plugin.get("name", "Unknown Plugin")
            for plugin in self.plugins
        ]
    
    # =========================
    # Get Plugin Details
    # =========================

    def get_plugin_details(self):

        details = []

        for plugin in self.plugins:

            details.append({
                "name": plugin.get("name", "Unknown Plugin"),
                "description": plugin.get(
                    "description",
                    "No description available."
                ),
                "enabled": plugin.get("enabled", True),
            })

        return details

    
    # =========================
    # Find Plugin
    # =========================

    def find_plugin(self, name):

        search_name = str(name).strip().lower()

        # Normalize
        search_name = search_name.replace(
            "_",
            " "
        )

        # Remove extra "plugin" from search
        search_name_without_plugin = search_name

        if search_name.endswith(" plugin"):
            search_name_without_plugin = (
                search_name[:-7].strip()
            )

        for plugin in self.plugins:

            plugin_name = str(
                plugin.get("name", "")
            ).strip().lower()

            plugin_name = plugin_name.replace(
                "_",
                " "
            )

            plugin_name_without_plugin = plugin_name

            if plugin_name.endswith(" plugin"):
                plugin_name_without_plugin = (
                    plugin_name[:-7].strip()
                )

            # Exact match
            if search_name == plugin_name:
                return plugin

            # Match without "plugin"
            if search_name_without_plugin == plugin_name_without_plugin:
                return plugin

            # Partial match
            if (
                search_name in plugin_name
                or plugin_name in search_name
            ):
                return plugin

        return None







    # =========================
    # Enable Plugin
    # =========================

    def enable_plugin(self, name):

        plugin = self.find_plugin(name)

        if not plugin:
            return f"Plugin '{name}' was not found."

        plugin["enabled"] = True

        return f"{plugin['name']} enabled successfully."


    # =========================
    # Disable Plugin
    # =========================

    def disable_plugin(self, name):

        plugin = self.find_plugin(name)

        if not plugin:
            return f"Plugin '{name}' was not found."

        plugin["enabled"] = False

        return f"{plugin['name']} disabled successfully."
    

    # =========================
    # Reload Plugins
    # =========================

    def reload_plugins(self):

        # Clear currently loaded plugins
        self.plugins = []

        # Load plugins again
        self.load_plugins()

        return f"{len(self.plugins)} plugin(s) loaded successfully."


    # =========================
    # Reload Single Plugin
    # =========================

    def reload_plugin(self, name):

        plugin = self.find_plugin(name)

        if not plugin:
            return f"Plugin '{name}' was not found."

        # Save current status
        enabled = plugin.get("enabled", True)

        # Remove old plugin
        self.plugins.remove(plugin)

        # Find plugin file
        target_file = None

        for filename in os.listdir(self.plugins_folder):

            if not filename.endswith(".py"):
                continue

            if filename == "__init__.py":
                continue

            plugin_path = os.path.join(
                self.plugins_folder,
                filename
            )

            try:

                spec = importlib.util.spec_from_file_location(
                    filename[:-3],
                    plugin_path
                )

                module = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(module)

                if hasattr(module, "get_plugin"):

                    new_plugin = module.get_plugin()

                    if new_plugin.get("name", "").lower() == name.lower():

                        new_plugin["enabled"] = enabled

                        self.plugins.append(new_plugin)

                        return (
                            f"{new_plugin['name']} "
                            f"reloaded successfully."
                        )

            except Exception as e:

                return f"Plugin reload failed: {e}"

        return f"Plugin '{name}' could not be reloaded."

    
    # =========================
    # Create Plugin
    # =========================

    def create_plugin(self, plugin_name):

        plugin_name = plugin_name.strip()

        if not plugin_name:
            return "Please provide a plugin name."

        # Safe filename
        safe_name = plugin_name.lower().replace(" ", "_")

        filename = f"{safe_name}_plugin.py"

        plugin_path = os.path.join(
            self.plugins_folder,
            filename
        )

        # Check existing plugin
        if os.path.exists(plugin_path):

            return (
                f"Plugin '{plugin_name}' "
                f"already exists."
            )

        class_name = plugin_name.title().replace(" ", "")

        plugin_code = f'''def {safe_name}(command):

        return "Hello! This is the {plugin_name} plugin."


    def get_plugin():

        return {{
            "name": "{plugin_name}",

            "description": "Custom {plugin_name} plugin.",

            "keywords": [
                "{plugin_name.lower()} plugin",
            ],

            "function": {safe_name},

            "enabled": True,
        }}
    '''

        try:

            with open(
                plugin_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(plugin_code)

            # Reload plugins
            self.reload_plugins()

            return (
                f"Plugin '{plugin_name}' "
                f"created successfully."
            )

        except Exception as e:

            return f"Plugin creation failed: {e}"


    # =========================
    # Delete Plugin
    # =========================

    def delete_plugin(self, name):

        plugin = self.find_plugin(name)

        if not plugin:
            return f"Could not find {name}."

        plugin_name = plugin.get(
            "name",
            name
        )

        # Normalize filename
        safe_name = plugin_name.lower()
        safe_name = safe_name.replace(
            " ",
            "_"
        )

        target_file = None
        
        # Expected filename
        expected_filename = (
            f"{safe_name}_plugin.py"
        )

        expected_path = os.path.join(
            self.plugins_folder,
            expected_filename
        )

        if os.path.exists(expected_path):

            target_file = expected_path

        else:

            # Fallback search
            for filename in os.listdir(
                self.plugins_folder
            ):

                if not filename.endswith(".py"):
                    continue

                if filename == "__init__.py":
                    continue

                filename_lower = filename.lower()

                if safe_name in filename_lower:

                    target_file = os.path.join(
                        self.plugins_folder,
                        filename
                    )

                    break

        if not target_file:

            return (
                f"Plugin file for "
                f"{plugin_name} was not found."
            )

        try:

            os.remove(target_file)

            if plugin in self.plugins:
                self.plugins.remove(plugin)

            return (
                f"{plugin_name} "
                f"deleted successfully."
            )

        except Exception as e:

            return (
                f"Plugin deletion failed: {e}"
            )
    



   
  


