#! /usr/bin/env python3 
# -*- coding: utf-8 -*-

# Description: generate with draw and publish /path in browser
# Author: sujit-168 su2054552689@gmail.com
# Copyright (c) 2025 by sujit-168, All Rights Reserved. 

import asyncio
import subprocess
import rospy, rospkg
import os

async def run_command(command):
    """
    Execute a command asynchronously
    :param command: Command to execute
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        print(f"Command execution failed: {command}")
        print(stderr.decode().strip())
    else:
        print(f"Command executed successfully: {command}")

async def main():
    """
    Main function to launch ROSbridge, web interface, and Rviz with delay
    """
    
    # Then launch other commands
    tasks = [
        run_command(f"xdg-open {index_filename}"),
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    rospy.init_node('path_generator_with_browser', anonymous=False)
    package_name = "path_generator"
    robot_name = rospy.get_param('~robot_name', '')

    # Get the package path
    try:
        pkg_path = rospkg.RosPack().get_path(package_name)

        # Construct the path to scripts directory
        index_filename= os.path.join(pkg_path, f"static/path_generator.html")
        print(f"index: {index_filename}")
    except rospkg.ResourceNotFound:
        rospy.logerr("Package '%s' not found" % package_name)
        exit(1)
    asyncio.run(main())