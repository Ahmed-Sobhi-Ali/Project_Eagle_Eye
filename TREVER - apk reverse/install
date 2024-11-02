#!/bin/bash
chmod +x trever.py
read -p "Do you want to add trever.py to /usr/bin/ (y/n)? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  cp trever.py /usr/bin/trever.py
  echo -e "\033[92mTrever.py added to /usr/bin/!\033[0m"
else
  echo -e "\033[93mTrever.py will not be added to /usr/bin/.\033[0m"
fi
sudo apt install unzip smali apktool dex2jar jadx
echo -e "\033[92mSucessful! To use, type trever.py <path_to_apk>.\033[0m"
