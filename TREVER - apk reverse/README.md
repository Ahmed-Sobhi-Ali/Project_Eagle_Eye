## TREVER: Advanced Android Application Analysis Tool

ReverseAPK is a powerful command-line tool designed to aid in the security analysis of Android applications. It leverages a suite of tools like `apktool`, `jadx`, and `d2j-dex2jar` to provide a comprehensive analysis of APK files.

**Features:**

* **Unpacking and Decompilation:** ReverseAPK unpacks APK files using `apktool` and decompiles them using `jadx`, providing access to the underlying Java code.
* **AndroidManifest.xml Analysis:** The tool offers functions to display various elements of the `AndroidManifest.xml` file, including package information, activities, services, content providers, broadcast receivers, permissions, exports, and backups.
* **Security-Focused Analysis:** ReverseAPK includes functions to search for potential security vulnerabilities, such as:
    * OAuth secrets
    * DeviceId references
    * Android.intent references
    * Intent references
    * Command execution references
    * SQLiteDatabase references
    * Log.d references
    * Content provider references
    * Broadcast receiver references
    * Service references
    * File:// references
    * getSharedPreferences references
    * getExternal references
    * Crypto references
    * MessageDigest references
    * java.util.Random references
    * Base64 references
* **Progress Indicators:** The tool utilizes `rich` library to provide visually appealing progress indicators during time-consuming operations.

**Installation:**

1. **Dependencies:** Ensure you have the following tools installed:
    * `unzip`
    * `smali`
    * `apktool`
    * `d2j-dex2jar`
    * `jadx`
2. **Installation Script:** Run the `./install` script to install the required dependencies.

**Usage:**

1. **Run the script:** Execute the `trever.py` script.
2. **Provide APK path:** The script will prompt you to enter the path to the APK file you want to analyze.
3. **Analysis:** ReverseAPK will perform the analysis and display the results in the console.

**Example:**

```bash
./trever.py
```



**Note:**

* The script requires root privileges to access certain system files.
* The analysis results are displayed in the console. You can redirect the output to a file for later review.

**Disclaimer:**

This tool is intended for educational and security research purposes only. It should not be used for any illegal or unethical activities.

**Contributing:**

Contributions are welcome! Feel free to submit pull requests or open issues on the GitHub repository.

**License:**

This project is licensed under the MIT License.
