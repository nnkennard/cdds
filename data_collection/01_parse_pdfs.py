import argparse
import subprocess

import data_lib

parser = argparse.ArgumentParser(
    description="Run Grobid on a particular conference's pdfs")
parser.add_argument("-i", "--idx", type=int, help="Invitation index")
parser.add_argument("-p", "--path", type=str, help="Path to data directory")
parser.add_argument("-g",
                    "--grobid_path",
                    type=str,
                    help="Path to grobid directory")

# java -Xmx4G -jar
# grobid-0.7.1/grobid-core/build/libs/grobid-core-0.7.1-onejar.jar \
#        -gH grobid-0.7.1/grobid-home \
#            -dIn pdfs/ \
#                -dOut xmls/ \
#                    -exe processFullText


def main():

  args = parser.parse_args()

  conference_name, _, _ = data_lib.venues[args.idx]

  subprocess.run([
      "java",
      "-Xmx4G",
      "-jar",
      f"{args.grobid_path}/grobid-core/build/libs/grobid-core-0.7.1-onejar.jar",
      "-r",
      "-gH",
      f"{args.grobid_path}/grobid-home",
      "-dIn",
      f"{args.path}/{conference_name}",
      "-dOut",
      f"{args.path}/{conference_name}/parsed",
      "-exe",
      "processFullText",
  ])


if __name__ == "__main__":
  main()
