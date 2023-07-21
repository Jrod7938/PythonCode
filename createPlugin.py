import os

# Define the Libraries class with the necessary constant values
class Libraries:
    pf4j = "org.pf4j:pf4j:3.7.0"

def createPlugin():
    default_dir = "/Users/jancarlosrodriguez/Documents/Code/Kotlin/dc-plugins"

    # Get user input
    fileName = input("Enter the fileName: ")
    pluginName = input("Enter the pluginName: ")
    pluginDescription = input("Enter the pluginDescription: ")

    fileNameCapital = fileName.capitalize()

    # Create folder structure
    folder_path = os.path.join(default_dir, fileName)
    os.makedirs(folder_path, exist_ok=True)

    src_path = os.path.join(folder_path, "src", "main", "java", "net", "unethicalite", "plugins", fileName)
    os.makedirs(src_path, exist_ok=True)

    # Create files and write contents
    with open(os.path.join(src_path, f"{fileNameCapital}Plugin.kt"), "w") as file:
        file.write(f'package net.unethicalite.plugins.{fileName}\n\n'
                   
                   f'import lombok.extern.slf4j.Slf4j\n'
                   f'import net.runelite.api.events.GameTick\n'
                   f'import net.runelite.client.eventbus.Subscribe\n'
                   f'import net.runelite.client.plugins.PluginDescriptor\n'
                   f'import net.unethicalite.api.plugins.LoopedPlugin\n'
                   f'import org.pf4j.Extension\n\n'
                   
                   f'@Extension\n'
                   f'@PluginDescriptor(name = "{pluginName}", description = "{pluginDescription}", enabledByDefault = false)\n'
                   f'@Slf4j\n'
                   f'class {fileNameCapital}: LoopedPlugin() {{\n'
                   f'    override fun startUp() {{\n'
                   f'    \n'
                   f'    }}\n\n'

                   f'    @Subscribe\n'
                   f'    private fun onGameTick(e: GameTick) {{\n'
                   f'    \n'
                   f'    }}\n\n'

                   f'    override fun loop(): Int {{\n'
                   f'        return 0\n'
                   f'    }}\n'
                   f'}}')

    with open(os.path.join(folder_path, f"{fileName}.gradle.kts"), "w") as file:
        file.write(f'version = "0.0.1"\n\n'
                   f'project.extra["PluginName"] = "{pluginName}"\n'
                   f'project.extra["PluginDescription"] = "{pluginDescription}"\n\n'

                   f'plugins{{\n'
                   f'   kotlin("kapt")\n'
                   f'}}\n\n'

                   f'dependencies{{\n'
                   f'   kapt(Libraries.pf4j)\n'
                   f'}}\n\n'
                   
                   f'tasks {{\n'
                   f'    jar {{\n'
                   f'        manifest {{\n'
                   f'            attributes(mapOf(\n'
                   f'                "Plugin-Version" to project.version,\n'
                   f'                "Plugin-Id" to nameToId(project.extra["PluginName"] as String),\n'
                   f'                "Plugin-Provider" to project.extra["PluginProvider"],\n'
                   f'                "Plugin-Description" to project.extra["PluginDescription"],\n'
                   f'                "Plugin-License" to project.extra["PluginLicense"]\n'
                   f'            ))\n'
                   f'        }}\n'
                   f'    }}\n'
                   f'}}')

    print(f"Folder and file creation completed for '{fileName}' plugin.")

if __name__ == "__main__":
    createPlugin()
