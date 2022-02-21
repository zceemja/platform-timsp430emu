import sys

from SCons.Script import DefaultEnvironment
env = DefaultEnvironment()

EMULATOR_VERSION_URL = "https://api.github.com/repos/zceemja/msp430emu/releases/latest"
EMULATOR_LINK = "https://github.com/zceemja/msp430emu/archive/master.zip"


def get_latest_emulator():
    import urllib.request
    import json
    response = urllib.request.urlopen(EMULATOR_VERSION_URL)
    data = json.loads(response.read())
    version = data.get('tag_name', 'v0.0').lstrip('v')
    asserts = [
        asset.get('browser_download_url')
        for asset in data.get('assets', [])
        if asset.get('browser_download_url')
    ]
    source = data.get('zipball_url', EMULATOR_LINK)
    body = data.get('body')
    if body:
        print("Latest version comment: " + str(body))
    return version, asserts, source


def ver_to_int(str_ver):
    sp = str_ver.split('.')
    return int(sp[0]), int(sp[1])


def update_emulator():
    print(f"Platform: {sys.platform}")
    print(f"Python ver: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    latest_ver, asserts, source = get_latest_emulator()
    try:
        import msp430emu
        print(f"Emulator ver: {msp430emu.__version__}")
        local_ver_major, local_ver_minor = ver_to_int(msp430emu.__version__)
        remote_ver_major, remote_ver_minor = ver_to_int(latest_ver)
        if local_ver_major > remote_ver_major or local_ver_minor >= remote_ver_minor:
            return
    except ImportError:  # if no emulator
        print(f"Emulator ver: -- no emulator --")
    except AttributeError:  # if emulator is old and has not __version__
        print(f"Emulator ver: -- no version --")
    print(f"Updating to new emulator: {latest_ver}")
    pkg_link = source
    if sys.platform == "win32":
        for asset in asserts:
            if 'win_amd64' in asset:
                pkg_link = asset
    env.Execute('pip install "%s"' % pkg_link)


def on_upload(source, target, env):
    update_emulator()
    firmware_path = str(source[0])[:-4]
    if sys.platform == 'darwin':
        # Running platformio python causes issues with opening GUI
        env.Execute('PYTHONPATH="%s" /usr/bin/python3 -m msp430emu "%s.bin"' % (':'.join(sys.path), firmware_path))
    else:
        env.Execute('python -m msp430emu "%s.bin"' % firmware_path)


env.Replace(UPLOADCMD=on_upload)

env.AddPostAction(
    "$BUILD_DIR/${PROGNAME}.elf",
    env.VerboseAction(" ".join([
        "$OBJCOPY", "-I", "elf32-little", "-O", "binary",
        "$BUILD_DIR/${PROGNAME}.elf", "$BUILD_DIR/${PROGNAME}.bin"
    ]), "Building $BUILD_DIR/${PROGNAME}.bin")
)
