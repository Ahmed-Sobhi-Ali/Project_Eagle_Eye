import os
import subprocess
import re
import shutil
from rich import print
from rich.panel import Panel
from rich.console import Console
from rich.style import Style
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn

# Create console instance
console = Console()

# Define colors for output
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
OKYELLOW = f"{BOLD}{WARNING}"
OKRED = f"{BOLD}{FAIL}"
RESET = f"{ENDC}"

from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.rule import Rule

console = Console()

def print_banner():
    """Prints the banner for the script."""
    banner = f"""{OKBLUE}
       ████████ ██████  ███████ ██    ██ ███████ ██████  
           ██    ██   ██ ██      ██    ██ ██      ██   ██ 
          ██    ██████  █████   ██    ██ █████   ██████  
          ██    ██   ██ ██       ██  ██  ██      ██   ██ 
          ██    ██   ██ ███████   ████   ███████ ██   ██ 
                                                                                        
                                                               {ENDC}
                    {OKBLUE}Created by Zierax{ENDC}
        {OKYELLOW}The Advanced Android Application Analysis Tool{RESET}
    """
    
    console.print(Panel(
        Align.center(banner),
        border_style="blue",
        title=f"{OKBLUE}ReverseAPK v1.1{ENDC}",
        title_align="right",
    ))

def print_section_header(message):
    """Prints a section header with consistent formatting."""
    console.print()
    console.print(Rule(f"{OKYELLOW}{message}{RESET}", style="yellow", no_wrap=True))
    console.print()


def check_dependencies():
    """Checks for required dependencies."""
    deps = ["unzip", "smali", "apktool", "d2j-dex2jar", "jadx"]
    for dep in deps:
        if not shutil.which(dep):
            console.print(f"{FAIL}Command: {dep} not found.{ENDC}\n")
            console.print(f"Use {OKGREEN}.install{ENDC} to install dependencies.\n")
            exit(1)

def unpack_apk(apk_path):
    """Unpacks the APK file."""
    print_section_header("Unpacking APK file")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Unpacking APK...", total=None)
        subprocess.run(["unzip", apk_path, "-d", f"{apk_path}-unzipped/"])
        subprocess.run(["baksmali", "d", f"{apk_path}-unzipped/classes.dex", "-o", f"{apk_path}-unzipped/classes.dex.out/"], stderr=subprocess.DEVNULL)

def convert_to_jar(apk_path):
    """Converts the APK to a Java JAR file."""
    print_section_header("Converting APK to Java JAR file")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Converting APK to JAR...", total=None)
        subprocess.run(["d2j-dex2jar", apk_path, "-o", f"{apk_path}.jar", "--force"])

def decompile_with_jadx(apk_path):
    """Decompiles the APK using Jadx."""
    print_section_header("Decompiling using Jadx")
    num_cores = int(subprocess.check_output(["grep", "-c", "^processor", "/proc/cpuinfo"]).decode().strip())
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Decompiling APK...", total=None)
        subprocess.run(["jadx", apk_path, "-j", str(num_cores), "-d", f"{apk_path}-jadx/"], stderr=subprocess.DEVNULL)

def unpack_with_apktool(apk_path):
    """Unpacks the APK using APKTool."""
    print_section_header("Unpacking using APKTool")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Unpacking APK with APKTool...", total=None)
        subprocess.run(["apktool", "d", apk_path, "-o", f"{apk_path}-unpacked/", "-f"])

def display_apk_files(apk_path):
    """Displays APK files."""
    print_section_header("Displaying APK files")
    subprocess.run(["find", apk_path, "-type", "f", "-exec", "egrep", "'apk|class'", "{}", ";"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_oauth_secrets(apk_path):
    """Searches for OAuth secrets."""
    print_section_header("Searching for OAuth secrets")
    subprocess.run(["find", apk_path, "-type", "f", "-exec", "egrep", "-i", "'oauth'", "{}", ";"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_androidmanifest(apk_path):
    """Displays the AndroidManifest.xml file."""
    print_section_header("Displaying AndroidManifest.xml")
    with open(f"{apk_path}-unpacked/AndroidManifest.xml", "r") as f:
        print(f.read())

def display_package_info(apk_path):
    """Displays package information from AndroidManifest.xml."""
    print_section_header("Displaying Package Info in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'package='", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_activities(apk_path):
    """Displays activities from AndroidManifest.xml."""
    print_section_header("Displaying Activities in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'activity '", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_services(apk_path):
    """Displays services from AndroidManifest.xml."""
    print_section_header("Displaying Services in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'service '", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_content_providers(apk_path):
    """Displays content providers from AndroidManifest.xml."""
    print_section_header("Displaying Content Providers in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'provider'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_broadcast_receivers(apk_path):
    """Displays broadcast receivers from AndroidManifest.xml."""
    print_section_header("Displaying Broadcast Receivers in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'receiver'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_intent_filter_actions(apk_path):
    """Displays intent filter actions from AndroidManifest.xml."""
    print_section_header("Displaying Intent Filter Actions in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'action|category'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_permissions(apk_path):
    """Displays permissions from AndroidManifest.xml."""
    print_section_header("Displaying Permissions in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'android.permission'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_exports(apk_path):
    """Displays exports from AndroidManifest.xml."""
    print_section_header("Displaying Exports in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'exported=\"true\"'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_backups(apk_path):
    """Displays backups from AndroidManifest.xml."""
    print_section_header("Displaying Backups in AndroidManifest.xml")
    subprocess.run(["egrep", "-i", "'backup'", f"{apk_path}-unpacked/AndroidManifest.xml"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_device_id_references(apk_path):
    """Searches for DeviceId references."""
    print_section_header("Searching for DeviceId references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'getDeviceId'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_android_intent_references(apk_path):
    """Searches for android.intent references."""
    print_section_header("Searching for android.intent references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'android\.intent'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_intent_references(apk_path):
    """Searches for Intent references."""
    print_section_header("Searching for Intent references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'intent\.'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_command_execution_references(apk_path):
    """Searches for command execution references."""
    print_section_header("Searching for command execution references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'Runtime.getRuntime\(\).exec'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_sqlitedatabase_references(apk_path):
    """Searches for SQLiteDatabase references."""
    print_section_header("Searching for SQLiteDatabase references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'SQLiteDatabase'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_log_references(apk_path):
    """Searches for Log.d references."""
    print_section_header("Searching for Log.d references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'log\.d|Log\.'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def display_content_providers_references(apk_path):
    """Displays content provider references."""
    print_section_header("Displaying Content Providers")
    subprocess.run(["egrep", "-nH", "'content://'", "-R", apk_path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'://'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_broadcast_receiver_references(apk_path):
    """Searches for Broadcast Receiver references."""
    print_section_header("Searching for Broadcast Receiver references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'BroadcastReceiver|onReceive|sendBroadcast'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_service_references(apk_path):
    """Searches for Service references."""
    print_section_header("Searching for Service references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'stopService|startService'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_file_references(apk_path):
    """Searches for file:// references."""
    print_section_header("Searching for file:// references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'file://'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_getsharedpreferences_references(apk_path):
    """Searches for getSharedPreferences references."""
    print_section_header("Searching for getSharedPreferences references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "getSharedPreferences", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_getexternal_references(apk_path):
    """Searches for getExternal references."""
    print_section_header("Searching for getExternal references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-iH", "getExternal", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_crypto_references(apk_path):
    """Searches for Crypto references."""
    print_section_header("Searching for Crypto references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'crypto\.'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_messagedigest_references(apk_path):
    """Searches for MessageDigest references."""
    print_section_header("Searching for MessageDigest references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'MessageDigest'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_java_util_random_references(apk_path):
    """Searches for java.util.Random references."""
    print_section_header("Searching for java.util.Random references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'java\.util\.Random'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_base64_references(apk_path):
    """Searches for Base64 references."""
    print_section_header("Searching for Base64 references")
    for filename in find_java_files(f"{apk_path}-jadx/"):
        subprocess.run(["egrep", "-nH", "'Base64'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_hex_references(apk_path):
    """Searches for Hex references."""
    print_section_header("Searching for Hex references")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for Hex references...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "'Hex|hex\\.'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_hardcoded_secrets(apk_path):
    """Searches for hardcoded secrets."""
    print_section_header("Searching for hardcoded secrets")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for hardcoded secrets...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-inH", "'secret|password|username'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_sensitive_information(apk_path):
    """Searches for sensitive information."""
    print_section_header("Searching for sensitive information")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for sensitive information...", total=None)
        subprocess.run(["strings", apk_path, ">", f"{apk_path}-strings.txt"])

def search_urls(apk_path):
    """Searches for URLs."""
    print_section_header("Searching for URLs")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for URLs...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "'http:|https:'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_http_headers(apk_path):
    """Searches for HTTP headers."""
    print_section_header("Searching for HTTP headers")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for HTTP headers...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "'addHeader'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_udp_tcp_sockets(apk_path):
    """Searches for UDP and TCP sockets."""
    print_section_header("Searching for UDP and TCP sockets")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for UDP and TCP sockets...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "'\\.connect\\(|\\.disconnect|serverSocket|DatagramSocket'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_client_certificates(apk_path):
    """Searches for client certificates."""
    print_section_header("Searching for client certificates")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for client certificates...", total=None)
        subprocess.run(["find", f"{apk_path}-unzipped/", "-type", "f", "-exec", "egrep", "'\\.pkcs|\\.p12|\\.cer|\\.der'", "{}", ";"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_ssl_certificate_pinning(apk_path):
    """Searches for SSL certificate pinning."""
    print_section_header("Searching for SSL certificate pinning")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for SSL certificate pinning...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "getCertificatePinningSSL", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_ssl_connections(apk_path):
    """Searches for SSL connections."""
    print_section_header("Searching for SSL connections")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for SSL connections...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "'ssl\\.SSL'", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_webview_activity(apk_path):
    """Searches for WebView activity."""
    print_section_header("Searching for WebView activity")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for WebView activity...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "WebView", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_addjavascripinterface_references(apk_path):
    """Searches for addJavascriptInterface references."""
    print_section_header("Searching for addJavascriptInterface references")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for addJavascriptInterface references...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "addJavascriptInterface", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_setjavascriptenabled_references(apk_path):
    """Searches for setJavaScriptEnabled references."""
    print_section_header("Searching for setJavaScriptEnabled references")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for setJavaScriptEnabled references...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "setJavaScriptEnabled", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_setallowfileaccess_references(apk_path):
    """Searches for setAllowFileAccess references."""
    print_section_header("Searching for setAllowFileAccess references")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for setAllowFileAccess references...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "setAllow", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

def search_setsavepassword_references(apk_path):
    """Searches for setSavePassword references."""
    print_section_header("Searching for setSavePassword references")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Scanning for setSavePassword references...", total=None)
        for filename in find_java_files(f"{apk_path}-jadx/"):
            subprocess.run(["egrep", "-nH", "setSavePassword", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            
def find_java_files(directory):
    """Finds all Java files in a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                yield os.path.join(root, file)

def main():
    """Main function for the script."""
    print_banner()
    check_dependencies()

    if len(os.sys.argv) < 2:
        print(f"{OKRED}Usage:{RESET} ./reverse-apk <path_to_apk>\n")
        exit(1)

    apk_path = os.sys.argv[1]

    unpack_apk(apk_path)
    convert_to_jar(apk_path)
    decompile_with_jadx(apk_path)
    unpack_with_apktool(apk_path)

    display_apk_files(apk_path)
    search_oauth_secrets(apk_path)
    display_androidmanifest(apk_path)
    display_package_info(apk_path)
    display_activities(apk_path)
    display_services(apk_path)
    display_content_providers(apk_path)
    display_broadcast_receivers(apk_path)
    display_intent_filter_actions(apk_path)
    display_permissions(apk_path)
    display_exports(apk_path)
    display_backups(apk_path)

    search_device_id_references(apk_path)
    search_android_intent_references(apk_path)
    search_intent_references(apk_path)
    search_command_execution_references(apk_path)
    search_sqlitedatabase_references(apk_path)
    search_log_references(apk_path)
    display_content_providers_references(apk_path)
    search_broadcast_receiver_references(apk_path)
    search_service_references(apk_path)
    search_file_references(apk_path)
    search_getsharedpreferences_references(apk_path)
    search_getexternal_references(apk_path)
    search_crypto_references(apk_path)
    search_messagedigest_references(apk_path)
    search_java_util_random_references(apk_path)
    search_base64_references(apk_path)
    search_hex_references(apk_path)
    search_hardcoded_secrets(apk_path)
    search_sensitive_information(apk_path)
    search_urls(apk_path)
    search_http_headers(apk_path)
    search_udp_tcp_sockets(apk_path)
    search_client_certificates(apk_path)
    search_ssl_certificate_pinning(apk_path)
    search_ssl_connections(apk_path)
    search_webview_activity(apk_path)
    search_addjavascripinterface_references(apk_path)
    search_setjavascriptenabled_references(apk_path)
    search_setallowfileaccess_references(apk_path)
    search_setsavepassword_references(apk_path)

    print(f"{OKYELLOW}DONE!{RESET}")
if __name__ == "__main__":
    main()