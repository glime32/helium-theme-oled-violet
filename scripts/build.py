#!/usr/bin/env python3
"""Build dist/: one signed .crx per extension + updates.xml for Helium's auto-update.

usage: build.py VERSION BASE_URL   (keys are read from keys/<name>.pem)
"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from pack_crx import pack

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTENSIONS = ["theme", "pages"]


def main(version, base_url):
    dist, build = os.path.join(ROOT, "dist"), os.path.join(ROOT, "build")
    for d in (dist, build):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    apps = []
    for name in EXTENSIONS:
        src = os.path.join(build, name)
        shutil.copytree(os.path.join(ROOT, name), src)
        manifest_path = os.path.join(src, "manifest.json")
        manifest = json.load(open(manifest_path, encoding="utf-8"))
        manifest["version"] = version
        json.dump(manifest, open(manifest_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        crx = f"oled-violet-{name}.crx"
        ext_id = pack(src, os.path.join(ROOT, "keys", f"{name}.pem"), os.path.join(dist, crx))
        apps.append(f"  <app appid='{ext_id}'>\n"
                    f"    <updatecheck codebase='{base_url}/{crx}' version='{version}' />\n"
                    f"  </app>")
        print(f"{name}: {ext_id} v{version}")
    with open(os.path.join(dist, "updates.xml"), "w") as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n"
                "<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>\n"
                + "\n".join(apps) + "\n</gupdate>\n")
    with open(os.path.join(dist, "index.html"), "w") as f:
        f.write(f"<!doctype html><meta charset='utf-8'><title>OLED Violet</title>"
                f"<body style='background:#000;color:#ebebeb;font-family:sans-serif'>"
                f"<h1 style='color:#d7adff'>OLED Violet {version}</h1><ul>"
                + "".join(f"<li><a style='color:#d7adff' href='oled-violet-{n}.crx'>oled-violet-{n}.crx</a></li>" for n in EXTENSIONS)
                + "</ul>")


if __name__ == "__main__":
    main(*sys.argv[1:3])
