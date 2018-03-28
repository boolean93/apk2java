import argparse
import commands
from os import path


def sh(cmd):
    print "executing: '%s'" % cmd
    return commands.getoutput(cmd)


def apk2dex(apk_path, output_path):
    print sh("unzip %s -d %s" % (apk_path, TEMP_PATH))
    print sh("mkdir " + output_path)
    print sh("mv %s/*.dex %s" % (TEMP_PATH, output_path))


def dex2jar(dex_dir, jar_dir):
    print sh("%s %s -o %s --force" % (DEX2JAR_PATH, dex_dir, jar_dir))


def jar2src(jar_dir, output_zip_dir):
    cmd = "java -jar %s %s --outputZipFile %s" % (JD_PATH, jar_dir, output_zip_dir)
    print sh(cmd)


def unzip(zip_dir, output_path):
    print sh("mkdir " + output_path)
    print sh("unzip %s -d %s" % (zip_dir, output_path))


base_dir = path.dirname(__file__)
if base_dir == "":
    base_dir = "."
base_dir += "/"

# lib
JD_PATH = base_dir + "jd-cli/jd-cli.jar"
DEX2JAR_PATH = base_dir + "dex2jar/d2j-dex2jar.sh"

# temp path
TEMP_PATH = base_dir + ".TEMP_PATH"
TEMP_DEX_PATH = base_dir + ".TEMP_DEX_PATH"
TEMP_JAR_PATH = base_dir + ".TEMP_JAR_PATH"
TEMP_ZIP_PATH = base_dir + ".TEMP_ZIP_PATH"

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--apk_file", help="Apk file directory", type=str)
parser.add_argument("-o", "--output_dir", help="Output directory", type=str)
args = parser.parse_args()


sh("mkdir " + TEMP_PATH)
sh("mkdir " + TEMP_DEX_PATH)
sh("mkdir " + TEMP_JAR_PATH)
sh("mkdir " + TEMP_ZIP_PATH)


apk_dir = args.apk_file
dex_dir = TEMP_DEX_PATH
jar_dir = TEMP_JAR_PATH
zip_dir = TEMP_ZIP_PATH
src_dir = args.output_dir

# APK->DEX
apk2dex(apk_dir, dex_dir)

# Find dex_files
dex_files = sh("ls %s | grep .dex" % dex_dir).split("\n")
for dex_file in dex_files:
    dex_file_path = dex_dir + "/" + dex_file
    output_jar_path = jar_dir + "/" + dex_file + ".jar"
    output_zip_path = zip_dir + "/" + dex_file + ".jar.src.zip"

    # DEX->JAR
    dex2jar(dex_file_path, output_jar_path)

    # JAR->ZIP
    jar2src(output_jar_path, output_zip_path)

    # ZIP->SRC
    print sh("mkdir " + src_dir)
    unzip(output_zip_path, src_dir + "/" + dex_file)


sh("rm -r " + TEMP_PATH)
sh("rm -r " + TEMP_DEX_PATH)
sh("rm -r " + TEMP_JAR_PATH)
sh("rm -r " + TEMP_ZIP_PATH)
