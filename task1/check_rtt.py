import csv
import argparse

import pythonping as pp


def read_file(name):
    with open(name, "r") as file:
        return file.read().splitlines()


def get_rtts(domains):
    rtts = []
    for domain in domains:
        response = pp.ping(domain)
        rtts.append(response.rtt_avg_ms)
    return rtts

def write_file(domains, rtts, name = "result.csv"):
    with open(name, "w", newline='') as file:
        fieldnames = ["Domain", "RTT"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for domain, rtt in zip(domains, rtts):
            writer.writerow({"Domain": domain, "RTT": rtt})

def main():
    parser = argparse.ArgumentParser(
        prog="Check_RTT",
        description="Use: <Program> <FileWithDomains.txt> <Result.csv>")

    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)
    args = parser.parse_args()

    domains = read_file(args.input)
    rtts = get_rtts(domains)
    write_file(domains, rtts, args.output)

if __name__ == "__main__":
    main()