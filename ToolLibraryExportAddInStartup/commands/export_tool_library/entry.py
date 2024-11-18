import adsk.core, adsk.cam, os, json, traceback

app = adsk.core.Application.get()
ui = app.userInterface

def export_tool_library():
    try:
        # ui.messageBox("Step 1: Script is running and accessing CAM manager.")
        cam_mgr = adsk.cam.CAMManager.get()
        # ui.messageBox("Step 2: CAM Manager accessed successfully.")
        
        # Access Tool Libraries
        tool_libraries = cam_mgr.libraryManager.toolLibraries
        # ui.messageBox("Step 3: Tool Libraries accessed successfully.")

        # Access the cloud library by location
        cloud_url = tool_libraries.urlByLocation(adsk.cam.LibraryLocations.CloudLibraryLocation)
        # ui.messageBox("Step 4: Cloud library location URL obtained.")

        # Locate the specific tool library by name "name of your cloud tool library to export"
        tool_library_url = None
        for lib_url in tool_libraries.childAssetURLs(cloud_url):
            if 'name of your cloud tool library to export' in lib_url.leafName:
                tool_library_url = lib_url
                # ui.messageBox(f"Step 5: Found tool library 'name of your cloud tool library to export' at URL: {tool_library_url.pathName}")
                break
        
        # Verify if the tool library was found
        if tool_library_url:
            tool_library = tool_libraries.toolLibraryAtURL(tool_library_url)
            # ui.messageBox("Step 6: Cloud tool library 'name of your cloud tool library to export' accessed successfully.")
        else:
            # ui.messageBox("Tool library 'name of your cloud tool library to export' not found in cloud assets.")
            return  # Exit if the library isn't found

        # Define the export path
        export_folder = r"Path to your google drive folder"
        export_path = os.path.join(export_folder, f"{tool_library_url.leafName}_export.json")
        # ui.messageBox(f"Step 7: Export path set to {export_path}")

        # Check if the export folder is writable
        if not os.path.exists(export_folder):
            os.makedirs(export_folder)
            # ui.messageBox("Export folder did not exist and was created.")

        # Collect tool data to export
        tool_data = []
        for tool in tool_library:
            tool_info = {}
            try:
                tool_info["BMC"] = tool.parameters.itemByName('BMC').expression
            except:
                tool_info["BMC"] = "N/A"
            try:
                tool_info["Grade"] = tool.parameters.itemByName('GRADE').expression
            except:
                tool_info["Grade"] = "N/A"
            try:
                tool_info["comment"] = tool.parameters.itemByName('tool_comment').expression
            except:
                tool_info["comment"] = "0"
            try:
                tool_info["description"] = tool.parameters.itemByName('tool_description').expression
            except:
                tool_info["description"] = "No description"
            try:
                tool_info["product-id"] = tool.parameters.itemByName('product-id').expression
            except:
                tool_info["product-id"] = "N/A"
            try:
                tool_info["product-link"] = tool.parameters.itemByName('product-link').expression
            except:
                tool_info["product-link"] = "No link"
            try:
                tool_info["vendor"] = tool.parameters.itemByName('vendor').expression
            except:
                tool_info["vendor"] = "No vendor"
            try:
                tool_info["OAL"] = tool.parameters.itemByName('OAL').expression
            except:
                tool_info["OAL"] = "N/A"
            try:
                tool_info["DC"] = tool.parameters.itemByName('DC').expression
            except:
                tool_info["DC"] = "N/A"
            
            tool_data.append(tool_info)
        
        # Write to JSON file
        with open(export_path, 'w') as outfile:
            json.dump(tool_data, outfile, indent=4)
        
        ui.messageBox(f"Tool library exported successfully to {export_path}")

    except Exception as e:
        ui.messageBox(f"Error during export: {traceback.format_exc()}")

def command_execute_handler(args):
    export_tool_library()

def start():
    export_tool_library()

def stop():
    print("Tool Library Export command stopped.")
