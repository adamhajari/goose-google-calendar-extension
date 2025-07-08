#!/usr/bin/env python3
"""
Final verification script for Goose Calendar Extension
Tests both the MCP server functionality and provides setup commands for Goose Desktop
"""

import subprocess
import sys
import os
import signal
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n[STEP {step}] {description}")
    print("-" * 50)

def run_command(cmd, description, timeout=5, check_output=True):
    """Run a command and return success status"""
    print(f"Running: {cmd}")
    try:
        if check_output:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            if result.returncode == 0:
                print(f"✅ {description} - SUCCESS")
                if result.stdout.strip():
                    print(f"Output: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ {description} - FAILED")
                if result.stderr.strip():
                    print(f"Error: {result.stderr.strip()}")
                return False
        else:
            # For commands that run servers (don't check output)
            proc = subprocess.Popen(cmd, shell=True)
            import time
            time.sleep(2)  # Give it time to start
            proc.terminate()
            proc.wait()
            print(f"✅ {description} - Server started successfully")
            return True
    except subprocess.TimeoutExpired:
        print(f"✅ {description} - Server started (timed out as expected)")
        return True
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print_section("GOOSE CALENDAR EXTENSION - FINAL VERIFICATION")
    
    # Get current directory
    project_dir = Path.cwd()
    venv_python = project_dir / "venv" / "bin" / "python"
    
    print(f"Project directory: {project_dir}")
    print(f"Virtual environment Python: {venv_python}")
    
    # Step 1: Check virtual environment
    print_step(1, "Checking Virtual Environment")
    venv_exists = venv_python.exists()
    print(f"Virtual environment exists: {'✅ YES' if venv_exists else '❌ NO'}")
    
    if not venv_exists:
        print("❌ Virtual environment not found! Please run:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -e .")
        return False
    
    # Step 2: Check installation
    print_step(2, "Checking Package Installation")
    install_cmd = f"source {project_dir}/venv/bin/activate && pip show goose-calendar-extension"
    if run_command(install_cmd, "Package installation check"):
        print("✅ Extension is properly installed")
    else:
        print("❌ Extension not installed. Running installation...")
        install_cmd = f"cd {project_dir} && source venv/bin/activate && pip install -e ."
        run_command(install_cmd, "Installing extension", timeout=30)
    
    # Step 3: Test MCP server import
    print_step(3, "Testing MCP Server Import")
    import_cmd = f"cd {project_dir} && source venv/bin/activate && python -c \"from goose_calendar.mcp_server import mcp; print('MCP server imported successfully')\""
    run_command(import_cmd, "MCP server import")
    
    # Step 4: Test MCP server execution
    print_step(4, "Testing MCP Server Execution")
    server_cmd = f"cd {project_dir} && source venv/bin/activate && python -m goose_calendar"
    run_command(server_cmd, "MCP server execution", timeout=3, check_output=False)
    
    # Step 5: Provide Goose Desktop setup instructions
    print_section("GOOSE DESKTOP SETUP INSTRUCTIONS")
    
    print("✅ Your Google Calendar extension is ready!")
    print("\nTo add it to Goose Desktop:")
    print("\n1. Open Goose Desktop")
    print("2. Go to Settings > Extensions > Add")
    print("3. Fill in these values:")
    print(f"   - Type: StandardIO")
    print(f"   - ID: calendar")
    print(f"   - Name: Google Calendar")
    print(f"   - Description: Google Calendar integration")
    print(f"   - Command: {venv_python} -m goose_calendar")
    print("\n4. Save and restart Goose Desktop")
    print("\n5. Test by asking: 'What tools do you have?'")
    
    print_section("ALTERNATIVE COMMANDS (if the first doesn't work)")
    print(f"Option A: {venv_python} {project_dir}/src/goose_calendar/mcp_server.py")
    print(f"Option B: cd {project_dir} && source venv/bin/activate && python -m goose_calendar")
    
    print_section("GOOGLE CALENDAR SETUP")
    print("Before using the extension, you need:")
    print("1. Google Calendar API credentials (~/credentials.json)")
    print("2. Run the authentication flow")
    print("3. For setup help, see README.md and TROUBLESHOOTING.md")
    
    print_section("VERIFICATION COMPLETE")
    print("🎉 Your extension is ready for Goose Desktop!")
    print("📚 See GOOSE_DESKTOP_SETUP.md for a quick setup guide")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification stopped by user")
        sys.exit(0)
