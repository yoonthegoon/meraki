from cisco_meraki import main
import json


if __name__ == '__main__':
    j = json.load(open('config.json'))
    main(
        network_id=j["network id"],
        school=j["school"],
        address=j["address"],
        lat=j["lat"],
        lng=j["lon"]
    )
