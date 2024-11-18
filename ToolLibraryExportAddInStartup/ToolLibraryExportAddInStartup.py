from . import commands

def run(context):
    try:
        # Start the commands within the add-in
        commands.start()
    except:
        print("Failed to start ToolLibraryExportAddInStartup")

def stop(context):
    try:
        # Stop and clean up the commands within the add-in
        commands.stop()
    except:
        print("Failed to stop ToolLibraryExportAddInStartup")
