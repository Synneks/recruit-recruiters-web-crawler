import json

with open("Cluj.txt", "r") as f:
    with open("converted_cluj.txt", "a") as output:
        for line in f.readlines():
            technology = json.loads(line)
            for tech in technology:
                for neighbour in technology[tech]['technologies']:
                    if str(tech) != str(neighbour) and technology[tech]['technologies'][neighbour] / technology[tech]['total_offers'] > 0.1:
                        output.write(str(tech) + "," + str(neighbour) + "\n")
